from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.model.dao.base_dao import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id_key: str, id_val: Any,
            conditions: dict = None) -> Optional[ModelType]:
        conditions[id_key] = id_val
        db_query = db.query(self.model)
        for db_field, field_val in conditions.items():
            db_query = db_query.filter(
                getattr(self.model, db_field) == field_val)
        return db_query.first()

    def get_multi(
            self, db: Session, page_no: int = 1, page_size: int = 10,
            condition_eq: dict = None, order_by: str = None,
            conditions: list = None
    ) -> List[ModelType]:
        db_query = db.query(self.model)
        if condition_eq:
            for db_field, field_val in condition_eq.items():
                if field_val:
                    db_query = db_query.filter(
                        getattr(self.model, db_field) == field_val)
        if conditions:
            db_query = db_query.filter(*conditions)
        if order_by:
            db_query.order_by(getattr(self.model, order_by))
        end = page_no * page_size
        db_query = db_query.offset(end - page_size).limit(page_size)
        return db_query.all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_insert(self, db: Session, objs: list):
        db.bulk_insert_mappings(self.model, objs, render_nulls=True)
        db.commit()

    def query_update(
            self, db: Session,
            condition_eq: dict,
            obj_in: dict,
            condition_list: list = None
    ) -> ModelType:
        db_qu = db.query(self.model)
        if condition_eq:
            for db_field, field_val in condition_eq.items():
                db_qu = db_qu.filter(getattr(self.model, db_field) == field_val)
        if condition_list:
            db_qu = db_qu.filter(*condition_list)
        result = db_qu.update(obj_in)
        db.commit()
        return result

    @staticmethod
    def update(
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id_in: int) -> ModelType:
        obj = db.query(self.model).get(id_in)
        db.delete(obj)
        db.commit()
        return obj


class PGDao(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
