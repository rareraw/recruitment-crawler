
# class Config:
#     ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#     configJson = json.load(open(ROOT_DIR + '/.projectconfig', 'r'))
#
#     @staticmethod
#     def get(find_key):
class QueryMapper:
    insert_raw_collection_query = '''INSERT INTO `stats`.`RAW_COLLECTIONS`
                                        (
                                        `years_of_experience`,
                                        `recruitment_site_seq`,
                                        `company`,
                                        `condition_type`,
                                        `collection_date`,
                                        `create_id`)
                                        VALUES
                                        (
                                        -1,
                                        %s,
                                        %s,
                                        %s,
                                        current_date(),
                                        'system')'''

    insert_raw_word_query = '''INSERT INTO `stats`.`RAW_WORDS`
                                (
                                `word`,
                                `raw_collection_seq`)
                                VALUES
                                (
                                %s,
                                %s);
                            '''

    select_recruitment_site_query = '''SELECT * FROM RECRUITMENT_SITES
                                        WHERE name = %s                            
                                    '''

    insert_keyword_statistics_query = '''insert into keyword_statistics(keyword, count, collection_date)
                                          select D.word, count(*) as cnt, collection_date 
                                            from raw_collections M inner join raw_words D
                                                on M.seq = D.seq
                                            where M.collection_date = current_date()
                                            group by D.word
                                        '''

    insert_condition_statistics_query = '''insert into CONDITION_STATISTICS (keyword, condition_type, count, collection_date)
                                            select D.word, M.condition_type, count(*) as cnt, collection_date 
                                                from RAW_COLLECTIONS M inner join RAW_WORDS D
                                                    on M.seq = D.seq
                                                where M.collection_date = current_date()
                                                    group by D.word, M.condition_type
			                            '''
