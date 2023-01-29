"""
Author: weijay
Date: 2023-01-26 16:35:30
LastEditors: weijay
LastEditTime: 2023-01-26 16:35:31
Description: 設定檔
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    playing_page = os.environ.get("PLAYING_PAGE", 5)
    comming_page = os.environ.get("COMMING_PAGE", 6)
    line_token = os.environ.get("LINE_TOKEN")
