# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests


class ConfdClient:

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def url(self, *parts):
        return 'http://{host}:{port}/{path}'.format(
            host=self._host,
            port=self._port,
            path='/'.join(parts)
        )

    def is_up(self):
        url = self.url()
        try:
            response = requests.get(url)
            return response.status_code == 404
        except requests.RequestException:
            return False

    def set_applications(self, *mock_applications):
        url = self.url('_set_response')
        body = {'response': 'applications',
                'content': {app.uuid(): app.to_dict() for app in mock_applications}}

        requests.post(url, json=body)

    def set_users(self, *mock_users):
        url = self.url('_set_response')
        body = {'response': 'users',
                'content': {user.uuid(): user.to_dict() for user in mock_users}}
        requests.post(url, json=body)

    def set_moh(self, *mock_mohs):
        url = self.url('_set_response')
        body = {'response': 'moh',
                'content': {moh.uuid(): moh.to_dict() for moh in mock_mohs}}

        requests.post(url, json=body)

    def reset(self):
        url = self.url('_reset')
        requests.post(url)

    def requests(self):
        url = self.url('_requests')
        return requests.get(url).json()


class MockApplication:

    def __init__(self, uuid, name, destination=None, type_=None, moh=None, answer=None):
        self._uuid = uuid
        self._name = name
        self._destination = destination
        self._destination_options = {}
        if type_:
            self._destination_options['type'] = type_
        if moh:
            self._destination_options['music_on_hold'] = moh
        if answer:
            self._destination_options['answer'] = answer

    def uuid(self):
        return self._uuid

    def to_dict(self):
        return {
            'uuid': self._uuid,
            'name': self._name,
            'destination': self._destination,
            'destination_options': self._destination_options,
        }


class MockMoh:

    def __init__(self, uuid, name='default'):
        self._uuid = uuid
        self._name = name

    def uuid(self):
        return self._uuid

    def to_dict(self):
        return {
            'uuid': self._uuid,
            'name': self._name,
        }


class MockUser:

    def __init__(self, uuid, line_ids=None, mobile=None, voicemail=None):
        self._uuid = uuid
        self._line_ids = line_ids or []
        self._mobile = mobile
        self._voicemail = voicemail

    def uuid(self):
        return self._uuid

    def to_dict(self):
        return {
            'uuid': self._uuid,
            'lines': [{'id': line_id} for line_id in self._line_ids],
            'mobile_phone_number': self._mobile,
            'voicemail': self._voicemail,
        }
