from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth
from db.database import engine, Base

app = FastAPI()

# Set CORS
origins = [
    "http://localhost:3000", 
     "*" # Adjust this to match the domain of your frontend if it's not running on localhost:3000
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
    uvicorn.run(app, host="0.0.0.0", port=8001)