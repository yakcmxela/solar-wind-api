"""create brands and products

Revision ID: b4b53a195196
Revises: 5859b3f32836
Create Date: 2024-05-09 09:55:36.660348

"""

from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b4b53a195196"
down_revision: Union[str, None] = "5859b3f32836"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

brands = [
    {"id": uuid.uuid4(), "name": "SunPower", "website": "https://www.sunpower.com/"},
    {"id": uuid.uuid4(), "name": "LG", "website": "https://www.lg.com/"},
    {"id": uuid.uuid4(), "name": "Panasonic", "website": "https://na.panasonic.com/"},
    {"id": uuid.uuid4(), "name": "REC", "website": "https://usa.recgroup.com/"},
    {
        "id": uuid.uuid4(),
        "name": "Canadian Solar",
        "website": "https://www.canadiansolar.com/",
    },
    {
        "id": uuid.uuid4(),
        "name": "Trina Solar",
        "website": "https://www.trinasolar.com/us",
    },
    {"id": uuid.uuid4(), "name": "JinkoSolar", "website": "https://jinkosolar.us/"},
    {"id": uuid.uuid4(), "name": "LONGi Solar", "website": "https://www.longi.com/us/"},
    {
        "id": uuid.uuid4(),
        "name": "Hanwha Q CELLS",
        "website": "https://www.hanwha.com/en.html/",
    },
    {
        "id": uuid.uuid4(),
        "name": "Talesun Solar",
        "website": "https://www.talesun.com/",
    },
]

products = [
    {
        "id": uuid.uuid4(),
        "name": "X-Series",
        "diameter": 22.8,
        "efficiency": 1046,
        "height": 1559,
        "width": 0,
        "brand_id": "",
        "type_id": "",
    },
    {
        "id": uuid.uuid4(),
        "name": "NeON R",
        "diameter": 22.0,
        "efficiency": 1026,
        "height": 1760,
        "width": 0,
        "brand_id": "",
        "type_id": "",
    },
    {
        "id": uuid.uuid4(),
        "name": "HIT",
        "diameter": 21.7,
        "efficiency": 1053,
        "height": 1575,
        "width": 0,
        "brand_id": "",
        "type_id": "",
    },
    {
        "id": uuid.uuid4(),
        "name": "Alpha Series",
        "diameter": 21.7,
        "efficiency": 1690,
        "height": 1000,
        "width": 0,
        "brand_id": "",
        "type_id": "",
    },
    {
        "id": uuid.uuid4(),
        "name": "HiKu",
        "diameter": 21.6,
        "efficiency": 1700,
        "height": 992,
        "width": 0,
        "brand_id": "",
        "type_id": "",
    },
    {
        "id": uuid.uuid4(),
        "name": "Vertex",
        "diameter": 21.2,
        "efficiency": 2175,
        "height": 1303,
        "width": 0,
        "brand_id": "",
        "type_id": "",
    },
    {
        "id": uuid.uuid4(),
        "name": "Tiger Pro",
        "diameter": 21.3,
        "efficiency": 1765,
        "height": 1052,
        "width": 0,
        "brand_id": "",
        "type_id": "",
    },
]


def upgrade() -> None:
    brands_table = sa.Table("brands", sa.MetaData(), autoload_with=op.get_bind())
    products_table = sa.Table("products", sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(
        brands_table,
        brands,
    )
    op.bulk_insert(products_table, products)


def downgrade() -> None:
    pass
