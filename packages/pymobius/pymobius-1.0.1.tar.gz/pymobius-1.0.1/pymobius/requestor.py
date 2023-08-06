import requests


class ApiError(Exception):
    pass


class Requestor:

    def __init__(self, api_key=None, host=None, version=None, auth=None):
        self.api_key = api_key
        self.host = host or 'https://mobius.network/api'
        self.version = version or 'v1'
        self.auth = auth

    def headers(self):
        result = dict()

        if self.auth:
            result['Authorization'] = self.auth

        result['x-api-key'] = self.api_key

        return result

    def url(self, resource, action):
        return '{}/{}/{}/{}'.format(self.host, self.version, resource, action)

    def request(self, method, resource, action, **payload):
        url = self.url(resource, action)
        headers = self.headers()

        request = requests.get if method == 'GET' else requests.post
        data = dict(params=payload) if method == 'GET' else dict(data=payload)

        response = request(url, headers=headers, **data)

        if response.status_code >= 400:
            message = 'Something wrong'

            try:
                error = response.json()
                message = error.get('error').get('message')
            except Exception:
                pass

            raise ApiError(message)

        return response.json()

    def get(self, resource, action, **payload):
        return self.request('GET', resource, action, **payload)

    def post(self, resource, action, **payload):
        return self.request('POST', resource, action, **payload)
