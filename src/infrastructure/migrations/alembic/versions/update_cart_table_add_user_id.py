"""Update cart table to add user_id and modify primary key

Revision ID: 8f3c9a2e1k5m
Revises: 4118f0fe3774
Create Date: 2025-01-15 10:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f3c9a2e1k5m'
down_revision = '4118f0fe3774'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade cart table schema to link with users."""
    with op.batch_alter_table('cart', schema=None) as batch_op:
        # Add user_id as foreign key
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        
        # Add id column as auto-increment identifier
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=True, autoincrement=True))
        
        # Create foreign key constraint
        batch_op.create_foreign_key(
            'fk_cart_user_id',
            'users',
            ['user_id'],
            ['id'],
            ondelete='CASCADE'
        )
        
        # Create index on user_id for query performance
        batch_op.create_index('ix_cart_user_id', ['user_id'])
        
        # Create index on (user_id, product_id) for unique constraint emulation
        batch_op.create_index('ix_cart_user_product', ['user_id', 'product_id'])


def downgrade() -> None:
    """Downgrade cart table schema to previous version."""
    with op.batch_alter_table('cart', schema=None) as batch_op:
        # Drop indexes
        batch_op.drop_index('ix_cart_user_product')
        batch_op.drop_index('ix_cart_user_id')
        
        # Drop foreign key constraint
        batch_op.drop_constraint('fk_cart_user_id', type_='foreignkey')
        
        # Remove columns
        batch_op.drop_column('user_id')
        batch_op.drop_column('id')
