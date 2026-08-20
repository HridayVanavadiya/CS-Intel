from fastapi import FastAPI

from Backend.api.news_routes import router as news_router


app = FastAPI(
    title="CS Intel API",
    description="Computer Science Intelligence Platform",
    version="1.0.0"
)


app.include_router(news_router)


@app.get("/")
def root():
    return {
        "message": "CS Intel API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }