#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Provides informational log messages used in the server application."""

from .base import LogMessage


REQUEST_FOR_AUTH_CODE = LogMessage(
    "I000",
    "Please authenticate at the following URL to issue an access token: %(url)s",
)

SUCCESS_ISSUE_TOKEN = LogMessage(
    "I001",
    "Successfully issued access token for the mAP Core API.",
)

SUCCESS_REFRESH_TOKEN = LogMessage(
    "I002",
    "Successfully refreshed access token for the mAP Core API.",
)
