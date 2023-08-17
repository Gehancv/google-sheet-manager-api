"""
Main entry for the project
"""

import logging.config
from fastapi import FastAPI
from app.routers import google_sheet

logging.config.fileConfig('logging.conf')

app = FastAPI(
    title="google-sheet-manager-api",
    description="API to manage google sheet database",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(google_sheet.router)
