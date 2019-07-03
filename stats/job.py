from db.db_service import DBService
from db.query_mapper import QueryMapper
from project.config import Config


def stats_insert():
    print("stats job start!")
    db_service = DBService(host=Config.get('db.url')
                           , user=Config.get('db.username')
                           , password=Config.get('db.password')
                           , db=Config.get('db.name')
                           , charset='utf8')

    cursor = db_service.get_cursor()
    cursor.execute(QueryMapper.insert_keyword_statistics_query)
    cursor.execute(QueryMapper.insert_condition_statistics_query)
    db_service.commit_and_close()
