#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Services for managing groups."""

from server.entities.group import GroupSummary


def search(**query) -> list[GroupSummary]:
    # Placeholder implementation
    return [GroupSummary(id=group_id) for group_id in query["id"]]
