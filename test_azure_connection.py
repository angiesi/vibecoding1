"""
Test script to verify Azure AI Search connection and set up the index.
"""

from dog_food_app import DogFoodRecommendationApp


def test_connection():
    """Test Azure Search connection and setup."""
    print("="*70)
    print("Testing Azure AI Search Connection")
    print("="*70)
    
    # Initialize the application
    app = DogFoodRecommendationApp()
    
    # Check if we're using fallback mode or Azure Search
    if app.search_client.use_fallback:
        print("\n❌ Azure Search not configured - using local fallback mode")
        print("Please check your .env file configuration.")
        return False
    else:
        print("\n✅ Azure Search credentials loaded successfully")
        print(f"Endpoint: {app.search_client.endpoint}")
        print(f"Index Name: {app.search_client.index_name}")
    
    # Set up the search index and upload data
    print("\n" + "-"*70)
    print("Setting up search index and uploading data...")
    print("-"*70)
    
    try:
        app.setup_search_index()
        print("\n✅ Index setup and data upload completed successfully!")
    except Exception as e:
        print(f"\n❌ Error setting up index: {e}")
        return False
    
    # Test a simple search
    print("\n" + "-"*70)
    print("Testing search functionality...")
    print("-"*70)
    
    try:
        results = app.get_recommendation_by_breed("Labrador")
        if results:
            print(f"\n✅ Search successful! Found {len(results)} result(s)")
            print("\nSample result:")
            if len(results) > 0:
                app.display_recommendation(results[0])
        else:
            print("\n⚠️  Search completed but no results found")
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        return False
    
    print("\n" + "="*70)
    print("Azure AI Search connection test completed successfully! 🎉")
    print("="*70)
    return True


if __name__ == "__main__":
    test_connection()
