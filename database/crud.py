from sqlalchemy.orm import Session

from . import models


def get_incentives(db: Session):
    return db.query(models.Incentive).all()

def get_incentives_by_id(db: Session, incentive_id: list[str]):
    return db.query(models.Incentive).filter(models.Incentive.id.in_(incentive_id)).all()


def get_incentive(db: Session, type_id: str):
    return db.query(models.Incentive).filter(models.Incentive.type == type_id).first()


def get_products_by_type_id(db: Session, type_id: str):
    return db.query(models.Product).filter(models.Product.type_id == type_id).all()


def get_products_by_type(db: Session, type: str):
    return db.query(models.Product).filter(models.Product.type == type).all()


def get_product_by_id(db: Session, product_id: str):
    return db.query(models.Product).filter(models.Product.id == product_id).first()
