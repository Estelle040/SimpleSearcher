from fastapi import FastAPI

app = FastAPI(
    title="Document Search API",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Service is running"}