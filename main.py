from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import models, crud, database

from internal.ai import RenewableAI
from internal.weather import WeatherAPI

models.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost:3000",
]

ai = RenewableAI()
weather = WeatherAPI()
app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/incentives/")
async def get_incentives(
    city: str,
    state: str,
    categories: str,
):
    response = await ai.get_incentives(
        location=f"{city} {state}", categories=categories.split(",")
    )
    return {"response": response}


@app.get("/incentives/types/")
async def get_incentive_types(db: Session = Depends(get_db)):
    incentives = crud.get_incentives(db)
    return {"response": incentives}


@app.post("/estimates/")
async def get_estimates(
    lat: float,
    lng: float,
    solar_panel_area: float,
    solar_product_id: str,
    wind_product_id: str,
    wind_turbine_count: int,
    db: Session = Depends(get_db),
):
    solar_product = crud.get_product_by_id(db, solar_product_id)
    wind_product = crud.get_product_by_id(db, wind_product_id)
    weather_data = await weather.get_weather_by_coords(lat, lng)

    response = await ai.get_estimates(
        solar_panel_area=solar_panel_area,
        solar_product=solar_product,
        solar_radiation=weather_data["solar_radiation"],
        wind_product=wind_product,
        wind_speed_average=weather_data["wind_speed"],
        wind_turbine_count=wind_turbine_count,
    )
    return {"response": response}


@app.get("/installers/")
async def get_installers_by_type(
    city: str, state: str, type: str, db: Session = Depends(get_db)
):
    incentive = crud.get_incentive(db, type)
    response = await ai.get_installers(incentive, f"{city} {state}")
    return {"response": response}


@app.get("/products/type_id/{type_id}/")
def get_products_by_type_id(type_id: str, db: Session = Depends(get_db)):
    print(type_id)
    products = crud.get_products_by_type_id(db, type_id)
    return {"response": products}


@app.get("/products/type/{type}/")
def get_products_by_type(type: str, db: Session = Depends(get_db)):
    products = crud.get_products_by_type(db, type)
    return {"response": products}
