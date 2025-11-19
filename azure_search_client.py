"""
Azure Search client for dog food recommendations.
Handles indexing and searching of dog food data.
"""

import os
from typing import List, Dict, Optional
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)
from dotenv import load_dotenv

load_dotenv()


class DogFoodSearchClient:
    """Client for searching dog food recommendations using Azure Search."""
    
    def __init__(self):
        """Initialize Azure Search client with environment variables."""
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "dog-food-recommendations")
        
        if not self.endpoint or not self.key:
            print("Warning: Azure Search credentials not found in environment variables.")
            print("Using local search fallback mode.")
            self.use_fallback = True
        else:
            self.use_fallback = False
            self.credential = AzureKeyCredential(self.key)
            self.search_client = SearchClient(
                endpoint=self.endpoint,
                index_name=self.index_name,
                credential=self.credential
            )
            self.index_client = SearchIndexClient(
                endpoint=self.endpoint,
                credential=self.credential
            )
    
    def create_index(self):
        """Create the search index if it doesn't exist."""
        if self.use_fallback:
            print("Skipping index creation in fallback mode.")
            return
        
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="breed", type=SearchFieldDataType.String),
            SearchableField(name="size", type=SearchFieldDataType.String, filterable=True),
            SearchableField(name="weight_range", type=SearchFieldDataType.String),
            SimpleField(name="daily_portions", type=SearchFieldDataType.Int32),
            SimpleField(name="portion_size_grams", type=SearchFieldDataType.Int32),
            SimpleField(name="protein_per_portion", type=SearchFieldDataType.Int32),
            SimpleField(name="fiber_per_portion", type=SearchFieldDataType.Int32),
            SimpleField(name="fat_per_portion", type=SearchFieldDataType.Int32),
            SimpleField(name="calories_per_portion", type=SearchFieldDataType.Int32),
            SearchableField(name="recommendations", type=SearchFieldDataType.String)
        ]
        
        index = SearchIndex(name=self.index_name, fields=fields)
        
        try:
            self.index_client.create_or_update_index(index)
            print(f"Index '{self.index_name}' created successfully.")
        except Exception as e:
            print(f"Error creating index: {e}")
    
    def upload_documents(self, documents: List[Dict]):
        """Upload documents to the search index."""
        if self.use_fallback:
            print("Skipping document upload in fallback mode.")
            return
        
        try:
            result = self.search_client.upload_documents(documents=documents)
            print(f"Uploaded {len(documents)} documents successfully.")
            return result
        except Exception as e:
            print(f"Error uploading documents: {e}")
            return None
    
    def search_by_breed(self, breed: str, top: int = 5) -> List[Dict]:
        """Search for dog food recommendations by breed."""
        if self.use_fallback:
            from dog_food_data import DOG_FOOD_DATABASE
            results = [
                doc for doc in DOG_FOOD_DATABASE 
                if breed.lower() in doc['breed'].lower()
            ]
            return results[:top]
        
        try:
            results = self.search_client.search(
                search_text=breed,
                select=["breed", "size", "weight_range", "daily_portions", 
                       "portion_size_grams", "protein_per_portion", "fiber_per_portion",
                       "fat_per_portion", "calories_per_portion", "recommendations"],
                top=top
            )
            return [dict(result) for result in results]
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def search_by_size(self, size: str, top: int = 10) -> List[Dict]:
        """Search for dog food recommendations by size."""
        if self.use_fallback:
            from dog_food_data import DOG_FOOD_DATABASE
            results = [
                doc for doc in DOG_FOOD_DATABASE 
                if size.lower() in doc['size'].lower()
            ]
            return results[:top]
        
        try:
            results = self.search_client.search(
                search_text="",
                filter=f"size eq '{size}'",
                select=["breed", "size", "weight_range", "daily_portions",
                       "portion_size_grams", "protein_per_portion", "fiber_per_portion",
                       "fat_per_portion", "calories_per_portion", "recommendations"],
                top=top
            )
            return [dict(result) for result in results]
        except Exception as e:
            print(f"Error searching by size: {e}")
            return []
    
    def search_by_weight(self, weight_kg: float, top: int = 5) -> List[Dict]:
        """Search for dog food recommendations by weight (in kg)."""
        if self.use_fallback:
            from dog_food_data import DOG_FOOD_DATABASE
            results = []
            for doc in DOG_FOOD_DATABASE:
                weight_range = doc['weight_range'].replace(' kg', '').split('-')
                try:
                    min_weight = float(weight_range[0])
                    max_weight = float(weight_range[1])
                    if min_weight <= weight_kg <= max_weight:
                        results.append(doc)
                except (ValueError, IndexError):
                    continue
            return results[:top]
        
        # For Azure Search, we would need to implement range queries
        # For now, using text search
        try:
            results = self.search_client.search(
                search_text=f"{weight_kg} kg",
                select=["breed", "size", "weight_range", "daily_portions",
                       "portion_size_grams", "protein_per_portion", "fiber_per_portion",
                       "fat_per_portion", "calories_per_portion", "recommendations"],
                top=top
            )
            return [dict(result) for result in results]
        except Exception as e:
            print(f"Error searching by weight: {e}")
            return []
