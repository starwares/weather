"""create

Revision ID: b646893ef392
Revises: 
Create Date: 2023-09-16 10:43:49.379780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b646893ef392'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('data_lat', sa.String(), nullable=True),
    sa.Column('data_lon', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_index(op.f('ix_cities_name'), 'cities', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['city_name'], ['cities.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('weather',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('degrees_Celsius', sa.Integer(), nullable=True),
    sa.Column('day', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('city_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['city_name'], ['cities.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_weather_day'), 'weather', ['day'], unique=False)
    op.create_index(op.f('ix_weather_degrees_Celsius'), 'weather', ['degrees_Celsius'], unique=False)
    op.create_index(op.f('ix_weather_id'), 'weather', ['id'], unique=False)
    op.create_table('crons',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.Column('minutes', sa.Integer(), nullable=True),
    sa.Column('seconds', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('city_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['city_name'], ['cities.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crons_id'), 'crons', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_crons_id'), table_name='crons')
    op.drop_table('crons')
    op.drop_index(op.f('ix_weather_id'), table_name='weather')
    op.drop_index(op.f('ix_weather_degrees_Celsius'), table_name='weather')
    op.drop_index(op.f('ix_weather_day'), table_name='weather')
    op.drop_table('weather')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_cities_name'), table_name='cities')
    op.drop_table('cities')
    # ### end Alembic commands ###
