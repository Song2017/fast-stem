from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

engine = create_engine(
    "AppConf.PG_DATABASE_URI",
    pool_pre_ping=True,
    poolclass=NullPool,
    connect_args={
        'connect_timeout': 10,
        "application_name": "PG Driver"
    },
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
