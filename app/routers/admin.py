from fastapi import APIRouter, UploadFile, File

from app.loader import load_csv

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/load")
async def upload_csv(file: UploadFile = File(...)):
    """
    Загружает CSV файл в БД и Elasticsearch
    """

    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    await load_csv(file_path)

    return {"status": "loaded"}