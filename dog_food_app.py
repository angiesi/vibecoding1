"""
Dog Food Recommendation Application
Main application for helping humans find daily food recommendations for their dogs.
"""

from typing import Dict, List
from azure_search_client import DogFoodSearchClient
from dog_food_data import DOG_FOOD_DATABASE


class DogFoodRecommendationApp:
    """Application for dog food recommendations."""
    
    def __init__(self):
        """Initialize the application with Azure Search client."""
        self.search_client = DogFoodSearchClient()
    
    def setup_search_index(self):
        """Set up the Azure Search index with dog food data."""
        print("Setting up search index...")
        self.search_client.create_index()
        self.search_client.upload_documents(DOG_FOOD_DATABASE)
        print("Search index setup complete.")
    
    def get_recommendation_by_breed(self, breed: str) -> List[Dict]:
        """
        Get food recommendations for a specific dog breed.
        
        Args:
            breed: The dog breed name
            
        Returns:
            List of food recommendations
        """
        print(f"\nBuscando recomendaciones para raza: {breed}")
        results = self.search_client.search_by_breed(breed)
        return results
    
    def get_recommendation_by_size(self, size: str) -> List[Dict]:
        """
        Get food recommendations for dogs of a specific size.
        
        Args:
            size: Dog size (pequeño, mediano, grande)
            
        Returns:
            List of food recommendations
        """
        print(f"\nBuscando recomendaciones para tamaño: {size}")
        results = self.search_client.search_by_size(size)
        return results
    
    def get_recommendation_by_weight(self, weight_kg: float) -> List[Dict]:
        """
        Get food recommendations for dogs of a specific weight.
        
        Args:
            weight_kg: Dog weight in kilograms
            
        Returns:
            List of food recommendations
        """
        print(f"\nBuscando recomendaciones para peso: {weight_kg} kg")
        results = self.search_client.search_by_weight(weight_kg)
        return results
    
    def display_recommendation(self, recommendation: Dict):
        """Display a single recommendation in a formatted way."""
        print("\n" + "="*60)
        print(f"Raza: {recommendation['breed']}")
        print(f"Tamaño: {recommendation['size']}")
        print(f"Rango de peso: {recommendation['weight_range']}")
        print(f"\nPorciones diarias: {recommendation['daily_portions']}")
        print(f"Tamaño de porción: {recommendation['portion_size_grams']} gramos")
        print(f"\nContenido nutricional por porción:")
        print(f"  - Proteína: {recommendation['protein_per_portion']}g")
        print(f"  - Fibra: {recommendation['fiber_per_portion']}g")
        print(f"  - Grasa: {recommendation['fat_per_portion']}g")
        print(f"  - Calorías: {recommendation['calories_per_portion']} kcal")
        print(f"\nRecomendaciones: {recommendation['recommendations']}")
        print("="*60)
    
    def display_recommendations(self, recommendations: List[Dict]):
        """Display multiple recommendations."""
        if not recommendations:
            print("\nNo se encontraron recomendaciones para los criterios especificados.")
            return
        
        print(f"\nSe encontraron {len(recommendations)} recomendaciones:")
        for recommendation in recommendations:
            self.display_recommendation(recommendation)
    
    def interactive_search(self):
        """Interactive search interface for users."""
        print("\n" + "="*60)
        print("Bienvenido a la Aplicación de Recomendaciones de Comida para Perros")
        print("="*60)
        
        while True:
            print("\n¿Cómo deseas buscar?")
            print("1. Por raza")
            print("2. Por tamaño (pequeño, mediano, grande)")
            print("3. Por peso (en kg)")
            print("4. Salir")
            
            choice = input("\nElige una opción (1-4): ").strip()
            
            if choice == "1":
                breed = input("Ingresa la raza del perro: ").strip()
                results = self.get_recommendation_by_breed(breed)
                self.display_recommendations(results)
            
            elif choice == "2":
                size = input("Ingresa el tamaño (pequeño, mediano, grande): ").strip().lower()
                results = self.get_recommendation_by_size(size)
                self.display_recommendations(results)
            
            elif choice == "3":
                try:
                    weight = float(input("Ingresa el peso en kg: ").strip())
                    results = self.get_recommendation_by_weight(weight)
                    self.display_recommendations(results)
                except ValueError:
                    print("Por favor ingresa un número válido para el peso.")
            
            elif choice == "4":
                print("\n¡Gracias por usar la aplicación!")
                break
            
            else:
                print("Opción no válida. Por favor elige 1-4.")


def main():
    """Main entry point for the application."""
    app = DogFoodRecommendationApp()
    
    # Setup search index (only needed once or when data changes)
    print("Inicializando la aplicación...")
    try:
        app.setup_search_index()
    except Exception as e:
        print(f"Note: {e}")
        print("Continuando en modo local (sin Azure Search)...")
    
    # Run interactive search
    app.interactive_search()


if __name__ == "__main__":
    main()
