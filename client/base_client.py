import requests
import logging
import json

from qsforex import settings

class BaseClient(object):
    def __init__(self):
        self.access_token = settings.ACCESS_TOKEN
        self.account_id = settings.ACCOUNT_ID
        self.stream_url = 'https://' + settings.STREAM_DOMAIN + '/v3/accounts/' + self.account_id + '/pricing/stream'
        self.api_url = 'https://' + settings.API_DOMAIN + '/v3'
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

    def stream_to_queue(self, pair_list):
        response = self.connect_to_stream(pair_list)
        if response.status_code != 200:
            return
        for line in response.iter_lines(1):
            if line:
                try:
                    dline = line.decode('utf-8')
                    msg = json.loads(dline)
                    return msg
                except Exception as e:
                    self.logger.error(
                        "Caught exception when converting message into json: %s" % str(e)
                    )
                    return


    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass
