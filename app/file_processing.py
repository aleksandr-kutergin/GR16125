import csv
import os
from io import StringIO

from dotenv import load_dotenv
from fastapi import UploadFile
from sqlalchemy.orm import Session

from .crud import save_file
from .schemas import FileCreate

load_dotenv()

SEARCHED_NAME = os.getenv("SEARCHED_NAME")


async def _search_in_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    line = file.readline()

    while line:
        if SEARCHED_NAME.lower() in line.decode("utf-8").lower():
            return True
        line = file.readline()

    return False


async def process_txt_file(file, db: Session, user_id: int):
    result = await _search_in_file(file)
    file_data = FileCreate(
        filename=file.filename,
        file_type="txt",
        result_found=result,
        user_id=user_id,
    )
    result = file_data.model_dump()
    result["id"] = save_file(db, file_data)
    return result


async def process_csv_file(file, db: Session, user_id: int):
    contents = await file.read()
    csv_reader = csv.reader(StringIO(contents.decode()))
    name_idx = next(csv_reader).index("Company Name")
    found = False
    for row in csv_reader:
        if any(SEARCHED_NAME.lower() in column.lower() for column in row):
            if row[name_idx].lower() == SEARCHED_NAME:
                found = True
            else:
                found = False
                break
    file_data = FileCreate(
        filename=file.filename,
        file_type="csv",
        result_found=found,
        user_id=user_id,
    )
    result = file_data.model_dump()
    result["id"] = save_file(db, file_data)
    return result
