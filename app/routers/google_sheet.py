"""
Routings for worksheet
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Query, Body
from app.controllers.google_sheet_controller import GoogleSheetController

router = APIRouter(prefix="/google-sheet")


@router.get("/get-all-sheet-names")
async def get_all_sheet_names(
    path: str = Query(
        ..., description="Path to the credentials.json file")):
    """
    Router method to fetch all sheet names
    parameters: 
    """
    return GoogleSheetController(path).get_all_sheet_names()


@router.post("/write-data-to-sheet")
async def write_data_to_sheet(
        path: str = Query(
        ..., description="Path to the credentials.json file"),
        worksheet_name: str = Query(
        ..., description="Name of worksheet to write data"),
        data: List[Dict[str, Any]] = Body(
        ..., description="Name of worksheet to write data")):
    """
    Router method to write data to sheet 
    """
    return GoogleSheetController(path).write_data_to_sheet(worksheet_name, data)


@router.post("/write-data-to-new-sheet")
async def write_data_to_new_sheet(
    path: str = Query(
        ..., description="Path to the credentials.json file"),
    worksheet_name: str = Query(
        ..., description="Name of the new worksheet"),
    data: List[Dict[str, Any]] = Body(
        ..., description="Name of worksheet to write data")):
    """
    Router method to write data to new sheet
    """
    return GoogleSheetController(path).write_data_to_new_sheet(worksheet_name, data)
