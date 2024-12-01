from sqlmodel import create_engine
from .secrets import settings

ENGINE = create_engine(
    f'mysql+pymysql://{settings.USER}:{settings.PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE}',
    # f"sqlite:///test.db"
    echo=True
)
