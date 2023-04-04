import sqlite3



class Word:
    en:str
    ru:str
    total:int
    success:int
    coef:int
    def __init__(self,en,ru,total,success,coef):
        self.en = en
        self.ru = ru
        self.total = total
        self.success = success
        self.coef = coef
    def __str__(self):
        return 'Word is '+self.en+', on Russian: '+self.ru  + ' total ' + str(self.total) + ' successful ' + str(self.success)+' coef ' + str(self.coef)

class Dictionary:

    words: list[Word]

    def __init__(self,count:int, name:str):
        db=sqlite3.connect(name)
        sql = db.cursor()
        self.words = []
        select=sql.execute('SELECT en,ru,total,successful,coef FROM words ORDER BY coef DESC')
        for i in range(count):
            word=select.fetchone()
            self.words.append(Word(word[0],word[1],word[2],word[3],word[4]))
        sql.close()
        db.close()

    def __str__(self):
        ans=''
        for i in range(len(self.words)):
            ans+=str(self.words[i])
            ans+='         ,           '
        return ans