from collector.wanted_collector import collect_from_wanted
from project.config import Config
from db.db_service import DBService

if __name__ == '__main__':
    dbService = DBService(host=Config.get('db.url')
                          , user=Config.get('db.username')
                          , password=Config.get('db.password')
                          , db=Config.get('db.name')
                          , charset='utf8')
    sql = 'select * from RECRUITMENT_SITE where is_use = %s and name = %s'
    row = dbService.select_one(sql, (1, 'test'))

    print(row)

    dbService.close()
