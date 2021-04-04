import sqlite3,os

class ImgUrlTable:
    def __init__(self):
        self.db_file = os.path.join(os.path.dirname(__file__), 'imgUrl.db')
        if not os.path.isfile(self.db_file):
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            self.cursor.execute('create table imgurl (id varchar(20) primary key,url varchar(200))')
            self.conn.commit()
        else:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        print('数据库连接关了')


    def add_row(self,url):
        sql = 'INSERT INTO imgurl (id, url) VALUES (?,?)'
        self.cursor.execute('select id from imgurl')
        result_list = self.cursor.fetchall()
        data = (str(len(result_list)), url)
        self.cursor.execute(sql,data)
        self.conn.commit()

    def select_all(self):
        self.cursor.execute('select * from imgurl')
        result_list = self.cursor.fetchall()
        return result_list

if __name__ == '__main__':
    imgdb = ImgUrlTable()
    print(imgdb.select_all())
