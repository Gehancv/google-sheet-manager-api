"""
Routings for worksheet
"""

from typing import List, Dict, Any
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.controllers.google_sheet_controller import GoogleSheetController

router = APIRouter(prefix="/google-sheet")


@router.post("/get-all-sheet-names")
async def get_all_sheet_names(path: str):
    """
    Router method to fetch all sheet names
    """
    try:
        return GoogleSheetController(path).get_all_sheet_names()
    except HTTPException as error:
        raise error


@router.post("/write-data-to-sheet")
async def write_data_to_sheet(path: str, worksheet_name: str, data: List[Dict[str, Any]]):
    """
    Router method to write data to sheet 
    """
    try:
        return GoogleSheetController(path).write_data_to_sheet(worksheet_name, data)
    except HTTPException as error:
        raise error

@router.post("/write-data-to-new-sheet")
async def write_data_to_new_sheet(path: str, worksheet_name: str, data: List[Dict[str, Any]]):
    """
    Router method to write data to new sheet
    """
    try:
        return GoogleSheetController(path).write_data_to_new_sheet(worksheet_name, data)
    except HTTPException as error:
        raise error

