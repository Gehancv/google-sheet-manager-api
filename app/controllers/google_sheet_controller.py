"""
Controller for google sheet handling
"""

import logging
from fastapi import status
from gspread.exceptions import GSpreadException, SpreadsheetNotFound
from app.services.authenticate_service import AuthenticateService
from app.services.column_data_service import ColumnDataService
from app.services.sheet_info_service import SheetInfoService
from app.services.data_service import DataService

class GoogleSheetController:
    """
    Authentication Controller
    """

    def __init__(self, path):
        self.client = AuthenticateService(path.strip("'")).authorize()
        self.logger = logging.getLogger(__name__)

    def get_all_sheet_names(self):
        """
        Fetch all sheet names
        Return: list of sheet names
        """
        try:
            res = ColumnDataService(self.client).get_all_sheet_names()
            if res is not None:
                self.logger.info("Fetched sheet names succesffuly")
                return res, status.HTTP_200_OK
        except SpreadsheetNotFound as not_found_error:
            self.logger.error("Error reading sheet names %s", not_found_error)
            return {'Error reading sheet names':
                    str(not_found_error)}, status.HTTP_404_NOT_FOUND
        except GSpreadException as gspread_error:
            self.logger.error("Error reading sheet names %s", gspread_error)
            return {'Error reading sheet names':
                    str(gspread_error)}, status.HTTP_400_BAD_REQUEST

    def write_data_to_sheet(self, worksheet_name, data):
        """
        Write data to sheet
        Return: True or Error
        """
        try:
            res = DataService(self.client).write_data_to_sheet(
                worksheet_name.strip("'"), data)
            SheetInfoService(self.client).update_row_count(
                worksheet_name.strip("'"))
            if res:
                self.logger.info("Data written to sheet successfully")
                return {"Data written to sheet successfully"}, status.HTTP_200_OK
        except SpreadsheetNotFound as not_found_error:
            self.logger.error("Error writing data to sheet: %s", not_found_error)
            return {'Error writing data to sheet':
                    str(not_found_error)}, status.HTTP_404_NOT_FOUND
        except GSpreadException as gspread_error:
            self.logger.error("Error writing data to sheet: %s", gspread_error)
            return {'Error writing data to sheet':
                    str(gspread_error)}, status.HTTP_400_BAD_REQUEST
        except Exception as other_error:
            self.logger.error("Error writing data to sheet: %s", other_error)
            return {'Error writing data to sheet':
                    str(other_error)}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def write_data_to_new_sheet(self, worksheet_name, data):
        """
        Write data to sheet
        Return: True or Error
        """
        try:
            res, no_records, col_info = DataService(
                self.client).write_data_to_new_sheet(worksheet_name.strip("'"), data)
            ColumnDataService(self.client).update_column_info(
                worksheet_name, col_info)
            SheetInfoService(self.client).update_row_count(
                worksheet_name, no_records)

            if res:
                self.logger.info("Data written to new sheet successfully")
                return {"Data written to sheet successfully"}, status.HTTP_200_OK
        except SpreadsheetNotFound as not_found_error:
            self.logger.error("Error writing data to new sheet: %s",
                         not_found_error)
            return {'Error writing data to new sheet':
                    str(not_found_error)}, status.HTTP_404_NOT_FOUND
        except GSpreadException as gspread_error:
            self.logger.error("Error writing data to new sheet: %s", gspread_error)
            return {'Error writing data to new sheet':
                    str(gspread_error)}, status.HTTP_400_BAD_REQUEST
        except Exception as other_error:
            self.logger.error("Error writing data to new sheet: %s", other_error)
            return {'Error writing data to new sheet':
                    str(other_error)}, status.HTTP_500_INTERNAL_SERVER_ERROR
