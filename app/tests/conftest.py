import pytest
import sys
import os

# Ajouter le répertoire parent au path pour importer app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def app_fixture():
    app.config.update({"TESTING": True, "DEBUG": False})

    yield app


@pytest.fixture
def client(app_fixture):
    return app_fixture.test_client()
