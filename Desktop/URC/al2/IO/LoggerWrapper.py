import logging
import datetime

class LoggerWrapper:
    def __init__(self, file=None, logLevel=logging.INFO, isPrintingToConsole=True):
        self.isPrintingToConsole = isPrintingToConsole
        logging.basicConfig(filename=file, level=logLevel)

    def log(self, level, msg: str):
        msg = str(datetime.datetime.now()) + ": " + msg
        logging.log(level, msg)
        if self.isPrintingToConsole:
            print(logging._levelToName[level] + ": " + msg)

    def logError(self, msg: str):
        self.log(logging.ERROR, msg)

    def logWarning(self, msg: str):
        self.log(logging.WARN, msg)

    def logInfo(self, msg: str):
        self.log(logging.INFO, msg)

    def logDebug(self, msg: str):
        self.log(logging.DEBUG, msg)