from setting import ENCODING


class Response:
    def __init__(self, code, body):
        self.code = code
        self.body = body


class Request:
    def __init__(self, datas=None):
        self.datas = datas or {}


def parse_input_data(data: str):
    result = {}
    if data:
        # делим параметры через &
        params = data.split('&')
        for item in params:
            # делим ключ и значение через =
            k, v = item.split('=')
            result[k] = v
    return result


def get_wsgi_input_data(env) -> bytes:
    # получаем длину тела
    content_length_data = env.get('CONTENT_LENGTH')
    # приводим к int
    content_length = int(content_length_data) if content_length_data else 0
    # считываем данные если они есть
    data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
    return data


def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        # декодируем данные
        data_str = data.decode(encoding=ENCODING)
        # собираем их в словарь
        result = parse_input_data(data_str)
    return result


def get_data_method(environ):
    # Метод которым отправили запрос
    method = environ['REQUEST_METHOD']

    # получаем параметры запроса
    query_string = environ['QUERY_STRING']

    request_params = None
    if method == 'GET':
        # превращаем параметры в словарь
        request_params = parse_input_data(query_string)
    elif method == 'POST':
        # получаем данные
        data = get_wsgi_input_data(environ)
        # превращаем данные в словарь
        request_params = parse_wsgi_input_data(data)
    return method, request_params


def secret_middleware(request):
    request.datas['data'] = 'Этот front controller'


middlewares = [
    secret_middleware,
]
