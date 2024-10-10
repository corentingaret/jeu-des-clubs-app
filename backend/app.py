from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials

from routes import country_routes, player_routes
from helpers.database import engine, SessionLocal
from helpers.auth import get_current_user
from models import Base

load_dotenv(".env")

app = FastAPI()

# Initialize Firebase Admin SDK
service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers
app.include_router(country_routes.router)
app.include_router(player_routes.router)

# Example Protected Route
@app.get("/api/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}!"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
