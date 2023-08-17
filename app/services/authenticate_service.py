"""
Methods related to authentication with gspread.
"""
import logging
import gspread
from gspread.exceptions import GSpreadException
from google.oauth2 import service_account

# Scope defines the rquired APIs(i.e. google drive & spreadsheet)s
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class AuthenticateService():
    """
    Authentication Service
    """

    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__)

    def authorize(self):
        """
        Validate and create auth token using the credentials in the file.
        """
        try:
            creds = None
            # Read credentials.json file to autheticate the user and create client object
            creds = service_account.Credentials.from_service_account_file(
                filename=self.path, scopes=SCOPES)
            client = gspread.authorize(creds)
            self.logger.info("Authentication successful.")
            return client
        except GSpreadException as gspread_error:
            self.logger.exception("AuthenticateService - authorize: %s", gspread_error)
            raise gspread_error
        