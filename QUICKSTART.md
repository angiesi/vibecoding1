# Guía de Inicio Rápido

## Instalación en 3 pasos

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. (Opcional) Configurar Azure Search
Si tienes una instancia de Azure Search:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

**Nota**: La aplicación funciona sin Azure Search usando búsqueda local.

### 3. Ejecutar la aplicación
```bash
python dog_food_app.py
```

## Ejemplos de Uso Rápido

### Modo Interactivo
```bash
python dog_food_app.py
```
Sigue las instrucciones en pantalla para buscar por:
- Raza del perro
- Tamaño (pequeño/mediano/grande)
- Peso en kg

### Modo Programático (Demo)
```bash
python example_usage.py
```
Muestra ejemplos de todas las funcionalidades.

## Razas Disponibles

**Pequeños**: Chihuahua, Yorkshire Terrier, Poodle, Dachshund

**Medianos**: Beagle, Bulldog

**Grandes**: Labrador, Golden Retriever, Pastor Alemán, Rottweiler, Boxer, Husky Siberiano

## Información Nutricional Incluida

Para cada raza, obtendrás:
- ✅ Porciones diarias recomendadas
- ✅ Tamaño de porción en gramos
- ✅ Proteína por porción
- ✅ Fibra por porción
- ✅ Grasa por porción
- ✅ Calorías por porción
- ✅ Recomendaciones específicas

## Ejemplo de Salida

```
============================================================
Raza: Labrador
Tamaño: grande
Rango de peso: 25-36 kg

Porciones diarias: 3
Tamaño de porción: 300 gramos

Contenido nutricional por porción:
  - Proteína: 35g
  - Fibra: 8g
  - Grasa: 15g
  - Calorías: 450 kcal

Recomendaciones: Comida para razas grandes, activas, balance de proteína y fibra
============================================================
```

## Solución de Problemas

**Error al instalar dependencias**: Asegúrate de tener Python 3.7 o superior
```bash
python --version
```

**La aplicación funciona lentamente**: Esto es normal en la primera ejecución mientras se cargan las dependencias.

**No tengo Azure Search**: ¡No hay problema! La aplicación funciona perfectamente en modo local.

## Próximos Pasos

1. Experimenta con diferentes razas y pesos
2. Revisa el código en `dog_food_app.py` para entender cómo funciona
3. Consulta la documentación completa en `README.md`
4. Considera configurar Azure Search para búsquedas más avanzadas
