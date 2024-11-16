from fastapi import APIRouter, status, Request
from schemas import *
from services import Classifier

router = APIRouter(tags=["Classifier"], prefix="/classifier")


@router.post("/create", response_model=Inform, status_code=status.HTTP_201_CREATED)
async def create_classifier(query: Query):
    return await Classifier.create(query)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_classifier(tablename: str):
    return await Classifier.get_all(tablename)

"""
@router.get("/get_by_id/{field_id}", status_code=status.HTTP_200_OK)
async def get_by_id_classifier(tablename: str, field_id: int):
    return await Classifier.get_by_id(tablename, field_id)


# потом уберу
@router.get("/get_by_name/{field_name}", status_code=status.HTTP_200_OK)
async def get_by_name_classifier(tablename: str, field_name: str):
    return await Classifier.get_by_name(tablename, field_name)
"""


@router.put("/update/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def update_classifier(field_id: int, query: Query):
    return await Classifier.update(field_id, query)


@router.delete("/delete/{field_id}", response_model=Inform, status_code=status.HTTP_200_OK)
async def delete_classifier(tablename: str, field_id: int):
    return await Classifier.delete(tablename, field_id)
