import datetime
from contextlib import asynccontextmanager

import pytz
import sentry_sdk
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request, Response
from fastapi_versioning import VersionedFastAPI, version
from jose import jwt, JWTError
from starlette.responses import StreamingResponse

from app.config import settings
from app.database import get_db
from app.models import Utente
from app.models.logUtente import CategoriaLogUtente
from app.routers.v1 import auth, admin, orientatore
from app.services.logs import log_user_action
from app.services.utentiTemporanei import elimina_utenti_temporanei

description = """
This is the API for the Vallauri orientamento project.
# Root
The API root is located at `/`, it responses with a welcome message.
## Authentication
The API uses JWT for authentication. You can obtain a token by sending a POST request to `/api/v1/auth/login`.
"""

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    # Pianifica il job per eseguire ogni giorno a mezzanotte
    scheduler.add_job(elimina_utenti_temporanei, 'cron', hour=0, minute=0)
    scheduler.start()
    yield


app = FastAPI(
    title=settings.app_name,
    description=description,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")
app.include_router(orientatore.router, prefix="/orientatore")


@app.get("/")
@version(1, 0)
async def read_root():
    """
    path di root dell'API

    restituisce un messaggio di benvenuto
    """
    return {"message": f"Welcome to {settings.app_name}"}


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')


@app.middleware("http")
async def log_user_action_middleware(request: Request, call_next):
    db = next(get_db())

    # recupera l'utente loggato dal token JWT
    user_id = None
    if "Authorization" in request.headers and request.headers["Authorization"].startswith("Bearer "):
        try:
            token = request.headers["Authorization"].split("Bearer ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
            user_id = db.query(Utente).filter(Utente.username == decoded_token["sub"]).first().id
        except JWTError:
            pass

    # Aggiunge log pre-richiesta (facoltativo)
    start_time = datetime.datetime.now(pytz.timezone("Europe/Rome"))

    # Read the request body
    dati_input = await request.body()
    request._body = dati_input  # Store the body in the request object

    # Processa la richiesta
    response = await call_next(request)

    # Aggiunge log post-richiesta
    end_time = datetime.datetime.now(pytz.timezone("Europe/Rome"))
    elapsed_time = (end_time - start_time).total_seconds()
    dati_input = dati_input.decode("utf-8", errors="ignore")

    # Leggi il corpo della risposta
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    dati_output = body.decode("utf-8")

    # Loggare l'azione
    if user_id:
        await log_user_action(
            utente_id=int(user_id),
            azione=f"Accessed {request.url.path}",
            categoria=CategoriaLogUtente.INFO,
            dati={"method": request.method, "status_code": response.status_code, "request_code": dati_input,
                  "request_output": dati_output, "elapsed_time": elapsed_time},
        )
    else:
        await log_user_action(
            azione=f"Accessed {request.url.path}",
            categoria=CategoriaLogUtente.INFO,
            dati={"method": request.method, "status_code": response.status_code, "request_code": dati_input,
                  "request_output": dati_output, "elapsed_time": elapsed_time},
        )
    return StreamingResponse(iter([body]), status_code=response.status_code, headers=dict(response.headers))


@app.middleware("http")
async def cors_handler(request: Request, call_next):
    # Gestione preflight OPTIONS
    if request.method == "OPTIONS":
        response = Response()
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response

    # Continuare con la richiesta normale
    response: Response = await call_next(request)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response
