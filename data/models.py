from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, UUID, Float
from sqlalchemy.orm import relationship

Base = declarative_base()

class Incentive(Base):
    __tablename__ = "incentives"

    id = Column(UUID, primary_key=True, index=True)
    type = Column(String(20), index=True)
    display_name = Column(String(60))

    products = relationship("Product", back_populates="type")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    website = Column(String)

    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID, primary_key=True, index=True)
    brand_id = Column(UUID, ForeignKey("brands.id"))
    diameter = Column(Float, nullable=True)
    efficiency = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    name = Column(String)
    width = Column(Float, nullable=True)
    type_id = Column(UUID, ForeignKey("incentives.id"))

    brand = relationship("Brand", back_populates="products")
    type = relationship("Incentive", back_populates="products")
