import logging
import traceback

from django.utils.html import strip_tags
from django.db import connection



class Log:
    @staticmethod
    def log(o: any, title: str = "") -> None:
        # Sends input logs to the "checkpoint" logger (settings).
        log = logging.getLogger("django")
        if title:
            if title == "_":
                for j in range(80):
                    title = title + "_"
            log.debug(title)

        log.debug(o)

        if title:
            log.debug(title)



    @staticmethod
    def logException(e: Exception) -> None:
        # Logs the stack trace information and the raw output if any.
        Log.log(traceback.format_exc(), 'Error')

        try:
            Log.log(e.raw, 'Raw checkpoint data')
        except Exception:
            pass



    @staticmethod
    def actionLog(o: any, user: dict = None) -> None:
        # Sends input logs to the "checkpoint" logger (settings).
        user = user or {}
        log = logging.getLogger("django")

        try:
            if "username" in user:
                log.debug("["+user['username']+"] "+o)
            else:
                log.debug(o)
        except Exception:
            pass
