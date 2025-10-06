import pytest

import const


@pytest.fixture(autouse=True)
def set_test_constants():
    const.MAP_USER_SCHEMA = "urn:ietf:params:scim:schemas:mace:example.jp:core:2.0:User"
    const.MAP_GROUP_SCHEMA = "urn:ietf:params:scim:schemas:mace:example.jp:core:2.0:Group"
    const.MAP_SERVICE_SCHEMA = "urn:ietf:params:scim:schemas:mace:example.jp:core:2.0:Service"
