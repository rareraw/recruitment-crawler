
# class Config:
#     ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#     configJson = json.load(open(ROOT_DIR + '/.projectconfig', 'r'))
#
#     @staticmethod
#     def get(find_key):
class QueryMapper:
    insert_raw_collection_query = '''INSERT INTO `stats`.`RAW_COLLECTION`
                                        (
                                        `years_of_exprience`,
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

    insert_raw_word_query = '''INSERT INTO `stats`.`RAW_WORD`
                                (
                                `word`,
                                `raw_collection_seq`)
                                VALUES
                                (
                                %s,
                                %s);
                            '''

    select_recruitment_site_query = '''SELECT * FROM RECRUITMENT_SITE
                                        WHERE name = %s                            
                                    '''
