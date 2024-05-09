"""create products

Revision ID: 11482eb22ff0
Revises: 56552715ee87
Create Date: 2024-05-09 11:18:25.327270

"""

from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

from database.data.solar import panels
from database.data.wind import turbines


# revision identifiers, used by Alembic.
revision: str = "11482eb22ff0"
down_revision: Union[str, None] = "56552715ee87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    products_table = sa.Table("products", sa.MetaData(), autoload_with=op.get_bind())
    incentives_table = sa.Table(
        "incentives", sa.MetaData(), autoload_with=op.get_bind()
    )
    wind = (
        op.get_bind()
        .execute(incentives_table.select().where(incentives_table.c.type == "wind"))
        .first()
    )
    solar = (
        op.get_bind()
        .execute(incentives_table.select().where(incentives_table.c.type == "solar"))
        .first()
    )

    op.bulk_insert(
        products_table,
        [
            {
                **p,
                "id": uuid.uuid4(),
                "type_id": solar.id,
            }
            for p in panels
        ],
    )
    op.bulk_insert(
        products_table,
        [
            {
                **t,
                "id": uuid.uuid4(),
                "type_id": wind.id,
            }
            for t in turbines
        ],
    )


def downgrade() -> None:
    pass
