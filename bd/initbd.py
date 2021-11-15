import sqlalchemy
from config import DNS

engine = sqlalchemy.create_engine(DNS)
con = engine.connect()

con.execute("""
    CREATE TABLE IF NOT EXISTS vk_user(
    id serial PRIMARY KEY,
    user_id INTEGER unique);
    """)

con.execute("""
    CREATE TABLE IF NOT EXISTS users_from_the_request (
    id serial PRIMARY KEY,
    vk_user_id INTEGER,
    user_id INTEGER REFERENCES vk_user(user_id));
    """)

con.execute("""
    CREATE TABLE IF NOT EXISTS favourites (
    id serial PRIMARY KEY,
    user_id INTEGER REFERENCES vk_user(user_id),
    black_list BOOLEAN,
    vk_user_id INTEGER);
    """)
