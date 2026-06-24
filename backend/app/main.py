import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.exc import OperationalError
from arq import create_pool
from arq.connections import RedisSettings
from app.api.auth import router as auth_router
from app.api.places import router as places_router
from app.api.deliveries import router as deliveries_router
from app.api.chaos import router as chaos_router
from app.api.alerts import router as alerts_router
from app.api.dashboard import router as dashboard_router
from app.core.bootstrap import dispose_engine
from app.core.config import settings
from app.core.events.bus import event_bus
from app.core.exceptions import DomainException
from app.infrastructure.cache.cache_service import CacheService
from app.infrastructure.cache.redis_client import get_redis, close_redis
from app.api.middleware import ObservabilityMiddleware
from app.core.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.logging import setup_logging

setup_logging()

logger = logging.getLogger("antigravity")


@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_pool = None
    try:
        redis = await get_redis()
        await redis.ping()
        cache_service = CacheService(redis)
        app.state.cache_service = cache_service
        worker_pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
        event_bus.worker_pool = worker_pool
        logger.info("Worker pool ARQ conectado — eventos serão processados em background")
    except Exception:
        logger.warning("Redis indisponível — eventos processados inline")
    yield
    if worker_pool is not None:
        await worker_pool.close()
    await close_redis()
    await dispose_engine()


app = FastAPI(
    title="Logistics Manager API",
    description="Motor analítico B2B para rastreamento inteligente, SLAs e injeção de Chaos.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = settings.ALLOWED_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ObservabilityMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(places_router, prefix="/places", tags=["places"])
app.include_router(deliveries_router, prefix="/deliveries", tags=["deliveries"])
app.include_router(chaos_router, prefix="", tags=["chaos"])
app.include_router(alerts_router, prefix="", tags=["alerts"])
app.include_router(dashboard_router, prefix="", tags=["dashboard"])


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    request_id = getattr(request.state, "request_id", None)
    logger.warning(
        "DomainException | request_id=%s status=%d detail=%s",
        request_id, exc.status_code, exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(OperationalError)
async def db_connection_exception_handler(request: Request, exc: OperationalError):
    request_id = getattr(request.state, "request_id", None)
    logger.error(
        "OperationalError | request_id=%s | %s",
        request_id, str(exc),
    )
    return JSONResponse(
        status_code=503,
        content={"detail": "Database Unavailable (503). O banco de dados está fora do ar ou injetado em Chaos."},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    logger.exception(
        "Unhandled exception | request_id=%s", request_id,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"},
    )


@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": "dev"}
