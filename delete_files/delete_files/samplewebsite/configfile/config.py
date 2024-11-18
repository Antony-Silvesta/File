import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
def setup_mongodb():
    # Retrieve MongoDB URI from environment variable
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Ping to check connection
        print("MongoDB connected successfully!")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        exit(1)
    # Set up test data (example)
    db = client.get_database('your_database_name')  # Use a database for testing
    collection = db.get_collection('files_collection')
    # Example: Insert some test documents
    sample_data = [
        
        {
            "_id": "6739ac09ad8775c1de2acef0",
            "file_name": "sample.txt",
            "folder_name": "store1",
            "is_valid": True,
            "expected_error": "success",
            "createdAt": "2024-11-17T08:40:41.860Z",
            "uploadedBy": "admin@example.com",
            "baseurl": "https://demo.filebrowser.org/login",
            "user_name": "demo",
            "password": "demo",
            "folder_name1": "store"
        },
        {
            "_id": "6739ac09ad8775c1de2acef1",
            "file_name": "hellohello123.pdf",
            "folder_name": "store1",
            "is_valid": True,
            "expected_error": "success",
            "createdAt": "2024-11-17T08:40:41.878Z",
            "uploadedBy": "admin@example.com",
            "baseurl": "https://demo.filebrowser.org/login",
            "user_name": "demo",
            "password": "demo",
            "folder_name1": "store"
        },
        {
            "_id": "6739ac09ad8775c1de2acef2",
            "file_name": "sales_by_customer.pdf",
            "folder_name": "store1",
            "is_valid": True,
            "expected_error": "success",
            "createdAt": "2024-11-17T08:40:41.881Z",
            "uploadedBy": "admin@example.com",
            "baseurl": "https://demo.filebrowser.org/login",
            "user_name": "demo",
            "password": "demo",
            "folder_name1": "store"
        },
        {
            "_id": "6739ac09ad8775c1de2acef3",
            "file_name": "Monthly Report.pdf",
            "folder_name": "store1",
            "is_valid": True,
            "expected_error": "success",
            "createdAt": "2024-11-17T08:40:41.884Z",
            "uploadedBy": "admin@example.com",
            "baseurl": "https://demo.filebrowser.org/login",
            "user_name": "demo",
            "password": "demo",
            "folder_name1": "store"
        }
        
    ]
    
    collection.insert_many(sample_data)
    print(f"Test data inserted into {db.name}.{collection.name}")
if __name__ == "__main__":
    setup_mongodb()







