from psycopg2 import connect
from environs import Env

env = Env()
env.read_env()

def get_connect():
    return connect(
        database = env.str("DATABASE"),
        user = env.str("USER"),
        port = env.str("PORT"),
        host = env.str("HOST"),
        password = env.str("PASSWORD")
    )
