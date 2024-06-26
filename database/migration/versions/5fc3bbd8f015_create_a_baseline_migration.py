"""create a baseline migration

Revision ID: 5fc3bbd8f015
Revises: 
Create Date: 2024-05-09 11:18:09.430146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fc3bbd8f015'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('incentives',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.Column('display_name', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incentives_id'), 'incentives', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('efficiency_max', sa.Float(), nullable=True),
    sa.Column('efficiency_min', sa.Float(), nullable=True),
    sa.Column('brand', sa.String(length=60), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('width', sa.Float(), nullable=True),
    sa.Column('type_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['incentives.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_incentives_id'), table_name='incentives')
    op.drop_table('incentives')
    # ### end Alembic commands ###
