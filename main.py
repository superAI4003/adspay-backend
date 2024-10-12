from fastapi import FastAPI
from routes import auth
from db.database import engine, Base

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth12",tags=["Auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)