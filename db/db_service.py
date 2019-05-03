import pymysql

# select * from RECRUITMENT_SITE
# 	where is_use = 1 and name = 'wanted';


class DBService():
    def __init__(self, host, user, password, db, charset):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)

    def close(self):
        self.connection.close()

    def select_one(self, query, replacement_data):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, replacement_data)

        return cursor.fetchone()


if __name__ == '__main__':
    dbService = DBService(host='mariadb-instance.c44qfi0htc1o.ap-northeast-2.rds.amazonaws.com'
                          , user='rareraw', password='statmaria', db='stats', charset='utf8')
    sql = 'select * from RECRUITMENT_SITE where is_use = %s and name = %s'
    row = dbService.select_one(sql, (1, 'wanted'))
    print(row['crwaling_root_urls'])
    dbService.close()
