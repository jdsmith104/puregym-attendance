import puregym
import json
import logging
import time
import os
import sys
import datetime

TARGET_GYM_IDS = [339, 286, 296, 168, 120, 222, 129]
POLL_INTERVAL = 27
HEADER="datetime,"+",".join(map(str, TARGET_GYM_IDS))
LOG_LEVEL = logging.INFO

def main(email: str, pin: str, logger: logging.Logger):
    
    client = puregym.PuregymAPIClient()
    client.login(email, pin)

    run = True

    logger.debug(HEADER)

    while run:
        try:
            all_attendance = [str(client.get_gym_attendance(gym_id)) for gym_id in TARGET_GYM_IDS]
            logline = datetime.datetime.now().isoformat()+","+",".join(all_attendance)
            logger.info(logline)

            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print('\nStopping server')
            try:
                sys.exit(130)
            except SystemExit:
                os._exit(130)

def setup_logging() -> logging.Logger:
    logging.basicConfig(filename="logs/log_"+time.strftime("%Y%m%d-%H%M%S"),
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=LOG_LEVEL)

    return logging.getLogger('PUREGYM_ATTENDANCE_SCRAPER')

if __name__ == "__main__":
    print("running server")

    logger = setup_logging()

    with open("credentials.json", "r") as f:
        credentials = json.load(f)
    
    email = credentials.get("email")
    pin = credentials.get("pin")
    logger.debug(f"Credentials email={email} pin={pin}")

    main(email, pin, logger)
