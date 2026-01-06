#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Models for User entity for client side."""

import typing as t

from datetime import datetime

from pydantic import BaseModel, Field

from .common import camel_case_config, forbid_extra_config
from .group import GroupSummary


class UserDetail(BaseModel):
    """Model for detailed User information in mAP Core API."""

    id: str
    """The unique identifier for the user."""

    eppn: list[str] = Field(default_factory=list)
    """The eduPersonPrincipalNames of the user."""

    user_name: str
    """The username of the user. Alias to 'userName'."""

    emails: list[str] = Field(default_factory=list)
    """The email addresses of the user."""

    preferred_language: t.Literal["en", "ja"] | None = None
    """The preferred language of the user. Alias to 'preferredLanguage'."""

    groups: list[GroupSummary] = Field(default_factory=list)
    """The groups the user belongs to."""

    created: datetime | None = None
    """The creation timestamp of the user."""

    last_modified: datetime | None = None
    """The last modification timestamp of the user. Alias to 'lastModified'."""

    model_config = camel_case_config | forbid_extra_config
    """Configure to use camelCase aliasing and forbid extra fields."""


class UserSummary(BaseModel):
    """Model for summary User information in mAP Core API."""

    id: str
    """The unique identifier for the user."""

    user_name: str | None = None
    """The username of the user. Alias to 'userName'."""

    email: str | None = None
    """The first email address of the user."""

    eppn: str | None = None
    """The first eduPersonPrincipalName of the user."""

    lask_modified: datetime | None = None
    """The last modification timestamp of the user. Alias to 'lastModified'."""

    model_config = camel_case_config | forbid_extra_config
    """Configure to use camelCase aliasing and forbid extra fields."""
