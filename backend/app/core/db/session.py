from app.core.config import get_settings
from app.core.db.postgres.engine import Base
# Strategy Pattern: Expose the correct database session dependency based on config
settings = get_settings()

if settings.DB_ENGINE == "sqlite":
    from app.core.db.sqlite.engine import get_sqlite_db_session as get_db_session
else:
    from app.core.db.postgres.engine import get_db_session

__all__ = ["get_db_session", "Base"]
