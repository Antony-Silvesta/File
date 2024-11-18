from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# class LoginPage():
#     username_field_id = "//textarea[@placeholder='e-mail address']"
#     password_field_id = "//input[@placeholder='password']"
#     login_button_name = "//button[.//span[text()='Login']]"  # Button name for login
#     error_message_xpath = "//div[contains(@class, 'q-notification__caption')]"

class LoginPage():
    def __init__(self, driver):
        self.driver = driver
    def setUsername(self, username):
        username_field = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Username']"))
        )

        username_field.clear()
        username_field.send_keys(username)

    def setPassword(self, password):
        password_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
        )
        password_field.send_keys(password)

    def clickLogin(self):
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Login']"))
        )
        login_button.click()


    def actualError(self):
        try:
            error_element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[text()='Wrong credentials']"))
            )
            return error_element.text
        except TimeoutException:
            print("Timeout: Element not found.")
            return None

    def getErrorPassword(self):
        return self.driver.find_element(By.XPATH, "//div[@role='alert' and text()='need text of minimum 8 characters']").text
    
    def usernameNotFound(self):
        return self.driver.find_element(By.XPATH, "//div[contains(@class, 'q-notification__caption') and text()='username not found']").text


    def usernameNotFound(self):
        wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds for the element
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'q-notification__caption') and text()='username not found']")))
            return element.text
        except TimeoutException:
            print("Element not found within the given time")
            return None


    def getErrorInvalidAccount(self):
        try:
                    # Wait for the error message to appear
            WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, self.error_message_xpath))
            )
            return self.driver.find_element(By.XPATH, self.error_message_xpath).text
        except TimeoutException:
                    return ''  # Return an empty string if the error message is not found
        
    def validationFailure(self):
        try:
            error_element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'q-notification__caption')]"))
            )
            return error_element.text
        except TimeoutException:
            print("Timeout: Element not found.")
            return None
