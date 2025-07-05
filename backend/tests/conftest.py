import pytest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test module."""
    app = create_app(TestConfig)
    yield app

@pytest.fixture(scope='module')
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()

@pytest.fixture(scope='module')
def init_database(test_app):
    """Create the database and the database table."""
    with test_app.app_context():
        db.create_all()
        yield db
        db.drop_all() 