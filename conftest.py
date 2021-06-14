import pytest


@pytest.fixture()
def parent_module_import_enabled(mocker):
    yield mocker.patch(
        "django_codemod.visitors.base.REPLACE_PARENT_MODULE_IMPORTED", True
    )
