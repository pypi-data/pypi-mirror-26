import os, configparser, requests, json, http

# os.environ['INTERFACE_CONF_FILE'] = '/home/jjorissen/interface_secrets.conf'
SECRETS_LOCATION = os.environ.get('INTERFACE_CONF_FILE')
SECRETS_LOCATION = os.path.abspath(SECRETS_LOCATION) if SECRETS_LOCATION else 'apprest.conf'

config = configparser.ConfigParser()
config.read(SECRETS_LOCATION)

ENDPOINT = config.get('app_rest', 'endpoint')

# ENDPOINT = 'http://127.0.0.1:8000'
USERNAME = config.get('app_rest', 'username')
PASSWORD = config.get('app_rest', 'password')


class ConnectionError(BaseException):
    pass


class APICallError(BaseException):
    pass


class APPRestConnection:
    endpoint = ENDPOINT
    username = USERNAME
    password = PASSWORD

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if (key in ['endpoint', 'username', 'password']) and not value:
                kwargs[key] = self.__getattribute__(key)
        params = {"username": self.username, "password": self.password}
        response = requests.post(f'{self.endpoint}/api/auth/login/', auth=requests.auth.HTTPBasicAuth(**params))
        response_dict = json.loads(response.text)
        if 'token' not in response_dict.keys():
            raise ConnectionError('Could not establish a connection to the API. Please check your credentials.')
        self.auth_token = response_dict['token']
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self.auth_token}'
        }

    def _handle_status_code(self, response):
        if response.status_code == 200:
            return json.loads(response.text)
        elif response.status_code == 201:
            return json.loads(response.text)
        elif response.status_code == 204:
            return {f"Success {response.status_code}": "Record deleted successfully."}
        elif str(response.status_code).startswith('2'):
            return {f"Success {response.status_code}": http.client.resonses[response.status_code]}
        elif str(response.status_code).startswith('3'):
            return {f"Redirection {response.status_code}": http.client.resonses[response.status_code]}
        elif response.status_code == 403:
            return {f"Error {response.status_code}": "Malformed request."}
        elif response.status_code == 404:
            return {f"Error {response.status_code}": "Record did not exist or non-existent endpoint."}
        elif response.status_code == 500:
            return {f"Error {response.status_code}": "Unspecified Error"}
        else:
            return {f"Error {response.status_code}": response.text}

    def _format_entity(self, entity):
        if entity is not None and not entity.endswith('s'):
            entity += 's'
        if issubclass(entity.__class__, str):
            entity = entity.lower()
        return entity

    def all(self, entity):
        entity = self._format_entity(entity)
        request_kwargs = {"headers": self.headers}
        response = requests.get(f'{self.endpoint}/{entity}/', **request_kwargs)
        return self._handle_status_code(response)

    def search(self, entity, term):
        if not term:
            raise APICallError('Search term must be specified.')
        entity = self._format_entity(entity)
        request_kwargs = {"headers": self.headers, "params": {"search": term}}
        response = requests.get(f'{self.endpoint}/{entity}?', **request_kwargs)
        # response_dict = json.loads(response.text)
        response = self._handle_status_code(response)
        return response

    def query(self, entity=None, url=None, **kwargs):
        request_kwargs = {"headers": self.headers, "params": kwargs}
        if url:
            response = requests.get(url, **request_kwargs)
        elif entity and kwargs:
            entity = self._format_entity(entity)
            response = requests.get(f'{self.endpoint}/{entity}?', **request_kwargs)
        else:
            raise APICallError('entity and Query terms must be specified.')
        return self._handle_status_code(response)

    def page(self, paginated_response, page='next'):
        request_kwargs = {"headers": self.headers}
        if page in list(paginated_response.keys()) and paginated_response[page]:
            url = paginated_response[page]
        else:
            return False
        response = requests.get(url, **request_kwargs)
        return self._handle_status_code(response)

    def de_paginate(self, paginated_response):
        pages, count = [], 0
        if 'results' not in list(paginated_response.keys()) or 'count' not in list(paginated_response.keys()):
            if issubclass(paginated_response.__class__, dict):
                pages.append(paginated_response)
            else:
                raise APICallError('This is not a properly paginated response.')
        if 'results' in list(paginated_response.keys()):
            pages.extend(paginated_response['results'])
        if 'count' in list(paginated_response.keys()):
            count = paginated_response['count']
        while len(pages) < count:
            next_page = self.page(paginated_response)
            if next_page:
                if 'results' in list(next_page.keys()):
                    pages.extend(next_page['results'])

        return pages

    def add(self, entity, **kwargs):
        entity = self._format_entity(entity)
        request_kwargs = {"headers": self.headers, "data": json.dumps(kwargs)}
        response = requests.post(f'{self.endpoint}/{entity}/', **request_kwargs)
        response = self._handle_status_code(response)
        if 'url' not in list(response.keys()):
            # happens when the rest api did not create the object for whatever reason.
            raise APICallError(f'{response}')
        return response

    def get_or_error(self, entity, **kwargs):
        response = self.query(entity, **kwargs)
        if 'count' not in response.keys() or response['count'] != 1:
            query_summary = '\n'.join([f'"{key}": "{value}"' for key, value in kwargs.items()])
            query_summary = f'({entity}={{{query_summary}}})'
            raise APICallError(f'{len(response)} records match {query_summary}. Exactly 1 required for get request.')
        return response['results']

    def get_or_create(self, entity, **kwargs):
        response = self.query(entity, **kwargs)
        if 'count' not in response.keys() or response['count'] > 1:
            raise APICallError(f'{len(response)} records match the provided query. Exactly 1 required for get request.')
        elif 'count' not in response.keys() or response['count'] == 0:
            response, created = self.add(entity, **kwargs), True
        else:
            response, created = response['results'][0], False

        return response, created

    def add_file(self, entity="files", file=None, **kwargs):
        entity = self._format_entity(entity)
        with open(file, 'rb') as f:
            files = {"file": f}
            headers = {**self.headers}
            headers.pop('Content-Type')
            request_kwargs = {"headers": headers, "files": files, "data": kwargs}
            response = requests.post(f'{self.endpoint}/{entity}/', **request_kwargs)
        response = self._handle_status_code(response)
        return response

    def edit(self, entity=None, entity_id=None, url=None, **kwargs):
        request_kwargs = {"headers": self.headers, "data": json.dumps(kwargs)}
        if url:
            response = requests.put(url, **request_kwargs)
        elif entity and entity_id:
            entity = self._format_entity(entity)
            response = requests.put(f'{self.endpoint}/{entity}/{entity_id}/', **request_kwargs)
        else:
            raise APICallError('entity and entity_id or fully qualified url to resource must be provided.')
        return self._handle_status_code(response)

    def delete(self, entity=None, entity_id=None, url=None, **kwargs):
        request_kwargs = {"headers": self.headers, "data": json.dumps(kwargs)}
        if url:
            response = requests.delete(url, **request_kwargs)
        elif entity and entity_id:
            entity = self._format_entity(entity)
            response = requests.delete(f'{self.endpoint}/{entity}/{entity_id}', **request_kwargs)
        else:
            raise APICallError('entity and entity_id or fully qualified url to resource must be provided.')
        return self._handle_status_code(response)

    def entity_info(self, entity=None, **kwargs):
        entity = self._format_entity(entity)
        request_kwargs = {"headers": self.headers,}
        uri = f'{self.endpoint}/model_info/{entity}/' if entity else f'{self.endpoint}/model_info/'
        response = requests.get(uri, **request_kwargs)
        return self._handle_status_code(response)