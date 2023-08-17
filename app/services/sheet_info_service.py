"""
Methods related to operations on sheet info worksheet
"""

import logging
from gspread.exceptions import GSpreadException, SpreadsheetNotFound
from app.const import WORKBOOK, SHEET_INFO

class SheetInfoService:
    """
    Sheet info service
    """

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def update_row_count(self, worksheet_name, row_count):
        """
        Update info sheet with no. of rows in the given data sheet.
        """
        try:
            info_sheet = self.client.open(WORKBOOK).worksheet(SHEET_INFO)
            row_no = None
            if row_count is None:
                # Open the given worksheet
                data_sheet = self.client.open(
                    WORKBOOK).worksheet(worksheet_name)
                # Fetch the total no. of records in the worksheet.
                records = data_sheet.get_all_records()
                row_count = len(records)
                # Open the sheet information worksheet
                cell = info_sheet.find(worksheet_name)
                row_no = cell.row
            # Update the record count
            if row_no is not None:
                info_sheet.update_cell(row_no, 2, row_count)
            else:
                info_sheet.append_row(
                    [worksheet_name, row_count, ""], value_input_option='USER_ENTERED')
            self.logger.info("Succesffully updatd the row count of data sheet %s in  %s",
                        worksheet_name, SHEET_INFO)
        except SpreadsheetNotFound as not_found_error:
            self.logger.exception(
                "SheetInfoService - update_row_count: %s", not_found_error)
            raise not_found_error
        except GSpreadException as gspread_error:
            self.logger.exception(
                "SheetInfoService - update_row_count: %s", gspread_error)
            raise gspread_error
        except Exception as other_error:
            self.logger.exception(
                "SheetInfoService - update_row_count: %s", other_error)
            raise other_error
