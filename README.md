# API de Predicción de Enfermedades con ML

Esta API recibe síntomas, edad y sexo, y devuelve la enfermedad predicha junto con una recomendación.

### Cómo ejecutar localmente con Docker

```bash
# 1. Construir imagen
docker build -t enfermedades-ml .

# 2. Ejecutar contenedor
docker run -d -p 8000:8000 --name enfermedades-api enfermedades-ml

# 3. Api disponible en:
# http://localhost:8000/graphql

# NOTA:
# El entorno Docker no incluye GraphQL por defecto para evitar errores de dependencia con starlette.
# Si deseas probar localmente la API con GraphQL:
# 1. Instala Strawberry: pip install "strawberry-graphql[asgi]"
# 2. Descomenta las líneas correspondientes en `main.py`
# 3. Ejecuta: uvicorn main:app --reload
