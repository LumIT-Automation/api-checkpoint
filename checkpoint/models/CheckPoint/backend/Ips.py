from checkpoint.helpers.ApiSupplicant import ApiSupplicant
from checkpoint.helpers.Log import Log

class Ips:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################


    @staticmethod
    def info(sessionId: str, assetId: int) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-ips-status",
                data={}
            )
        except Exception as e:
            raise e



    @staticmethod
    def runUpdate(sessionId: str, assetId: int, data: dict = None) -> dict:
        data = data or {}

        try:
            return  ApiSupplicant(sessionId, assetId).post(
                urlSegment="run-ips-update",
                data=data
            )
        except Exception as e:
            raise e



    @staticmethod
    def updateScheduleInfo(sessionId: str, assetId: int) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="show-ips-update-schedule",
                data={}
            )
        except Exception as e:
            raise e



    @staticmethod
    def updateScheduleModify(sessionId: str, assetId: int, data: dict) -> dict:
        try:
            return ApiSupplicant(sessionId, assetId).post(
                urlSegment="set-ips-update-schedule",
                data=data
            )
        except Exception as e:
            raise e
