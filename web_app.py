"""
Dog Food Recommendation Web Application
Web interface for helping humans find daily food recommendations for their dogs.
"""

from flask import Flask, render_template, request, jsonify
from dog_food_app import DogFoodRecommendationApp

app = Flask(__name__)

# Initialize the recommendation app
recommendation_app = DogFoodRecommendationApp()

# Setup search index on startup
try:
    recommendation_app.setup_search_index()
    print("Search index initialized successfully")
except Exception as e:
    print(f"Note: {e}")
    print("Running in local mode...")


@app.route('/')
def index():
    """Render the main page."""
    # Get list of available breeds from Azure Search
    breeds = get_all_breeds()
    return render_template('index.html', breeds=breeds)


def get_all_breeds():
    """Get all unique breed names from Azure Search."""
    try:
        # Query Azure Search to get all breeds
        search_client = recommendation_app.search_client.search_client
        results = search_client.search(
            search_text="*",
            select=["breed"],
            top=1000
        )
        
        # Extract unique breeds and sort them
        breeds = set()
        for result in results:
            breed = result.get('breed')
            if breed:
                breeds.add(breed)
        
        return sorted(list(breeds))
    except Exception as e:
        print(f"Error getting breeds: {e}")
        # Return default breeds if Azure Search fails
        return ['Labrador Retriever', 'Golden Retriever', 'German Shepherd', 'Bulldog', 
                'Beagle', 'Poodle', 'Rottweiler', 'Yorkshire Terrier', 'Boxer', 'Dachshund']


@app.route('/search', methods=['POST'])
def search():
    """Handle search requests."""
    try:
        data = request.get_json()
        search_type = data.get('search_type')
        search_value = data.get('search_value')
        
        results = []
        
        if search_type == 'breed':
            results = recommendation_app.get_recommendation_by_breed(search_value)
        elif search_type == 'size':
            results = recommendation_app.get_recommendation_by_size(search_value.lower())
        elif search_type == 'weight':
            try:
                weight = float(search_value)
                results = recommendation_app.get_recommendation_by_weight(weight)
            except ValueError:
                return jsonify({'error': 'Peso inválido. Por favor ingresa un número.'}), 400
        else:
            return jsonify({'error': 'Tipo de búsqueda no válido'}), 400
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
