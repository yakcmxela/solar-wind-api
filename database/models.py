from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, UUID, Float
from sqlalchemy.orm import relationship

Base = declarative_base()


class Incentive(Base):
    __tablename__ = "incentives"

    id = Column(UUID, primary_key=True, index=True)
    type = Column(String(20))
    display_name = Column(String(60))

    products = relationship("Product", back_populates="type")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    efficiency_max = Column(Float, nullable=True)
    efficiency_min = Column(Float, nullable=True)
    brand = Column(String(60), nullable=True)
    height = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    type_id = Column(UUID, ForeignKey("incentives.id"))

    type = relationship("Incentive", back_populates="products")
