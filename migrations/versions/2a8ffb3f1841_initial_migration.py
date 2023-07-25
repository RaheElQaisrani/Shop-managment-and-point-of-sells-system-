"""Initial migration

Revision ID: 2a8ffb3f1841
Revises: 
Create Date: 2023-07-25 13:29:00.772898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a8ffb3f1841'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Business',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Products',
    sa.Column('Sno', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('title2', sa.String(length=255), nullable=True),
    sa.Column('title3', sa.String(length=255), nullable=True),
    sa.Column('purchesepr', sa.Integer(), nullable=True),
    sa.Column('retailpr', sa.Integer(), nullable=True),
    sa.Column('wholepr', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('Sno')
    )
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('CNICnumber', sa.String(length=15), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('debit', sa.Float(), nullable=True),
    sa.Column('credit', sa.Float(), nullable=True),
    sa.Column('reference', sa.String(length=255), nullable=True),
    sa.Column('detail', sa.String(length=255), nullable=True),
    sa.Column('debt_allowed', sa.Boolean(), nullable=True),
    sa.Column('searchable', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('LocationID', sa.Integer(), nullable=False),
    sa.Column('locationName', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('LocationID')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('Password', sa.String(length=255), nullable=True),
    sa.Column('phoneno', sa.String(length=25), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Sales',
    sa.Column('orderid', sa.Integer(), nullable=False),
    sa.Column('customerID', sa.Integer(), nullable=True),
    sa.Column('salesmanID', sa.Integer(), nullable=True),
    sa.Column('selldate', sa.DateTime(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['customerID'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['salesmanID'], ['user.id'], ),
    sa.PrimaryKeyConstraint('orderid')
    )
    op.create_table('quantity',
    sa.Column('QID', sa.Integer(), nullable=False),
    sa.Column('LocationID', sa.Integer(), nullable=True),
    sa.Column('ProductID', sa.Integer(), nullable=True),
    sa.Column('Quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['LocationID'], ['locations.LocationID'], ),
    sa.ForeignKeyConstraint(['ProductID'], ['Products.Sno'], ),
    sa.PrimaryKeyConstraint('QID')
    )
    op.create_table('sales_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sale_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('profit', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['Products.Sno'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['Sales.orderid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sales_items')
    op.drop_table('quantity')
    op.drop_table('Sales')
    op.drop_table('user')
    op.drop_table('locations')
    op.drop_table('customers')
    op.drop_table('Products')
    op.drop_table('Business')
    # ### end Alembic commands ###
