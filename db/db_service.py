import pymysql

# select * from RECRUITMENT_SITE
# 	where is_use = 1 and name = 'wanted';


class DBService():
    def __init__(self, host, user, password, db, charset):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def close(self):
        self.connection.close()

    def select_one(self, query, replacement_data=()):
        self.cursor.execute(query, replacement_data)

        return self.cursor.fetchone()

    def get_last_id(self):
        return self.select_one('SELECT LAST_INSERT_ID() as last_id')['last_id']

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.cursor.execute("commit")

    def commit_and_close(self):
        self.commit()
        self.close()

    # def execute(self, query, replacement_data):
    #     cursor = self.connection.cursor(pymysql.cursors.DictCursor)
    #     cursor.execute(query, replacement_data)
