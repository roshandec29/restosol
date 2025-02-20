"""new cols

Revision ID: 9c2d1ba13bd5
Revises: 4d1147b7f380
Create Date: 2025-02-17 18:28:35.566319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9c2d1ba13bd5'
down_revision: Union[str, None] = '4d1147b7f380'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.alter_column('menus', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.add_column('order_items', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.alter_column('order_items', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.add_column('orders', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.alter_column('orders', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('orders', 'updated_at')
    op.alter_column('order_items', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('order_items', 'updated_at')
    op.alter_column('menus', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('menus', 'updated_at')
    # ### end Alembic commands ###
