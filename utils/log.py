import datetime
import logging
import os
import re
import sys


class MultiprocessHandler(logging.FileHandler):
    """
    A custom log handler that supports log file rotation based on time intervals.

    Args:
        filename (str): The base name of the log file.
        when (str, optional): The time interval for log rotation ('S', 'M', 'H', 'D'). Defaults to 'D'.
        backupCount (int, optional): The number of backup files to keep. Defaults to 0.
        encoding (str, optional): The encoding used for the log file. Defaults to None.
        delay (bool, optional): If True, the log file is not opened until the first emit call. Defaults to False.
    """

    def __init__(self, filename, when="D", backupCount=0, encoding=None, delay=False):
        self.prefix = filename
        self.backupCount = backupCount
        self.when = when.upper()
        self.extMath = r"^\d{4}-\d{2}-\d{2}"

        # Define supported time intervals and their corresponding format strings
        self.when_dict = {
            "S": "%Y-%m-%d-%H-%M-%S",
            "M": "%Y-%m-%d-%H-%M",
            "H": "%Y-%m-%d-%H",
            "D": "%Y-%m-%d",
        }

        self.suffix = self.when_dict.get(when)
        if not self.suffix:
            print(f"The specified date interval unit is invalid: {self.when}")
            sys.exit(1)

        # Construct the full path for the log file
        self.filefmt = os.path.join(".", "logs", f"{self.prefix}-{self.suffix}.log")
        self.filePath = datetime.datetime.now().strftime(self.filefmt)

        # Ensure the log directory exists
        self._ensure_log_directory()

        # Initialize the parent FileHandler with the constructed file path
        super().__init__(self.filePath, "a+", encoding, delay)

    def _ensure_log_directory(self):
        """Ensure the log directory exists."""
        _dir = os.path.dirname(self.filefmt)
        try:
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        except Exception as e:
            print(f"Failed to create log directory: {e}")
            print(f"log_path: {self.filePath}")
            sys.exit(1)

    def should_change_file_to_write(self):
        """Determine if the log file needs to be rotated."""
        _filePath = datetime.datetime.now().strftime(self.filefmt)
        return _filePath != self.filePath

    def do_change_file(self):
        """Rotate the log file."""
        self.baseFilename = os.path.abspath(self.filePath)
        if self.stream:
            self.stream.close()
            self.stream = None

        if not self.delay:
            self.stream = self._open()
        if self.backupCount > 0:
            for s in self.get_files_to_delete():
                try:
                    os.remove(s)
                except FileNotFoundError:
                    pass

    def get_files_to_delete(self):
        """Get a list of log files to delete based on the backup count."""
        dir_name, _ = os.path.split(self.baseFilename)
        file_names = os.listdir(dir_name)
        result = []
        prefix = self.prefix + "-"
        for file_name in file_names:
            if file_name.startswith(prefix):
                suffix = file_name[len(prefix) : -4]
                if re.match(self.extMath, suffix):
                    result.append(os.path.join(dir_name, file_name))
        result.sort()

        if len(result) <= self.backupCount:
            return []
        else:
            return result[: len(result) - self.backupCount]

    def emit(self, record):
        """Emit a log record."""
        try:
            if self.should_change_file_to_write():
                self.do_change_file()
            super().emit(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


def write_log(log_name, log_num=7, console_level=logging.INFO, file_level=logging.DEBUG):
    """
    Configure and return a logger instance.

    Args:
        log_name (str): The base name of the log file.
        log_num (int, optional): The number of backup log files to keep. Defaults to 7.
        console_level (int, optional): The logging level for console output. Defaults to logging.INFO.
        file_level (int, optional): The logging level for file output. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s ｜ %(levelname)s ｜ %(filename)s ｜ %(funcName)s ｜ %(lineno)s ｜ %(message)s")

    # Add console handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(console_level)
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    # Add file handler with log rotation
    file_handler = MultiprocessHandler(log_name, when="D", backupCount=log_num, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(fmt)
    file_handler.do_change_file()
    logger.addHandler(file_handler)

    return logger


logger = write_log(log_name="agent")
