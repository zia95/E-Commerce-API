"""fixes

Revision ID: 38a4813ec7ae
Revises: 9ae6584010b6
Create Date: 2023-10-04 10:43:18.065014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '38a4813ec7ae'
down_revision = '9ae6584010b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('prod_name', sa.String(length=256), nullable=False))
    op.add_column('inventory', sa.Column('prod_description', sa.String(length=2048), nullable=False))
    op.add_column('inventory', sa.Column('prod_size', sa.Integer(), nullable=False))
    op.drop_column('inventory', 'product_name')
    op.drop_column('inventory', 'desc')
    op.drop_column('inventory', 'size')
    op.add_column('orders', sa.Column('delivery_address', sa.String(length=255), nullable=False))
    op.alter_column('orders', 'notes',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)
    op.drop_index('drop_address', table_name='orders')
    op.drop_column('orders', 'drop_address')
    op.add_column('prices', sa.Column('description', sa.String(length=2048), nullable=False))
    op.add_column('prices', sa.Column('units', sa.Integer(), nullable=False))
    op.drop_column('prices', 'desc')
    op.drop_column('prices', 'quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prices', sa.Column('quantity', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('prices', sa.Column('desc', mysql.VARCHAR(length=2048), nullable=False))
    op.drop_column('prices', 'units')
    op.drop_column('prices', 'description')
    op.add_column('orders', sa.Column('drop_address', mysql.VARCHAR(length=255), nullable=False))
    op.create_index('drop_address', 'orders', ['drop_address'], unique=False)
    op.alter_column('orders', 'notes',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)
    op.drop_column('orders', 'delivery_address')
    op.add_column('inventory', sa.Column('size', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('inventory', sa.Column('desc', mysql.VARCHAR(length=2048), nullable=False))
    op.add_column('inventory', sa.Column('product_name', mysql.VARCHAR(length=256), nullable=False))
    op.drop_column('inventory', 'prod_size')
    op.drop_column('inventory', 'prod_description')
    op.drop_column('inventory', 'prod_name')
    # ### end Alembic commands ###