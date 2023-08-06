from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ReprMixin:
    __tablename__ = "ReprMixin"

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return 'Table %s is called by %s, data: %s' % (
            self.__tablename__, self.__class__.__name__, str(self.__dict__)
        )
