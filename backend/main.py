from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.responses import JSONResponse
from backend.config.config import settings
from rate_limit import allow_general

from backend.routes import auth_routes, password_routes

app = FastAPI(
    title="Secure Password Manager",
    description="A simple fastapi application with authentication to manage secure passwords.",
    version="1.0.0",
)

app.add_middleware(
    HTTPSRedirectMiddleware,
    https_redirect=settings.HTTPS_REDIRECT,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(o) for o in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.middleware("http")
async def global_rate_limit(request: Request, call_next):
    ip = request.client.host if request.client.host else "unknown"
    if not allow_general(ip):
        return JSONResponse({"detail": "Too many requests"}, status_code=429)
    return await call_next(request)

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(password_routes.router, prefix="/passwords", tags=["Passwords"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Welcome to Secure Password Manager!"}
