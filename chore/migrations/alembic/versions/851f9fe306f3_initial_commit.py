"""Initial commit

Revision ID: 851f9fe306f3
Revises: 
Create Date: 2021-03-27 02:26:36.407878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '851f9fe306f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('assemblyinformation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('commit_message', sa.String(), nullable=False),
    sa.Column('commit_id', sa.String(), nullable=False),
    sa.Column('assembly', sa.JSON(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    )


def downgrade():
    op.drop_table('assemblyinformation')
