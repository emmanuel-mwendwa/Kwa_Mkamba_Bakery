"""Database Migration

Revision ID: 0ecc11e06d81
Revises: 
Create Date: 2023-08-22 11:32:45.959810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ecc11e06d81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('unit_of_measurement', sa.String(length=12), nullable=True),
    sa.Column('unit_cost', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('payment_methods',
    sa.Column('method_id', sa.Integer(), nullable=False),
    sa.Column('method_name', sa.String(length=28), nullable=True),
    sa.Column('method_details', sa.String(length=56), nullable=True),
    sa.PrimaryKeyConstraint('method_id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_roles_default'), ['default'], unique=False)

    op.create_table('suppliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('phone_no', sa.String(length=13), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('production_runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flour_kneaded', sa.Integer(), nullable=False),
    sa.Column('oil_used', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('yield_amount', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('phone_no', sa.String(length=13), nullable=True),
    sa.Column('member_since', sa.DateTime(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('recipe_ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit_of_measurement', sa.String(length=12), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routes',
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.Column('route_name', sa.String(length=26), nullable=True),
    sa.Column('sales_assoc_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sales_assoc_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('route_id')
    )
    op.create_table('customers',
    sa.Column('cust_id', sa.Integer(), nullable=False),
    sa.Column('cust_name', sa.String(length=128), nullable=True),
    sa.Column('cust_email', sa.String(length=128), nullable=True),
    sa.Column('cust_phone_no', sa.Integer(), nullable=True),
    sa.Column('cust_mpesa_agent_name', sa.String(length=128), nullable=True),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['route_id'], ['routes.route_id'], ),
    sa.PrimaryKeyConstraint('cust_id')
    )
    op.create_table('dispatch',
    sa.Column('dispatch_id', sa.Integer(), nullable=False),
    sa.Column('dispatch_date', sa.DateTime(), nullable=True),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['route_id'], ['routes.route_id'], ),
    sa.PrimaryKeyConstraint('dispatch_id')
    )
    op.create_table('dispatch_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dispatch_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('returns', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['dispatch_id'], ['dispatch.dispatch_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('order_notes', sa.Text(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('payment_method_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.cust_id'], ),
    sa.ForeignKeyConstraint(['payment_method_id'], ['payment_methods.method_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('order_details',
    sa.Column('order_detail_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('order_detail_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('orders')
    op.drop_table('dispatch_details')
    op.drop_table('dispatch')
    op.drop_table('customers')
    op.drop_table('routes')
    op.drop_table('recipe_ingredients')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    op.drop_table('recipes')
    op.drop_table('production_runs')
    op.drop_table('suppliers')
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_roles_default'))

    op.drop_table('roles')
    op.drop_table('products')
    op.drop_table('payment_methods')
    op.drop_table('ingredients')
    # ### end Alembic commands ###