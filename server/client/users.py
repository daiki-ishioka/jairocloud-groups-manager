import time
import traceback

import requests
from flask import current_app
from pydantic import TypeAdapter
from pydantic_core import ValidationError


from config import config
from const import MAP_EXIST_EPPN_ENDPOINT

from client.utils import compute_signature

from schema.map_user import MapUser
from schema.map_error import MapError

ExixtEppnResponse = MapUser | MapError


def exixt_eppn(eppn: str, *, access_token: str, client_secret: str) -> bool:
    """Check if the given ePPN exists in mAP Core."""
    time_stamp = str(int(time.time()))

    signature = compute_signature(client_secret, access_token, time_stamp)

    try:
        response = requests.get(
            f"{config.MAP_CORE_BASE_URL}{MAP_EXIST_EPPN_ENDPOINT}/{eppn}",
            params={
                "time_stamp": time_stamp,
                "signature": signature,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        if 400 < response.status_code:
            response.raise_for_status()
        data = response.json()
    except requests.HTTPError, requests.JSONDecodeError:
        current_app.logger.error(f"Failed to check ePPN existence for {eppn}.")
        traceback.print_exc()
        raise

    try:
        result = TypeAdapter(ExixtEppnResponse).validate_python(data, extra="ignore")
    except ValidationError:
        current_app.logger.error("Received invalid ePPN existence response.")
        traceback.print_exc()
        raise

    return isinstance(result, MapUser)
