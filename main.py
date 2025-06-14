import pickle
import numpy as np
import pandas as pd
import strawberry
from starlette.middleware.cors import CORSMiddleware
from starlette.applications import Starlette
from starlette.responses import Response
from strawberry.asgi import GraphQL

# Paso 1: Cargar modelo completo
with open("modelo_completo.pkl", "rb") as f:
    modelo_data = pickle.load(f)

modelo = modelo_data["modelo"]
columnas = modelo_data["columnas"]
traducciones = modelo_data["traducciones"]
recomendaciones = modelo_data["recomendaciones"]

# Paso 2: Definir esquema GraphQL
@strawberry.type
class Diagnostico:
    enfermedad: str
    recomendacion: str

@strawberry.type
class Query:
    @strawberry.field
    def predecir(
        self,
        edad: int,
        sexo: str,
        sintomas: str
    ) -> Diagnostico:
        # Convertir cadena en lista separada por coma
        lista_sintomas = [s.strip() for s in sintomas.split(",")]

        # Vector binario
        entrada = np.zeros(len(columnas))
        for sintoma in lista_sintomas:
            if sintoma in columnas:
                entrada[columnas.index(sintoma)] = 1

        entrada_df = pd.DataFrame([entrada], columns=columnas)

        # Predicción
        pred = modelo.predict(entrada_df)[0]
        enfermedad = traducciones.get(pred, pred)
        recomendacion = recomendaciones.get(pred, "Consultar con un médico especialista.")

        return Diagnostico(enfermedad=enfermedad, recomendacion=recomendacion)

# Paso 3: Crear app
schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)  # ⬅️ esto es la app GraphQL

app = Starlette()
# Manejo de OPTIONS para preflight
async def handle_cors_preflight(request):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",  # Cambia por tu dominio específico
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
            "Access-Control-Max-Age": "86400",
        }
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        "accept",
        "accept-encoding", 
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ],
)

# Agregar ruta OPTIONS antes del mount
app.add_route("/graphql", handle_cors_preflight, methods=["OPTIONS"])
app.mount("/graphql", graphql_app)
