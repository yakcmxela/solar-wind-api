from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from data import models, crud, database

from internal.ai import RenewableAI

models.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost:3000",
]

ai = RenewableAI()
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


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/solar/installers/{location}")
async def get_solar_potential(solarradiation: str, area: float):
    response = await ai.calculate_solar_potential(
        solarradiation=solarradiation, area=area
    )
    return {"response": response}


@app.get("/solar/panels")
def get_solar_panels(db: Session = Depends(get_db)):
    solar_panels = crud.get_solar_panels(db)
    return {"response": solar_panels}


@app.get("/incentives/")
async def get_incentives(
    city: str,
    state: str,
    categories: str,
):
    response = await ai.get_incentives(
        location=f"{city} {state}", categories=categories.split(",")
    )
    return {"response": response}
