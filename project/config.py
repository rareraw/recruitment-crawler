import json


class Config:
    configJson = json.load(open('.projectconfig', 'r'))

    @staticmethod
    def get(find_key):
        keys = find_key.split('.')
        val = Config.configJson
        for key in keys:
            val = val[key]
        return val

if __name__ == '__main__':
    print(Config.get('db.username'))

# secret_key = config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
# ci_hook_url = config['CI']['HOOK_URL'] # 'web-hooking-url-from-ci-service'