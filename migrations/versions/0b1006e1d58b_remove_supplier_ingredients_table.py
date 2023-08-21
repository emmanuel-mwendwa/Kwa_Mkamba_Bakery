"""remove supplier_ingredients table

Revision ID: 0b1006e1d58b
Revises: 500ff655890e
Create Date: 2023-08-21 15:13:31.721053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b1006e1d58b'
down_revision = '500ff655890e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplier_ingredients')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supplier_ingredients',
    sa.Column('supplier_id', sa.INTEGER(), nullable=False),
    sa.Column('ingredient_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
    sa.PrimaryKeyConstraint('supplier_id', 'ingredient_id')
    )
    # ### end Alembic commands ###
