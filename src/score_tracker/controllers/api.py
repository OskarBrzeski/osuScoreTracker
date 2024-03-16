from typing import Final
import os

from dotenv import load_dotenv
from ossapi import Ossapi, OssapiV1

load_dotenv(".env")

_API_LEGACY_KEY: Final[str] = os.environ.get("LEGACY_OSU_API_KEY")
_API_CLIENT_ID: Final[int] = int(os.environ.get("CLIENT_ID"))
_API_CLIENT_SECRET: Final[str] = os.environ.get("CLIENT_SECRET")

API_V1 = OssapiV1(_API_LEGACY_KEY)
API = Ossapi(_API_CLIENT_ID, _API_CLIENT_SECRET)
