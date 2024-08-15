import psycopg2
import os

db = psycopg2.connect(
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host="postgres_db",  # Это имя контейнера с базой данных
    port="5432"
)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS words (
                user_id BIGINT,
                en TEXT,
                ru TEXT,
                tag TEXT,
                date DATE,
                total SMALLINT,
                successful SMALLINT,
                winrate FLOAT,
                coef FLOAT
                )""")

sql.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT,
                total_games INT,
                successful_games INT,
                winrate FLOAT,
                rating INT,
                set_test_words SMALLINT,
                include_tag BIT
                )""")


db.commit()
sql.close()
db.close()
