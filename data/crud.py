from sqlalchemy.orm import Session

from . import models

def get_solar_panels(db: Session):
    return db.query(models.Product).filter(models.Product.type == models.IncentiveType.solar_panel).all()

def get_wind_turbines(db: Session):
    return db.query(models.Product).filter(models.Product.type == models.IncentiveType.wind_turbine).all()