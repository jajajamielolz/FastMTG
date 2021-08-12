import os  # noqa!
import sys  # noqa!

sys.path.append(os.getcwd())  # noqa
from logging.config import fileConfig  # noqa!
from sqlalchemy import engine_from_config  # noqa!
from sqlalchemy import pool  # noqa!
from alembic import context  # noqa!
from alembic.config import Config  # noqa!
from app.config import DB_FILE  # noqa!
from app.utils.env_utils import load_environment  # noqa!

# import the model files is all that is needed to take them into account during autogeneration
from models.core.base import Base  # noqa!

load_environment()


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_ini_path = "alembic.ini"
dsn = "sqlite:///" + DB_FILE


def setup(script_location: str, dsn: str):
    print(
        f"Running DB migrations in {script_location} on {dsn} (environment: {os.environ.get('ENVIRONMENT')})"
    )
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    return alembic_cfg


config = setup("alembic:versions", dsn)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
