import sqlite3
from data.update_table import update


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
    words_copy: list[Word]
    tag: str
    def __init__(self,count:int, name:str, id:int, tag:str):
        db=sqlite3.connect(name)
        sql = db.cursor()
        self.words = []
        self.tag = tag
        select=sql.execute(f'SELECT en,ru,total,successful,coef FROM words WHERE user_id = {id} AND tag LIKE "{tag}" ORDER BY coef ASC')

        for i in range(count):
            word=select.fetchone()
            if word is not None:
                self.words.append(Word(word[0],word[1],word[2],word[3],word[4]))
        self.words_copy = self.words.copy()
        sql.close()
        db.close()

    def __str__(self):
        ans=''
        for i in range(len(self.words)):
            ans+=str(self.words[i])
            ans+='         ,           '
        return ans

    def __call__(self):
        i=-1
        while len(self.words)>0:
            i= (i+1)%len(self.words)
            yield self.words[i]

    def delete_word(self, ru:str):
        for i in range(len(self.words)):
            if self.words[i].ru == ru:
                del self.words[i]
                return
        return

    def update(self, name, id):
        db = sqlite3.connect(name)
        sql = db.cursor()
        for i in range(len(self.words_copy)):
            word_i= self.words_copy[i]
            print(f'UPDATE words SET total = {word_i.total}, successful = {word_i.success}, '
            f'date = DATE("now", "localtime") WHERE en = "{word_i.en}" AND user_id={id}')
            sql.execute(f'UPDATE words SET total = {word_i.total}, successful = {word_i.success}, '
            f'date = DATE("now", "localtime") WHERE en = "{word_i.en}" AND user_id={id}')
        db.commit()
        sql.close()
        db.close()
        update('data/words.db')
