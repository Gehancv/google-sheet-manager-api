"""
Methods related to operations on sheets storing data
"""

import logging
import json
from gspread.exceptions import GSpreadException, SpreadsheetNotFound
from app.const import WORKBOOK


class DataService:
    """
    Data Service
    """

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def write_data_to_sheet(self, worksheet_name, data):
        """
        Write data to an existing worksheet
        Return: True if successful
        """
        try:
            # Get client name
            client_name = self.get_client_name()

            # Unpack data
            column_info, data = self.unpack_json_list(client_name, data, False)

            # Open the given worksheet
            sheet = self.client.open(WORKBOOK).worksheet(worksheet_name)
            # Append data lines to the end of the worksheet
            sheet.append_rows(data, value_input_option='USER_ENTERED')

            self.logger.info(
                "Completed writing data to sheet %s successfully.", worksheet_name)

            return True
        except SpreadsheetNotFound as not_found_error:
            self.logger.exception(
                "DataService - write_data_to_sheet: %s", not_found_error)
            raise not_found_error
        except GSpreadException as gspread_error:
            self.logger.exception(
                "DataService - write_data_to_sheet: %s", gspread_error)
            raise gspread_error
        except Exception as other_error:
            self.logger.exception(
                "DataService - write_data_to_sheet: %s", other_error)
            raise other_error

    def write_data_to_new_sheet(self, worksheet_name, data):
        """
        Write data to a new worksheet
        Return: True if successful, no. of records written and column information
        """
        try:
            client_name = self.get_client_name()
            column_info, data = self.unpack_json_list(client_name, data, True)

            workbook = self.client.open(WORKBOOK)
            sheet = workbook.add_worksheet(
                title=worksheet_name, rows=len(data), cols=len(data[0]))
            # Append data lines to the end of the worksheet
            sheet.append_rows(data, value_input_option='USER_ENTERED')
            self.logger.info("Completed writing data to the new sheet %s",
                             worksheet_name)

            no_records = len(data) - 1
            return True, no_records, column_info
        except SpreadsheetNotFound as not_found_error:
            self.logger.exception(
                "DataService - write_data_to_new_sheet: %s", not_found_error)
            raise not_found_error
        except GSpreadException as gspread_error:
            self.logger.exception(
                "DataService - write_data_to_new_sheet: %s", gspread_error)
            raise gspread_error
        except Exception as other_error:
            self.logger.exception(
                "DataService - write_data_to_new_sheet: %s", other_error)
            raise other_error

    def get_client_name(self):
        """
        Substring client name from the service account email
        Return: Client name
        """
        email = self.client.auth.service_account_email
        name = email.split('@')[0]
        return name

    def get_topic_list(self, keys):
        """
        Create the topic line for the new data sheet
        Return: list containing topic names
        """
        topic_list = []
        for key in keys:
            topic_list.append(key)
        return topic_list

    def unpack_json_list(self, client_name, data, is_new_sheet):
        """
        Unpack Json data object into a list to pass through the gspread API
        Return: column information(Note: this is only needed for new sheet) and final data list
        """
        try:
            column_info = []
            # Convert JSON array list into a list
            dict_list = data
            nested_list = [[value for value in dictionary.values()]
                           for dictionary in dict_list]

            # Append the service account name to the end of each data list
            for lst in nested_list:
                lst.append(client_name)

            if is_new_sheet:
                # Append the topic line to the beginning of the data list
                topic_line = self.get_topic_list(dict_list[0].keys())
                topic_line.append("Source")
                nested_list.insert(0, topic_line)

                # Get column info
                column_info = self.get_column_info(dict_list[0])

            return column_info, nested_list
        except Exception as error:
            self.logger.exception(
                "DataService - write_data_to_new_sheet: %s", error)
            raise error

    def get_column_info(self, data_dict):
        """
        Create a list of column information
        Return: list containing column name and data type
        """
        column_info = []
        keys = data_dict.keys()
        for key in keys:
            column_info.append([key, type(data_dict[key])])

        return column_info
