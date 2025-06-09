"""redesign order schema, add inventory

Revision ID: e12912287830
Revises: 1102f4a617ed
Create Date: 2025-06-09 13:31:47.149368

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e12912287830'
down_revision = '1102f4a617ed'
branch_labels = None
depends_on = None


def upgrade():
    # 1) 创建 orders 表
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('total_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('status', sa.String(32), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_orders_user'),
    )

    # 2) 创建 order_items 表
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('show_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name='fk_order_items_order'),
        sa.ForeignKeyConstraint(['show_id'],  ['shows.id'],  name='fk_order_items_show'),
    )

    # 3) 给 shows 表新增 inventory 列（带默认值 0）
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'inventory',
                sa.Integer(),
                nullable=False,
                server_default='0'
            )
        )


def downgrade():
    # 回滚时反向操作：先删 inventory，再删两个表
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.drop_column('inventory')

    op.drop_table('order_items')
    op.drop_table('orders')
