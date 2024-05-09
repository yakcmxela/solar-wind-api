"""create incentives

Revision ID: 56552715ee87
Revises: 5fc3bbd8f015
Create Date: 2024-05-09 11:18:21.021337

"""

from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

from database.enums import IncentiveType


# revision identifiers, used by Alembic.
revision: str = "56552715ee87"
down_revision: Union[str, None] = "5fc3bbd8f015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = sa.Table("incentives", sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(
        table,
        [
            {
                "id": uuid.uuid4(),
                "type": e.name,
                "display_name": e.value,
            }
            for e in IncentiveType
        ],
    )


def downgrade() -> None:
    pass
