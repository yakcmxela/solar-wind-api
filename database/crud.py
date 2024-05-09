from sqlalchemy.orm import Session

from . import models


def get_incentives(db: Session):
    return db.query(models.Incentive).all()


def get_incentive(db: Session, type_id: str):
    return db.query(models.Incentive).filter(models.Incentive.type == type_id).first()


def get_products(db: Session, type_id: str):
    return db.query(models.Product).filter(models.Product.type_id == type_id).all()


def get_product_by_id(db: Session, product_id: str):
    return db.query(models.Product).filter(models.Product.id == product_id).first()
