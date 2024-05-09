"""create incentives

Revision ID: 5859b3f32836
Revises: 1aeb105994f9
Create Date: 2024-05-09 09:43:05.415469

"""

from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa

from data.enums import IncentiveType


# revision identifiers, used by Alembic.
revision: str = "5859b3f32836"
down_revision: Union[str, None] = "1aeb105994f9"
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
