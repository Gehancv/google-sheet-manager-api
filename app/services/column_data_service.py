"""
Methods related to operations on column info worksheet
"""

import logging
from gspread.exceptions import GSpreadException, SpreadsheetNotFound
from app.const import WORKBOOK, COLUMN_INFO

class ColumnDataService:
    """
    Column data service
    """

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def get_all_sheet_names(self):
        """
        Fetch all the data sheet names in the given spreadsheet.
        Return: list of data sheet names
        """
        try:
            # Open the column information worksheet
            sheet = self.client.open(WORKBOOK).worksheet(COLUMN_INFO)
            # Convert to a set to get the unique sheet names
            sheet_names = set(sheet.col_values(3))
            # Remove the topic SheetName
            sheet_names.remove("sheetName")
            name_list = list(sheet_names)
            self.logger.info("Successfully fetched sheet names from %s",
                        COLUMN_INFO)
            return name_list
        except SpreadsheetNotFound as not_found_error:
            self.logger.exception("ColumnDataService - get_all_sheet_names: %s", not_found_error)
            raise not_found_error
        except GSpreadException as gspread_error:
            self.logger.exception("ColumnDataService - get_all_sheet_names: %s", gspread_error)
            raise gspread_error
        except Exception as other_error:
            self.logger.exception("ColumnDataService - get_all_sheet_names: %s", other_error)
            raise other_error

    def update_column_info(self, sheet_name, column_info):
        """
        Update column_data sheet with new worksheet information
        """
        try:
            sheet = self.client.open(WORKBOOK).worksheet(COLUMN_INFO)
            column_list = []
            for i, col_info in enumerate(column_info):
                column_list.append(
                    [col_info[0], str(col_info[1]), sheet_name])
            self.logger.info(column_list)
            sheet.append_rows(column_list, value_input_option='USER_ENTERED')
            self.logger.info("Successfully updated column info of %s in %s",
                        sheet_name, COLUMN_INFO)
        except SpreadsheetNotFound as not_found_error:
            self.logger.exception("ColumnDataService - update_row_count: %s", not_found_error)
            raise not_found_error
        except GSpreadException as gspread_error:
            self.logger.exception("ColumnDataService - update_row_count: %s", gspread_error)
            raise gspread_error
        except Exception as other_error:
            self.logger.exception("ColumnDataService - update_row_count: %s", other_error)
            raise other_error
