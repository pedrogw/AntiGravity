from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from app.api.auth import router as auth_router
from app.api.places import router as places_router
from app.api.deliveries import router as deliveries_router

app = FastAPI(
    title="Logistics Manager API",
    description="Motor analítico B2B para rastreamento inteligente, SLAs e injeção de Chaos.",
    version="1.0.0"
)

# CORS configurations
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(places_router, prefix="/places", tags=["places"])
app.include_router(deliveries_router, prefix="/deliveries", tags=["deliveries"])

@app.exception_handler(OperationalError)
async def db_connection_exception_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Database Unavailable (503). O banco de dados está fora do ar ou injetado em Chaos."}
    )

@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": "dev"}
