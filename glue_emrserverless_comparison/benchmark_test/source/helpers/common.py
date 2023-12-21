import logging

def get_logger(log_name):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)  # so we see logged messages in console when debugging
    file_handler = logging.FileHandler(f"log/{log_name}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger