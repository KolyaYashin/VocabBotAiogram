import sqlite3
import math

C = 0.1

def update(db_name):
    db = sqlite3.connect(db_name)
    db.create_function('sqrt', 1, math.sqrt)
    db.create_function('tanh', 1, math.tanh)
    sql = db.cursor()
    with db:
        sql.execute(f'UPDATE words SET winrate = CASE WHEN total=0 THEN 0 ELSE'
                    f' CAST(successful AS FLOAT) / CAST(total AS FLOAT) END')
        sql.execute(f'UPDATE words SET coef = SQRT(winrate)*(1 - TANH({C}*CAST(julianday("now") - julianday(date) AS INT)))')
    sql.close()
    db.close()