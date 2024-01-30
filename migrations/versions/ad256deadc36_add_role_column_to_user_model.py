"""Add role column to User model

Revision ID: ad256deadc36
Revises: ba4c3541286d
Create Date: 2024-01-30 21:42:30.005408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad256deadc36'
down_revision = 'ba4c3541286d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=10), nullable=True))

    # Set the default value for the role column for existing users
    op.execute("UPDATE user SET role = 'customer' WHERE role IS NULL OR role = ''")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
