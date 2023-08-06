"""
Factory that configures SQLAlchemy for PostgreSQL.

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from microcosm.api import binding, defaults


@binding("postgres")
@defaults(
    host="localhost",
    port=5432,
    database_name=None,
    username=None,
    # the default password; should be change in any non-trivial environment
    password="secret",
    # the size of the connection pool; 5 is the default
    driver="postgresql",
    pool_size=5,
    # the timeout waiting for a connection from the pool; 30 is the default and much too large
    pool_timeout=2,
    # the number of extra connections over/above the pool size; 10 is the default
    max_overflow=10,
    # echo all SQL
    echo=False,
)
def configure_sqlalchemy_engine(graph):
    """
    Create the SQLAlchemy engine.

    """
    # use different database name for testing
    if graph.config.postgres.database_name is not None:
        # we expect to use a database name driven by conventions, but allow configuration
        database_name = graph.config.postgres.database_name
    elif graph.metadata.testing:
        database_name = "{}_test_db".format(graph.metadata.name)
    else:
        database_name = "{}_db".format(graph.metadata.name)

    if graph.config.postgres.username is not None:
        username = graph.config.postgres.username
    else:
        # use the metadata name as the username
        username = graph.metadata.name

    password = graph.config.postgres.password or ""

    uri = "{}://{}:{}@{}:{}/{}".format(
        graph.config.postgres.driver,
        username,
        password,
        graph.config.postgres.host,
        graph.config.postgres.port,
        database_name,
    )

    return create_engine(
        uri,
        pool_size=graph.config.postgres.pool_size,
        pool_timeout=graph.config.postgres.pool_timeout,
        max_overflow=graph.config.postgres.max_overflow,
        echo=bool(graph.config.postgres.echo),
    )


def configure_sqlalchemy_sessionmaker(graph):
    """
    Create the SQLAlchemy session class.

    """
    return sessionmaker(bind=graph.postgres)
