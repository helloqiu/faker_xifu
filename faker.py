# -*- coding: utf-8 -*-

import requests
import json


class Faker(object):
    def __init__(self):
        self.s = requests.Session()
        self.common_data = {'app_version': '4.5.0',
                            'appversion': '4.5.0',
                            'os': 'android',
                            'osversion': '5.1'}
        self.userid = None
        self.student_num = None
        self.host = 'http://api.bionictech.cn'

    def login(self, username=None, password=None):
        url = self.host + '/app/v4/login'
        data = self.common_data
        data['mobile'] = username
        data['password'] = password
        r = self.s.post(url, data)
        if r.status_code != 200:
            raise RuntimeError("Valid username or password")
        r_json = json.loads(r.text)
        self.userid = r_json['data']['userid']

        url = self.host + '/app/v4/profile'
        data = self.common_data
        data['no_ykt_balance'] = 'yes'
        data['userid'] = self.userid
        r = self.s.post(url, data=data)
        r_json = json.loads(r.text)
        self.student_num = r_json['data']['stuempno']

    def set_room(self, room=None):
        url = self.host + '/external/electric_biz/v1/bind_room'
        data = self.common_data
        data['room_id'] = room
        data['school_id'] = 1
        data['stuempno'] = self.student_num
        data['userid'] = self.userid

        self.s.post(url, data=data)

    def get_elec(self):
        url = self.host + '/external/electric_biz/v1/query_room_ele_info'
        r = self.s.post(url, data=self.common_data)
        r_json = json.loads(r.text)
        return {'ele_quantity': r_json['data']['ele_quantity'],
                'ele_balance': r_json['data']['ele_balance']}
