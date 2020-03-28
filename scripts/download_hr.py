import logging
import os
import re

import dateutil
import pandas as pd
import requests

from utils import _COLUMNS_ORDER, COVIDScrapper, get_response

logging.basicConfig()
logger = logging.getLogger("covid-eu-data.download.hr")

REPORT_URL = "https://www.koronavirus.hr/en"
REPORT_IN_HR_URL = "https://www.koronavirus.hr"
CACHE_FOLDER = os.path.join("cache", "daily", "hr")

def cache_page(url, name):
    req = get_response(url)

    # 28.03.2020. 09:00</span>
    content =req.content.decode(req.apparent_encoding)
    re_dt = re.compile(r"(\d+.\d+.\d+. \d+:\d+)</span>")
    dt = re_dt.findall(content)[0]
    # parse dt
    dt = dateutil.parser.parse(dt).isoformat()
    logger.info(f"found datetime: {dt}")
    # save page

    if not os.path.exists(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)
        logger.info(f"Created folder {CACHE_FOLDER}")

    save_path = os.path.join(CACHE_FOLDER, f"{dt}__{name}.html")

    with open(save_path, 'wb') as f:
        f.write(req.content)


if __name__ == "__main__":

    cache_page(REPORT_URL, "en__koronavirus.hr")
    cache_page(REPORT_IN_HR_URL, "hr__koronavirus.hr")
    logger.info("End of Game")
