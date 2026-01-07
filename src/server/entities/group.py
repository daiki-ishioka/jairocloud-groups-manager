#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Models for Group entity for client side."""

from datetime import datetime

from pydantic import BaseModel

from .common import camel_case_config, forbid_extra_config
from .map_group import MapGroup, MemberUser, Visibility


class GroupDetail(BaseModel):
    """Model for detailed Group information in mAP Core API."""

    id: str
    """The unique identifier for the group."""

    display_name: str
    """The display name of the group. Alias to 'displayName'."""

    public: bool | None = None
    """Whether the group is public or private."""

    member_list_visibility: Visibility | None = None
    """The visibility of the member list. Alias to 'memberListVisibility'."""

    created: datetime | None = None
    """The creation timestamp of the group."""

    last_modified: datetime | None = None
    """The last modification timestamp of the group. Alias to 'lastModified'."""

    users_count: int | None = None
    """The number of users in the group. Alias to 'usersCount'."""

    model_config = camel_case_config | forbid_extra_config
    """Configure to use camelCase aliasing and forbid extra fields."""

    @classmethod
    def from_map_group(cls, group: MapGroup) -> GroupDetail:
        """Create a GroupDetail instance from a MapGroup instance.

        Args:
            group (MapGroup): The MapGroup instance to convert.

        Returns:
            GroupDetail: The created GroupDetail instance.
        """
        return cls(
            id=group.id,
            display_name=group.display_name or "",
            public=group.public,
            member_list_visibility=group.member_list_visibility,
            created=group.meta.created if group.meta else None,
            last_modified=group.meta.last_modified if group.meta else None,
            users_count=len([
                member for member in group.members if isinstance(member, MemberUser)
            ])
            if group.members
            else 0,
        )


class GroupSummary(BaseModel):
    """Model for summary Group information in mAP Core API."""

    id: str
    """The unique identifier for the group."""

    display_name: str | None = None
    """The display name of the group. Alias to 'displayName'."""

    public: bool | None = None
    """Whether the group is public or private."""

    member_list_visibility: Visibility | None = None
    """The visibility of the member list. Alias to 'memberListVisibility'."""

    users_count: int | None = None
    """The number of users in the group. Alias to 'usersCount'."""

    model_config = camel_case_config | forbid_extra_config
    """Configure to use camelCase aliasing and forbid extra fields."""
