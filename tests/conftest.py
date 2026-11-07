import pytest
from app import create_app


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test_expenses.sqlite"
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "DATABASE": str(database),
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
