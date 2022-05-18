"""empty message

Revision ID: 062b8688e8e0
Revises: 5ebed943eb3e
Create Date: 2022-05-18 03:44:48.305502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '062b8688e8e0'
down_revision = '5ebed943eb3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
