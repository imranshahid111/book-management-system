from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.books import router as book_router
from database import engine
from models.book import Base

# Initialize FastAPI
app = FastAPI()

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(book_router)
