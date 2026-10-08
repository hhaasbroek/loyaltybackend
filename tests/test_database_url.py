import pytest
from sqlalchemy.engine import make_url

from app.core.config import Settings


@pytest.mark.parametrize(
    "raw",
    [
        "postgres://u:p@host:5432/db",  # what some platforms hand out
        "postgresql://u:p@host:5432/db",  # what Railway hands out
    ],
)
def test_bare_postgres_urls_use_the_installed_psycopg2_driver(raw):
    url = Settings(DATABASE_URL=raw).DATABASE_URL
    assert url == "postgresql+psycopg2://u:p@host:5432/db"
    # Regression guard: SQLAlchemy 2.1 made a bare postgresql:// resolve to the psycopg (v3)
    # driver, which isn't installed, and the backend crashed on startup.
    assert make_url(url).get_dialect().driver == "psycopg2"


def test_explicit_driver_choice_is_respected():
    raw = "postgresql+psycopg://u:p@host/db"
    assert Settings(DATABASE_URL=raw).DATABASE_URL == raw


def test_sqlite_url_is_untouched():
    assert Settings(DATABASE_URL="sqlite:///./x.db").DATABASE_URL == "sqlite:///./x.db"
