from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth
from db.database import engine, Base

app = FastAPI()

# Set CORS
origins = [
    "http://161.35.15.35:3000",  # Update this to match the domain of your frontend
    "*"  # This allows all origins. Consider removing this if you want to restrict access.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth",tags=["Auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)