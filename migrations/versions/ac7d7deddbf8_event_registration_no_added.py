"""event registration no added

Revision ID: ac7d7deddbf8
Revises: 100e449086a6
Create Date: 2021-10-16 19:52:51.833457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac7d7deddbf8'
down_revision = '100e449086a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('life_events', sa.Column('event_registration_no', sa.String(length=65), nullable=False))
    op.add_column('life_events', sa.Column('event_time', sa.Time(), nullable=False))
    op.create_index(op.f('ix_life_events_event_registration_no'), 'life_events', ['event_registration_no'], unique=False)
    op.create_index(op.f('ix_life_events_event_time'), 'life_events', ['event_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_life_events_event_time'), table_name='life_events')
    op.drop_index(op.f('ix_life_events_event_registration_no'), table_name='life_events')
    op.drop_column('life_events', 'event_time')
    op.drop_column('life_events', 'event_registration_no')
    # ### end Alembic commands ###
