"""init

Revision ID: 5def1489c782
Revises: 
Create Date: 2022-04-23 21:20:44.782277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5def1489c782'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('search_film_history')
    op.drop_table('users_authentication')
    op.drop_table('user_profile')
    op.drop_table('users')
    op.drop_table('films_selected')
    op.drop_table('film_history_by_search')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film_history_by_search',
    sa.Column('id_search_film', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name_film', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.Column('rating', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('img_link', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_search_film'], ['search_film_history.id_search'], name='film_history_by_search_id_search_film_fkey', ondelete='CASCADE')
    )
    op.create_table('films_selected',
    sa.Column('id_film', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('login', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name_film', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.Column('rating', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('img_link', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['login'], ['users.login'], name='films_selected_login_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_film', name='films_selected_pkey')
    )
    op.create_table('users',
    sa.Column('login', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('login', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user_profile',
    sa.Column('login', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('registered', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['login'], ['users.login'], name='user_profile_login_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('login', name='user_profile_pkey')
    )
    op.create_table('users_authentication',
    sa.Column('login', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('generated_timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('auth_code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_used', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['login'], ['users.login'], name='users_authentication_login_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('login', name='users_authentication_pkey')
    )
    op.create_table('search_film_history',
    sa.Column('id_search', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('login', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name_film', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.Column('rating_start', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('rating_end', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['login'], ['users.login'], name='search_film_history_login_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_search', name='search_film_history_pkey')
    )
    # ### end Alembic commands ###