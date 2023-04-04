import sqlite3

C = 0.1

def update(db_name):
    db = sqlite3.connect(db_name)
    sql = db.cursor()
    with db:
        sql.execute(f'UPDATE words SET winrate = CASE WHEN total=0 THEN 0 ELSE'
                    f' CAST(successful AS FLOAT) / CAST(total AS FLOAT) END')
        sql.execute(f'UPDATE words SET coef = winrate*winrate*(1 - TANH({C}*CAST(julianday("now") - julianday(date) AS INT)))')
    sql.close()
    db.close()