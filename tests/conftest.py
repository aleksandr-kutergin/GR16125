from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.main import app

load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
def db():
    """Fixture for setting up and tearing down the test database."""
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_db():
    """Fixture for mocking the database session."""
    db = MagicMock(spec=Session)
    return db


@pytest.fixture
def mock_user():
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    return mock_user


@pytest.fixture
def mock_env_variables():
    """Fixture for mocking environment variables."""
    with patch.dict("os.environ", {"SECRET_KEY": "testsecret", "ALGORITHM": "HS256"}):
        yield


@pytest.fixture
def mock_oauth2_token():
    """Fixture for a mock OAuth2 token."""
    return "mock-valid-token"


@pytest.fixture()
def client():
    """Fixture for creating the FastAPI test client."""
    return TestClient(app)
