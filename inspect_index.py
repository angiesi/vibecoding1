"""
Script to inspect the existing Azure Search index schema.
"""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
import os
from dotenv import load_dotenv

load_dotenv()

def inspect_index():
    """Inspect the existing index schema."""
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "angiesichowindex")
    
    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
    
    print(f"Inspecting index: {index_name}")
    print("="*70)
    
    # Get the index schema
    try:
        index = index_client.get_index(index_name)
        print(f"\n✅ Index '{index_name}' exists!")
        print(f"\nFields in the index:")
        print("-"*70)
        for field in index.fields:
            print(f"  - {field.name} ({field.type}){' [KEY]' if field.key else ''}")
        
        # Try to get a sample document
        print("\n" + "-"*70)
        print("Sample documents in the index:")
        print("-"*70)
        results = search_client.search(search_text="*", top=2)
        for i, result in enumerate(results, 1):
            print(f"\nDocument {i}:")
            for key, value in result.items():
                if not key.startswith('@'):
                    print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_index()
