"""empty message

Revision ID: 8b6e45533c3a
Revises: acd9c55de271
Create Date: 2018-12-14 04:39:54.082111

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8b6e45533c3a'
down_revision = 'acd9c55de271'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('role',
    sa.Column('ID', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('createdDate', sa.DateTime(), nullable=False),
    sa.Column('lastModifiedDate', sa.DateTime(), nullable=False),
    sa.Column('restId', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('ID'),
    sa.UniqueConstraint('restId'),
    schema='users'
    )
  
    op.create_table('user',
    sa.Column('ID', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('createdDate', sa.DateTime(), nullable=False),
    sa.Column('lastModifiedDate', sa.DateTime(), nullable=False),
    sa.Column('restId', sa.Integer(), nullable=True),
    sa.Column('userame', sa.String(length=80), nullable=True),
    sa.Column('firstname', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('ID'),
    sa.UniqueConstraint('restId'),
    sa.UniqueConstraint('userame'),
    schema='users'
    )
    op.create_table('information',
    sa.Column('ID', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('createdDate', sa.DateTime(), nullable=False),
    sa.Column('lastModifiedDate', sa.DateTime(), nullable=False),
    sa.Column('restId', sa.Integer(), nullable=True),
    sa.Column('userId', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.user.ID'], ),
    sa.PrimaryKeyConstraint('ID'),
    sa.UniqueConstraint('restId'),
    schema='billing'
    )
    op.create_table('login',
    sa.Column('ID', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('createdDate', sa.DateTime(), nullable=False),
    sa.Column('lastModifiedDate', sa.DateTime(), nullable=False),
    sa.Column('restId', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('passwordHash', sa.String(length=80), nullable=True),
    sa.Column('userId', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.user.ID'], ),
    sa.PrimaryKeyConstraint('ID'),
    sa.UniqueConstraint('passwordHash'),
    sa.UniqueConstraint('restId'),
    sa.UniqueConstraint('username'),
    schema='users'
    )


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment', schema='billing')
    op.drop_table('membership', schema='users')
    op.drop_table('login', schema='users')
    op.drop_table('information', schema='billing')
    op.drop_table('user', schema='users')
    op.drop_table('subscription', schema='users')
    op.drop_table('role', schema='users')
    op.drop_table('product', schema='products')
    # ### end Alembic commands ###
