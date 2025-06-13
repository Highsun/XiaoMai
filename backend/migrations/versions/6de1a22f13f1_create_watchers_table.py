"""create watchers table

Revision ID: 6de1a22f13f1
Revises: a6eb9c2aa5e6
Create Date: 2025-06-13 16:24:50.722381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6de1a22f13f1'
down_revision = 'a6eb9c2aa5e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'watchers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('realname', sa.String(64), nullable=False, server_default=''),
        sa.Column('id_number', sa.String(32), nullable=False, server_default=''),
        sa.Column('phone', sa.String(20), nullable=False, server_default=''),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('watchers')