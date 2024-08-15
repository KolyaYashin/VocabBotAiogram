import psycopg2
import os
import math

C = 0.1


def update(db_name):
    db = psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                          user=os.environ['POSTGRES_USER'],
                          password=os.environ['POSTGRES_PASSWORD'],
                          host="postgres_db",  # Это имя контейнера с базой данных
                          port="5432")
    db.create_function('sqrt', 1, math.sqrt)
    db.create_function('tanh', 1, math.tanh)
    sql = db.cursor()
    with db:
        sql.execute(f'UPDATE words SET winrate = CASE WHEN total=0 THEN 0 ELSE'
                    f' CAST(successful AS FLOAT) / CAST(total AS FLOAT) END')
        sql.execute(f'UPDATE words SET coef = SQRT(winrate)*'
                    f'(1 - TANH({C}*CAST(julianday("now") - julianday(date) AS INT)))')
    sql.close()
    db.close()
