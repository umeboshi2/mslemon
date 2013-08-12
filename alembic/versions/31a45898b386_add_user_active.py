"""add user active

Revision ID: 31a45898b386
Revises: None
Create Date: 2013-08-12 14:53:03.965712

"""

# revision identifiers, used by Alembic.
revision = '31a45898b386'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('active', sa.Boolean, default=True))

def downgrade():
    op.drop_column('users', 'active')
    
                  
                   
