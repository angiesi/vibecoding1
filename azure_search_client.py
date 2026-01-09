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
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "angiesichowindex")
        
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
    
    def _convert_result_to_app_format(self, result: Dict) -> Dict:
        """Convert Azure Search result to application format."""
        # Extract weight range
        weight_min = result.get("weight_min", 0)
        weight_max = result.get("weight_max", 0)
        weight_range = f"{weight_min}-{weight_max} kg"
        
        # Parse portion per kg to get grams
        portion_str = result.get("portion_per_kg", "20 g")
        try:
            portion_grams = int(portion_str.replace(" g", "").strip())
        except (ValueError, AttributeError):
            portion_grams = 20
        
        # Parse percentages
        def parse_percent(value, default=0):
            if value:
                try:
                    return int(value.replace("%", "").strip())
                except (ValueError, AttributeError):
                    return default
            return default
        
        return {
            "id": result.get("DogId", result.get("id", "unknown")),
            "breed": result.get("breed", "Unknown"),
            "size": result.get("size", "Unknown"),
            "weight_range": weight_range,
            "daily_portions": 2,
            "portion_size_grams": portion_grams,
            "protein_per_portion": parse_percent(result.get("protein")),
            "fiber_per_portion": parse_percent(result.get("fiber")),
            "fat_per_portion": parse_percent(result.get("fat")),
            "calories_per_portion": 300,
            "recommendations": result.get("notes", "No special notes")
        }
    
    def create_index(self):
        """Check if the index exists (no need to create - using existing index)."""
        if self.use_fallback:
            print("Using local search fallback mode.")
            return
        
        try:
            index = self.index_client.get_index(self.index_name)
            print(f"✅ Connected to existing index '{self.index_name}' with {len(index.fields)} fields.")
        except Exception as e:
            print(f"⚠️  Index '{self.index_name}' not found: {e}")
            print("Please ensure the index exists in your Azure Search service.")
    
    def upload_documents(self, documents: List[Dict]):
        """Note: The index already contains data. This method is not needed for existing index."""
        if self.use_fallback:
            print("Using local data in fallback mode.")
            return
        
        print("ℹ️  Using existing data in Azure Search index.")
        print("The index already contains dog nutrition data.")
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
                select=["DogId", "breed", "size", "weight_min", "weight_max", 
                       "protein", "fiber", "fat", "portion_per_kg", "notes"],
                top=top
            )
            return [self._convert_result_to_app_format(dict(result)) for result in results]
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
                select=["DogId", "breed", "size", "weight_min", "weight_max",
                       "protein", "fiber", "fat", "portion_per_kg", "notes"],
                top=top
            )
            return [self._convert_result_to_app_format(dict(result)) for result in results]
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
        
        # Search using weight range filter
        try:
            results = self.search_client.search(
                search_text="*",
                filter=f"weight_min le {weight_kg} and weight_max ge {weight_kg}",
                select=["DogId", "breed", "size", "weight_min", "weight_max",
                       "protein", "fiber", "fat", "portion_per_kg", "notes"],
                top=top
            )
            return [self._convert_result_to_app_format(dict(result)) for result in results]
        except Exception as e:
            print(f"Error searching by weight: {e}")
            return []
