"""
Controller for authentication handling
"""

import logging
from fastapi import status
from gspread.exceptions import GSpreadException
from app.services.authenticate_service import AuthenticateService


class AuthenticateController:
    """
    Authentication Controller
    """

    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__)

    def authenticate_user(self):
        """
        Authenticate user
        Return: client object
        """
        try:
            res = AuthenticateService(self.path).authorize()
            if res is not None:
                self.logger.info("Gspread authentication successful")
                return res, status.HTTP_200_OK
        except GSpreadException as error:
            self.logger.error(
                "Error authenticating the user with gspread: %s", error)
            return {'Error authenticating the user with gspread':
                    str(error)}, status.HTTP_400_BAD_REQUEST
