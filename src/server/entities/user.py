#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Models for User entity for client side."""

import typing as t

from datetime import datetime

from pydantic import BaseModel

from .common import camel_case_config, forbid_extra_config
from .group import GroupSummary


if t.TYPE_CHECKING:
    from .map_user import MapUser


class UserDetail(BaseModel):
    """Model for detailed User information in mAP Core API."""

    id: str
    """The unique identifier for the user."""

    eppn: list[str] | None = None
    """The eduPersonPrincipalNames of the user."""

    user_name: str
    """The username of the user. Alias to 'userName'."""

    emails: list[str] | None = None
    """The email addresses of the user."""

    preferred_language: t.Literal["en", "ja"] | None = None
    """The preferred language of the user. Alias to 'preferredLanguage'."""

    groups: list[GroupSummary] | None = None
    """The groups the user belongs to."""

    created: datetime | None = None
    """The creation timestamp of the user."""

    last_modified: datetime | None = None
    """The last modification timestamp of the user. Alias to 'lastModified'."""

    model_config = camel_case_config | forbid_extra_config
    """Configure to use camelCase aliasing and forbid extra fields."""

    @classmethod
    def from_map_user(cls, user: MapUser) -> UserDetail:
        """Create a UserDetail instance from a MapUser instance.

        Args:
            user (MapUser): The MapUser instance to convert.

        Returns:
            UserDetail: The created UserDetail instance.
        """
        from server.services import groups  # noqa: PLC0415

        resolved_groups: list[GroupSummary] = []
        if user.groups:
            group_ids = [group.value for group in user.groups]
            resolved_groups = groups.search(id=group_ids)

        return cls(
            id=user.id,
            eppn=[eppn.value for eppn in user.edu_person_principal_names or []],
            user_name=user.user_name or "",
            emails=[email.value for email in user.emails or []],
            preferred_language=user.preferred_language,
            groups=resolved_groups,
            created=user.meta.created if user.meta else None,
            last_modified=user.meta.last_modified if user.meta else None,
        )


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
