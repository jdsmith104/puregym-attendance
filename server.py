from requests import HTTPError
import puregym
import json
import logging
import time
import os
import sys
import datetime

TARGET_GYM_IDS = [339, 286, 296, 168, 120, 222, 129, 49]
POLL_INTERVAL = 270
HEADER = "datetime,"+",".join(map(str, TARGET_GYM_IDS))
LOG_LEVEL = logging.INFO
LOG_DIR = "logs"


def setup_logging() -> logging.Logger:
    # Create directory for logs if it does not exist
    logfile_path = LOG_DIR+"/log_"+time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(os.path.dirname(logfile_path), exist_ok=True)

    logging.basicConfig(filename=logfile_path,
                        filemode='a',
                        format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=LOG_LEVEL)

    return logging.getLogger('PUREGYM_ATTENDANCE_SCRAPER')


def login(client, email, pin):
    client.login(email, pin)


def get_attendance(client) -> list[str]:
    return [str(client.get_gym_attendance(gym_id)) for gym_id in TARGET_GYM_IDS]


def log(logger, attendance):
    logline = datetime.datetime.now().isoformat()+","+",".join(attendance)
    logger.info(logline)


def run(email: str, pin: str, logger: logging.Logger):
    run = True
    # setup client
    client = puregym.PuregymAPIClient()
    logger.info(HEADER)
    # Loop
    while run:
        try:
            # auth
            login(client, email, pin)

            if client.authed:
                # get data
                all_attendance = get_attendance(client)

                # log
                log(logger, all_attendance)
            else:
                logger.error("\nClient not authed")

            # wait
            time.sleep(POLL_INTERVAL)
        except HTTPError as e:
            logger.error(f"{e} and response={e.response}")
            time.sleep(POLL_INTERVAL*3)
        except ConnectionError as e:
            logger.error(f"{e} and response={e.response}")
            time.sleep(POLL_INTERVAL*3)

        except KeyboardInterrupt:
            logger.info('\nStopping server')
            run = False
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)


if __name__ == "__main__":
    print("running server")

    # Get credentials from env
    with open("credentials.json", "r") as f:
        credentials = json.load(f)

    email = credentials.get("email")
    pin = credentials.get("pin")

    logger = setup_logging()
    logger.debug(f"Credentials email={email} pin={pin}")

    run(email, pin, logger)
