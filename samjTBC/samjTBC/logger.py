import logging
import logging.config
from datetime import datetime


class CustomFormatter(logging.Formatter):
    # Farbdefinitionen
    COLORS = {
        'DEBUG': '\033[94m',  # Blau
        'INFO': '\033[92m',  # Grün
        'WARNING': '\033[93m',  # Gelb
        'ERROR': '\033[91m',  # Rot
        'CRITICAL': '\033[95m'  # Magenta
    }
    DARK_GREEN = '\033[32m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.WHITE)
        log_fmt = (
            f"{self.WHITE}[{record.name}]"
            f"{self.WHITE}[{self.DARK_GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{self.WHITE}]"
            f"{self.WHITE}[{log_color}{record.levelname}{self.WHITE}] "
            f"{self.WHITE}{record.getMessage()}{self.RESET}"
        )
        return log_fmt
