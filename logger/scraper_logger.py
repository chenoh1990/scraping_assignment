import logging
import os


class Logger:
    """
    Logger class to manage logging for different scrapers.
    """
    loggers = {}

    @staticmethod
    def get_logger(name: str, log_file: str, level=logging.INFO):
        """
        Returns a logger instance. Ensures each logger is created only once per log file.
        """

        if name in Logger.loggers:
            return Logger.loggers[name]  # Return existing logger if already created.

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)  # Create log directory if it does not exist.

        # Create a new logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Prevent adding multiple handlers to the same logger
        if not logger.handlers:
            # Define log format
            log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            # Create file handler
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(log_format)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(log_format)

            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        # Store logger instance to prevent duplicates
        Logger.loggers[name] = logger
        return logger
