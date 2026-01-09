"""
Script to delete the existing Azure Search index and create a fresh one.
"""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
import os
from dotenv import load_dotenv

load_dotenv()

def delete_and_recreate_index():
    """Delete the existing index if it exists."""
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "angiesichowindex")
    
    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    
    # List all indexes
    print("Existing indexes:")
    indexes = index_client.list_indexes()
    for index in indexes:
        print(f"  - {index.name}")
    
    # Delete the index if it exists
    try:
        print(f"\nDeleting index '{index_name}'...")
        index_client.delete_index(index_name)
        print(f"✅ Index '{index_name}' deleted successfully!")
    except Exception as e:
        print(f"Note: {e}")
    
    print("\nYou can now run the test script again to create a fresh index.")

if __name__ == "__main__":
    delete_and_recreate_index()
