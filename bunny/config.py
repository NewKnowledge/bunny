from datetime import datetime, timezone, timedelta
import os

# Task Config
BROKER_URL = os.environ.get('REDIS_BROKER_URL', 'redis://localhost:6379/0')

# Time Config
OLD_WINDOW_LENGTH = timedelta(days=30)
NEW_WINDOW_LENGTH = timedelta(hours=1)
CURRENT_HOUR = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
PIVOT_TIME = CURRENT_HOUR - NEW_WINDOW_LENGTH
OLD_WINDOW_BEGINNING = PIVOT_TIME - OLD_WINDOW_LENGTH
OLD_WINDOW_END = NEW_WINDOW_BEGINNING = PIVOT_TIME
NEW_WINDOW_END = CURRENT_HOUR

# Snowflake Config
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT', None)
SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER', None)
SNOWFLAKE_PASS = os.environ.get('SNOWFLAKE_PASS', None)
SNOWFLAKE_NAME = os.environ.get('SNOWFLAKE_NAME', None)
SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_NAME', None)
SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE', None)
SNOWFLAKE_ROLE = os.environ.get('SNOWFLAKE_ROLE', None)
SNOWFLAKE_CONFIG = {
    "user": SNOWFLAKE_USER,
    "password": SNOWFLAKE_PASS,
    "account": SNOWFLAKE_ACCOUNT,
    "name": SNOWFLAKE_NAME,
    "schema": SNOWFLAKE_SCHEMA,
    "warehouse": SNOWFLAKE_WAREHOUSE,
    "role": SNOWFLAKE_ROLE,
    "paramstyle": "qmark",
    "query_tag": "bunny"
}
