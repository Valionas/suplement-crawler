import logging
import os
from datetime import datetime
from dotenv import load_dotenv

def configure_app():
    load_dotenv()
    now = datetime.now()
    datetime_string = now.strftime("%Y%m%d-%H%M%S")
    env = os.getenv('ENVIRONMENT')

    logging.basicConfig(filename="./logs/crawler-{}-{}.log".format(datetime_string, env), encoding='utf-8',
                        level=logging.DEBUG)
