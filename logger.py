from datetime import datetime

debug_level = "DEBUG"
info_level = "INFO"
warn_level = "WARN"
error_level = "ERROR"

levels = {
    debug_level: 0,
    info_level: 1,
    warn_level: 2,
    error_level: 3,
}

class Logger:
    def __init__(self, level=info_level):
        if level not in levels.keys():
            raise Exception(f"log level {level} is unknown")
        self.level = level


    def _print(self, msg: str, level: str):
        if levels[level] < levels[self.level]:
            return
        print(f"{level} at {str(datetime.now())}: {msg}")


    def debug(self, msg: str):
        self._print(msg, debug_level)


    def info(self, msg: str):
        self._print(msg, info_level)


    def warn(self, msg: str):
        self._print(msg, warn_level)


    def error(self, msg: str):
        self._print(msg, error_level)
