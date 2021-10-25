#  Copyright (c) 2021 Robin Ferch
import time

import requests


class FusionClient:
    def __init__(self, username, systemcode, baseurl="https://eu5.fusionsolar.huawei.com"):
        self.requestsSession = None
        self.username = username
        self.systemcode = systemcode
        self.baseurl = baseurl
        self.is_authenticated = False

    def test_authentication(self):
        auth_result = requests.post(f'{self.baseurl}/thirdData/login',
                             json={'userName': self.username, 'systemCode': self.systemcode})
        return auth_result.json()['success']

    def test_if_auth_valid(self):
        test_result = self.requestsSession.post()

    def authenticate(self):
        s = requests.session()
        auth_result = s.post(f'{self.baseurl}/thirdData/login',
                             json={'userName': self.username, 'systemCode': self.systemcode})
        if auth_result.json()['success']:
            self.requestsSession = s
            # Wait some time to ensure FusionSolar is ready to take authenticated requests
            time.sleep(1)
            self.is_authenticated = True
        else:
            raise Exception('Could not authenticate with FusionAuth cloud.')

    def get_station_list(self):
        if self.is_authenticated:
            s = self.requestsSession
            r = s.post(f'{self.baseurl}/thirdData/getStationList')
            if r.json()['failCode'] and r.json()['failCode'] == 305:
                self.authenticate()
                r = s.post(f'{self.baseurl}/thirdData/getStationList')
                return r.json()
            else:
                return r.json()
        else:
            self.authenticate()


