#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Models for Repository entity for client side."""

from pydantic import BaseModel, Field, HttpUrl

from .common import camel_case_config, forbid_extra_config


class RepositoryDetail(BaseModel):
    """Model for detailed Repository information in mAP Core API."""

    id: str
    """The unique identifier for the repository."""

    display_name: str
    """The name of the repository. Alias to 'displayName'."""

    service_url: HttpUrl | None = None
    """The URL of the service. Alias for 'serviceUrl'."""

    suspended: bool | None = None
    """Whether the service is suspended."""

    sp_connecter_id: str | None = None
    """The SP Connecter ID of the repository. Alias to 'spConnecterId'."""

    entity_id: list[str] = Field(default_factory=list)
    """The entity IDs associated with the repository. Alias to 'entityID'."""

    users_count: int | None = None
    """The number of users in the group. Alias to 'usersCount'."""

    groups_count: int | None = None
    """The number of groups in the repository. Alias to 'groupsCount'."""

    model_config = camel_case_config | forbid_extra_config
    """Configure to use camelCase aliasing and forbid extra fields."""


class RepositorySummary(BaseModel):
    """Model for summary Repository information in mAP Core API."""

    id: str
    """The unique identifier for the repository."""

    display_name: str | None = None
    """The name of the repository. Alias to 'displayName'."""

    service_url: HttpUrl | None = None
    """The URL of the service. Alias for 'serviceUrl'."""

    sp_connecter_id: str | None = None
    """The SP Connecter ID of the repository. Alias to 'spConnecterId'."""

    model_config = camel_case_config | forbid_extra_config
    """Configure to use camelCase aliasing and forbid extra fields."""
