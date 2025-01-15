import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import init_db
from app.models import Base
from tests.conftest import engine as en


@pytest.mark.parametrize("eng", [en])
def test_database_connection(eng):
    """Test that the engine is able to connect to the database."""
    try:
        connection = en.connect()
        connection.close()
        assert True
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")


def test_init_db():
    test_db_url = "sqlite:///:memory:"
    engine = create_engine(test_db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    init_db()

    assert len(Base.metadata.tables) > 0, "No tables were created in the database"
    assert "users" in Base.metadata.tables, "Users table was not created"
