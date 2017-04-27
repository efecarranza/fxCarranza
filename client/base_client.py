import requests

class BaseClient(object):
    def __init__(self):
        self.access_token = settings.ACCESS_TOKEN
        self.account_id = settings.ACCOUNT_ID
        self.stream_url = 'https://' + settings.STREAM_DOMAIN + '/v3/accounts/' + self.account_id + '/pricing/stream'
        self.api_url = 'https://' + settings.API_DOMAIN + '/v3'
        self.headers = {'Authorization': 'Bearer %s' % self.access_token}

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass
