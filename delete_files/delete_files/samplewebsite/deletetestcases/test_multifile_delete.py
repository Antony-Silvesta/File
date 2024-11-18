import sys
sys.path.append(r"c:\Users\shinba\Downloads\delete_files\delete_files")
from samplewebsite.homeobjects.login import LoginPage

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from samplewebsite.homeobjects.login import LoginPage
from samplewebsite.homeobjects.home import HomePage
from samplewebsite.configfile.config import get_db, get_files_collection


@pytest.fixture(scope="class")
def setup_class():
    # Setup: Initialize WebDriver and MongoDB connection
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    # Connect to MongoDB and fetch valid delete files
    db = get_db()  # Establishes the database connection
    files_collection = get_files_collection()
    valid_delete_files = list(files_collection.find({"is_valid": True}))

    if not valid_delete_files:
        raise Exception("No valid files found in the database!")

    yield driver, valid_delete_files

    # Teardown: Quit the WebDriver after tests
    driver.quit()


@pytest.mark.usefixtures("setup_class")
class TestDeleteFiles:
    valid_delete_files = []

    @pytest.fixture(autouse=True)
    def login(self, setup_class):
        driver, valid_delete_files = setup_class
        self.driver = driver
        self.valid_delete_files = valid_delete_files
        self.logged_in = False  # Flag to track login status

        for index, delete_details in enumerate(self.valid_delete_files):
            if not all(key in delete_details for key in ["user_name", "password"]):
                print(f"Skipping entry at index {index} due to missing keys.")
                continue

            if not self.logged_in:
                username = delete_details["user_name"]
                password = delete_details["password"]
                base_url = delete_details["baseurl"]

                try:
                    self.driver.get(base_url)
                    print("Navigated to:", base_url)
                except Exception as e:
                    print("Error navigating to base URL:", e)
                    continue  # Skip to the next user if navigation fails

                lg = LoginPage(self.driver)
                try:
                    lg.setUsername(username)
                    lg.setPassword(password)
                    lg.clickLogin()
                    self.logged_in = True
                    print(f"Login successful for user: {username}")
                except Exception as e:
                    print(f"Error during login for {username}: {e}")
                    continue

    def test_delete_files(self):
        # Group files by folder_name
        folders = {}
        for delete_details in self.valid_delete_files:
            folder_name = delete_details.get("folder_name")
            if folder_name:
                if folder_name not in folders:
                    folders[folder_name] = []
                folders[folder_name].append(delete_details)

        # Process each folder
        for folder_name, files in folders.items():
            hp = HomePage(self.driver)
            hp.clickMyfiles()
            print("Clicked 'My Files'")

            # Retry mechanism for folder selection
            try:
                hp.selectFolder(folder_name)
                print(f"Folder '{folder_name}' selected")
            except TimeoutException:
                print(f"ERROR: Unable to locate the folder named '{folder_name}'. Moving on.")

            # Click the multi-icon to activate file selections
            hp.multiicon()
            print("Multi-icon clicked")

            # Select files within the selected folder
            for file_details in files:
                file_name = file_details.get("file_name")
                if not file_name:
                    print(f"Skipping entry due to missing file name.")
                    continue

                try:
                    hp.selectFile(file_name)
                    print(f"File selected for download: {file_name}")
                except TimeoutException:
                    print(f"File {file_name} not found for selection.")
                    continue

            hp.delete()
            hp.delete1()
            time.sleep(2)
