import requests
import logging
import json

from qsforex import settings

class BaseClient(object):
    def __init__(self):
        self.access_token = settings.ACCESS_TOKEN
        self.account_id = settings.ACCOUNT_ID
        self.stream_url = 'https://' + settings.STREAM_DOMAIN + '/v3/accounts/' + self.account_id + '/pricing/stream'
        self.api_url = 'https://' + settings.API_DOMAIN + '/v3/accounts/' + self.account_id
        self.headers = {'Authorization': 'Bearer %s' % self.access_token}
        self.logger = logging.getLogger(__name__)

    def connect_to_stream(self, pair_list):
        try:
            requests.packages.urllib3.disable_warnings()
            s = requests.Session()
            headers = {'Authorization' : 'Bearer ' + self.access_token}
            params = {'instruments' : pair_list}
            req = requests.Request('GET', self.stream_url, headers=headers, params=params)
            pre = req.prepare()
            resp = s.send(pre, stream=True, verify=False)
            return resp
        except Exception as e:
            s.close()
            print("Caught exception when connecting to stream\n" + str(e))

    def send_request(self, request_type, endpoint, params={}):
        url = self.api_url + endpoint

        if request_type == 'GET':
            r = self.get(url, params)
        elif request_type == 'POST':
            r = self.post(url, params)
        elif request_type == 'PUT':
            r = self.put(url, params)

        if r.status_code != 200 and r.status_code != 201:
            raise Exception('Error during ' + request_type + ' request to Oanda API', r.status_code)

        return r.json()

    def get(self, url, params):
        return requests.get(url, headers=self.headers, params=params)

    def post(self, url, data):
        return requests.post(url, headers=self.headers, data=data)

    def put(self, url, data):
        return requests.put(url, headers=self.headers, data=data)
