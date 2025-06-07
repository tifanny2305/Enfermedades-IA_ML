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
