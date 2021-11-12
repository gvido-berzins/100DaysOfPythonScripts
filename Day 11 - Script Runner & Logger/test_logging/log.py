#!/usr/bin/env python3.9
import logging
import random

FAIL_LOG_FILE = "fail.log"
PASS_LOG_FILE = "pass.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%d-%m %H:%M",
    filename="main.log",
    filemode="w",
)

formatter = logging.Formatter(
    fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%d-%m %H:%M"
)

fail_handler = logging.FileHandler(FAIL_LOG_FILE)
fail_handler.setLevel(logging.CRITICAL)
fail_handler.setFormatter(formatter)

pass_handler = logging.FileHandler(PASS_LOG_FILE)
pass_handler.setLevel(logging.INFO)
pass_handler.setFormatter(formatter)
pass_logger = logging.getLogger('pass')
pass_logger.addHandler(pass_handler)


# logging.getLogger("").addHandler(pass_handler)
logging.getLogger("").addHandler(fail_handler)

logger = logging.getLogger("")
logger.propagate = False

for i in range(100):
    logger.debug(f"Iteration {i} START.")

    if random.choice([0, 1]):
        logger.critical("Return status is 1")
    else:
        pass_logger.info("Return status is 0")

    logger.debug(f"Iteration {i} END.")
