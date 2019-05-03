from collector.wanted_collector import collect_from_wanted
from db.db_service import DBService

if __name__ == '__main__':
    dbService = DBService(host='mariadb-instance.c44qfi0htc1o.ap-northeast-2.rds.amazonaws.com'
                          , user='rareraw', password='', db='stats', charset='utf8')
    sql = 'select * from RECRUITMENT_SITE where is_use = %s and name = %s'
    row = dbService.select_one(sql, (1, 'wanted'))
    collect_from_wanted(row['crwaling_root_urls'])