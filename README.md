# Dog Food Recommendation Application

Aplicación para ayudar a los humanos a encontrar recomendaciones diarias de comida para sus perros basadas en raza, tamaño y peso, utilizando Azure Search para la recuperación de información.

## Descripción

Esta aplicación permite buscar y obtener recomendaciones nutricionales para perros en base a:
- **Raza**: Buscar por raza específica del perro
- **Tamaño**: Filtrar por tamaño (pequeño, mediano, grande)
- **Peso**: Encontrar recomendaciones basadas en el peso del perro

La base de datos incluye información nutricional detallada por porción:
- Proteína (gramos)
- Fibra (gramos)
- Grasa (gramos)
- Calorías (kcal)
- Tamaño de porción recomendado
- Número de porciones diarias

## Tecnologías

- **Python 3.7+**
- **Azure Search** para retrieval de información
- **Vibecoding** para desarrollo rápido
- Base de datos ficticia con 12 razas de perros

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/angiesi/vibecoding1.git
cd vibecoding1
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno (opcional para Azure Search):
```bash
cp .env.example .env
# Editar .env con tus credenciales de Azure Search
```

### Variables de Entorno

Si deseas usar Azure Search (opcional), configura las siguientes variables en `.env`:

```
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your-search-admin-key
AZURE_SEARCH_INDEX_NAME=dog-food-recommendations
```

**Nota**: La aplicación funciona sin Azure Search usando búsqueda local como fallback.

## Uso

### Ejecutar la aplicación interactiva:

```bash
python dog_food_app.py
```

La aplicación te presentará un menú interactivo:

```
Bienvenido a la Aplicación de Recomendaciones de Comida para Perros
==================================================================

¿Cómo deseas buscar?
1. Por raza
2. Por tamaño (pequeño, mediano, grande)
3. Por peso (en kg)
4. Salir
```

### Ejemplos de uso:

#### Buscar por raza:
```
Elige una opción: 1
Ingresa la raza del perro: Labrador
```

#### Buscar por tamaño:
```
Elige una opción: 2
Ingresa el tamaño: grande
```

#### Buscar por peso:
```
Elige una opción: 3
Ingresa el peso en kg: 25
```

## Estructura del Proyecto

```
vibecoding1/
├── README.md                   # Documentación
├── requirements.txt            # Dependencias de Python
├── .env.example               # Ejemplo de configuración
├── .gitignore                 # Archivos ignorados por git
├── dog_food_data.py           # Base de datos ficticia
├── azure_search_client.py     # Cliente de Azure Search
└── dog_food_app.py            # Aplicación principal
```

## Base de Datos

La aplicación incluye datos ficticios para 12 razas de perros:

1. Chihuahua (pequeño)
2. Yorkshire Terrier (pequeño)
3. Poodle (pequeño)
4. Dachshund (pequeño)
5. Beagle (mediano)
6. Bulldog (mediano)
7. Labrador (grande)
8. Golden Retriever (grande)
9. Pastor Alemán (grande)
10. Rottweiler (grande)
11. Boxer (grande)
12. Husky Siberiano (grande)

Cada entrada incluye información nutricional completa y recomendaciones específicas.

## Futuras Mejoras

- [ ] Integración con AI Foundry para agents con knowledge
- [ ] Agregar más razas a la base de datos
- [ ] Implementar recomendaciones personalizadas basadas en actividad del perro
- [ ] API REST para integración con otras aplicaciones
- [ ] Interfaz web con UI moderna
- [ ] Soporte para alergias y restricciones dietéticas
- [ ] Seguimiento de historial de alimentación

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
