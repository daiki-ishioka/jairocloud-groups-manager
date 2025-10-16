from typing import Literal

from const import MAP_ERROR_SCHEMA
from schema.base import BaseModel


class MapError(BaseModel):
    """An error response entity in mAP API."""

    schemas: list[str] = [MAP_ERROR_SCHEMA]
    """Schema URIs that define the attributes present in the Error resource."""

    status: Literal[
        "307",
        "308",
        "400",
        "401",
        "403",
        "404",
        "409",
        "412",
        "413",
        "415",
        "500",
        "501",
    ]
    """The HTTP status code of the error as a string."""

    scim_type: Literal[
        "invalidFilter",
        "tooMany",
        "uniqueness",
        "mutability",
        "invalidValue",
        "invalidSyntax",
        "noTarget",
        "invalidValue",
        "invalidVers",
        "sensitive",
    ]
    """The SCIM error type. Alias to 'scimType'."""

    detail: str
    """A detailed description of the error."""

    error_code: int | None = None
    """An error response code. Alias to 'errorCode'."""
