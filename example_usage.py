"""
Example usage of the Dog Food Recommendation Application
Demonstrates programmatic usage without interactive mode.
"""

from dog_food_app import DogFoodRecommendationApp


def main():
    """Demonstrate various usage patterns."""
    print("="*70)
    print("Demo de la Aplicación de Recomendaciones de Comida para Perros")
    print("="*70)
    
    # Initialize the application
    app = DogFoodRecommendationApp()
    
    # Example 1: Search by breed
    print("\n\n### EJEMPLO 1: Buscar por raza (Labrador) ###")
    results = app.get_recommendation_by_breed("Labrador")
    app.display_recommendations(results)
    
    # Example 2: Search by size
    print("\n\n### EJEMPLO 2: Buscar por tamaño (pequeño) ###")
    results = app.get_recommendation_by_size("pequeño")
    app.display_recommendations(results)
    
    # Example 3: Search by weight
    print("\n\n### EJEMPLO 3: Buscar por peso (30 kg) ###")
    results = app.get_recommendation_by_weight(30)
    app.display_recommendations(results)
    
    # Example 4: Get specific nutritional info
    print("\n\n### EJEMPLO 4: Información nutricional para Pastor Alemán ###")
    results = app.get_recommendation_by_breed("Pastor Alemán")
    if results:
        recommendation = results[0]
        print(f"\nRaza: {recommendation['breed']}")
        print(f"Necesidades diarias:")
        total_protein = recommendation['protein_per_portion'] * recommendation['daily_portions']
        total_fiber = recommendation['fiber_per_portion'] * recommendation['daily_portions']
        total_calories = recommendation['calories_per_portion'] * recommendation['daily_portions']
        print(f"  - Proteína total: {total_protein}g")
        print(f"  - Fibra total: {total_fiber}g")
        print(f"  - Calorías totales: {total_calories} kcal")
    
    print("\n\n" + "="*70)
    print("Demo completado. Usa 'python dog_food_app.py' para modo interactivo.")
    print("="*70)


if __name__ == "__main__":
    main()
