import logging
from pythonjsonlogger import jsonlogger


def get_logger(name=__name__):
    """
    📝 Returns a logger configured with JSON formatting and emoji support.
    """
    # 🔍 Get or create logger instance with given name
    logger = logging.getLogger(name)

    # ⚡ Only add handler if none exist to avoid duplicates
    if not logger.handlers:
        # 🖥️ Create console handler for output
        console_handler = logging.StreamHandler()

        # ✅ Use json_ensure_ascii=False for emoji/unicode support
        # 🎨 Configure JSON formatter with timestamp, name, level and message
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            json_ensure_ascii=False  # 👈 Correct way to allow emoji output
        )

        # 🔗 Connect formatter to handler and handler to logger
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # ℹ️ Set default logging level to INFO
        logger.setLevel(logging.INFO)

    # ✨ Return configured logger
    return logger
