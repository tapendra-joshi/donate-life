"""empty message

Revision ID: 42cd15e13270
Revises: dfe1e98d2b64
Create Date: 2021-10-24 10:38:48.638656

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import sqlalchemy_utils
from constants.user_constants import BloodGroup,UserSex

# revision identifiers, used by Alembic.
revision = '42cd15e13270'
down_revision = 'dfe1e98d2b64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temp_life_users',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('blood_group', sqlalchemy_utils.types.choice.ChoiceType(BloodGroup), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('sex', sqlalchemy_utils.types.choice.ChoiceType(UserSex), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('city', sa.String(length=65), nullable=False),
    sa.Column('state', sa.String(length=65), nullable=False),
    sa.Column('country', sa.String(length=65), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_temp_life_users_city'), 'temp_life_users', ['city'], unique=False)
    op.create_index(op.f('ix_temp_life_users_country'), 'temp_life_users', ['country'], unique=False)
    op.create_index(op.f('ix_temp_life_users_created_at'), 'temp_life_users', ['created_at'], unique=False)
    op.create_index(op.f('ix_temp_life_users_last_updated_at'), 'temp_life_users', ['last_updated_at'], unique=False)
    op.create_index(op.f('ix_temp_life_users_state'), 'temp_life_users', ['state'], unique=False)
    op.alter_column('life_users', 'email',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.drop_constraint('user_event_map_ibfk_2', 'user_event_map', type_='foreignkey')
    op.create_foreign_key(None, 'user_event_map', 'temp_life_users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_event_map', type_='foreignkey')
    op.create_foreign_key('user_event_map_ibfk_2', 'user_event_map', 'life_users', ['user_id'], ['id'])
    op.alter_column('life_users', 'email',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.drop_index(op.f('ix_temp_life_users_state'), table_name='temp_life_users')
    op.drop_index(op.f('ix_temp_life_users_last_updated_at'), table_name='temp_life_users')
    op.drop_index(op.f('ix_temp_life_users_created_at'), table_name='temp_life_users')
    op.drop_index(op.f('ix_temp_life_users_country'), table_name='temp_life_users')
    op.drop_index(op.f('ix_temp_life_users_city'), table_name='temp_life_users')
    op.drop_table('temp_life_users')
    # ### end Alembic commands ###
