import sqlite3
from constant import MY_ID_TELEGRAM

dp = sqlite3.connect('data/words.db')
sql = dp.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS words (
                id INT,
                user_id BIGINT,
                en TEXT,
                ru TEXT,
                tag TEXT,
                date DATE,
                current_date DATE,
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


dp.commit()

dp.close()