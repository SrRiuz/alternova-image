# Libs
from core.db.exceptions.database import DataBaseConfigException, InvalidEngine
from core.db.constants import ALLOWED_ENGINES, POSTGRESQL_ENGINES
from core.db.exceptions.database import InvalidEngine

try:
    from core.settings import DATABASE
except ImportError:
    DATABASE = {}


def validate_database_config(config):
    required_keys = ["ENGINE", "NAME"]
    if config["ENGINE"] in POSTGRESQL_ENGINES:
        required_keys += ["USER", "PASSWORD", "HOST", "PORT"]

    for key in required_keys:
        if key not in config or not config[key]:
            raise DataBaseConfigException(
                f"The '{key}' value is required for the database configuration."
            )


def get_db_uri() -> str:
    if not DATABASE:
        return

    ENGINE = DATABASE.get("ENGINE")
    if ENGINE and ENGINE not in ALLOWED_ENGINES:
        raise InvalidEngine(f"The database engine '{ENGINE}' is not supported.")

    validate_database_config(DATABASE)

    DATABASE_URL = f"sqlite:///./{DATABASE["NAME"]}"
    if DATABASE["ENGINE"] == POSTGRESQL_ENGINES:
        DATABASE_URL = f"postgresql://{DATABASE["USER"]}:{DATABASE["PASSWORD"]}@{DATABASE["HOST"]}:{DATABASE["PORT"]}/{DATABASE["NAME"]}"

    return DATABASE_URL
