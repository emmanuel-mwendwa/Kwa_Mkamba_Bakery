"""some new modifications

Revision ID: 2651752fb42c
Revises: 626a4a0ed09b
Create Date: 2023-06-21 21:32:47.527555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2651752fb42c'
down_revision = '626a4a0ed09b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_details',
    sa.Column('order_detail_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('order_detail_id')
    )
    op.drop_table('orderdetails')
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cust_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('cust_name', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('cust_email', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('cust_phone_no', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('cust_mpesa_agent_name', sa.String(length=128), nullable=True))
        batch_op.drop_column('email')
        batch_op.drop_column('name')
        batch_op.drop_column('mpesa_agent_name')
        batch_op.drop_column('phone_no')
        batch_op.drop_column('id')

    with op.batch_alter_table('dispatch', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dispatch_id', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('order_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('order_notes', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('customer_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'customers', ['customer_id'], ['cust_id'])
        batch_op.drop_column('orderDate')
        batch_op.drop_column('id')
        batch_op.drop_column('notes')

    with op.batch_alter_table('payment_methods', schema=None) as batch_op:
        batch_op.add_column(sa.Column('method_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('method_details', sa.String(length=56), nullable=True))
        batch_op.drop_column('details')
        batch_op.drop_column('id')

    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sales_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('sale_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('sales_total_amount', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('customer_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('payment_method', sa.String(length=28), nullable=True))
        batch_op.create_foreign_key(None, 'customers', ['customer_id'], ['cust_id'])
        batch_op.drop_column('totalAmount')
        batch_op.drop_column('saleDate')
        batch_op.drop_column('id')
        batch_op.drop_column('paymentMethod')

    with op.batch_alter_table('sales_reports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('report_id', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sales_reports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('report_id')

    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paymentMethod', sa.VARCHAR(length=28), nullable=True))
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('saleDate', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('totalAmount', sa.FLOAT(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('payment_method')
        batch_op.drop_column('customer_id')
        batch_op.drop_column('sales_total_amount')
        batch_op.drop_column('sale_date')
        batch_op.drop_column('sales_id')

    with op.batch_alter_table('payment_methods', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('details', sa.VARCHAR(length=56), nullable=True))
        batch_op.drop_column('method_details')
        batch_op.drop_column('method_id')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notes', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('orderDate', sa.DATETIME(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('customer_id')
        batch_op.drop_column('order_notes')
        batch_op.drop_column('order_date')
        batch_op.drop_column('order_id')

    with op.batch_alter_table('dispatch', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('dispatch_id')

    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('phone_no', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('mpesa_agent_name', sa.VARCHAR(length=128), nullable=True))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=128), nullable=True))
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=128), nullable=True))
        batch_op.drop_column('cust_mpesa_agent_name')
        batch_op.drop_column('cust_phone_no')
        batch_op.drop_column('cust_email')
        batch_op.drop_column('cust_name')
        batch_op.drop_column('cust_id')

    op.create_table('orderdetails',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('quantity', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('order_details')
    # ### end Alembic commands ###