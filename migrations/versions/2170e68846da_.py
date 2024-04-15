"""empty message

Revision ID: 2170e68846da
Revises: c2be24291d56
Create Date: 2024-04-14 14:08:49.830062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2170e68846da'
down_revision = 'c2be24291d56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=60), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_column('email')

    # ### end Alembic commands ###