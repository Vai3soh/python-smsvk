from .api_async import Api
import inspect
from .activations import balance_mode, get_count_number_mode, \
    get_number_mode, set_status_activation_mode, \
    get_code_activation_mode, get_avaible_service_mode
from typing import List, Tuple

url_ = "http://smsvk.net/stubs/handler_api.php?api_key="


class GetBalance(Api):

    def __init__(self, api: Api):
        super().__init__(api.api_key, api.number, api.timeout, api.limit, api.user_agent)

    @balance_mode
    def request(self):
        self.number = 1
        action = "&action=getBalance"
        return self.get_request_to_api(
            f"{url_}{self.api_key}{action}",
            inspect.stack()[0][3],
            self.__class__.__name__)


class GetAvaibleService(Api):

    def __init__(self, api: Api):
        super().__init__(api.api_key, api.number, api.timeout, api.limit, api.user_agent)

    @get_avaible_service_mode
    def request_json(self):
        self.number = 1
        action = "&action=getNumbersStatus"
        url = f"{url_}{self.api_key}{action}"
        return self.get_request_to_api(
            url, inspect.stack()[0][3], self.__class__.__name__)


class GetCountNumberService(Api):

    def __init__(self, api: Api):
        super().__init__(api.api_key, api.number, api.timeout, api.limit, api.user_agent)

    @get_count_number_mode
    def request_json(self, service: str):
        self.number = 1
        action = "&action=getNumbersStatus"
        url = f"{url_}{self.api_key}{action}"
        return self.get_request_to_api(
            url, inspect.stack()[0][3], self.__class__.__name__)


class GetNumber(Api):

    def __init__(self, api: Api):
        super().__init__(api.api_key, api.number, api.timeout, api.limit, api.user_agent)

    @get_number_mode
    def request(self, service: str):
        action = f"&action=getNumber&service={service}"
        url = f"{url_}{self.api_key}{action}"
        return self.get_request_to_api(
            url, inspect.stack()[0][3], self.__class__.__name__)


class SetStatusActivation(Api):

    def __init__(self, api: Api):
        super().__init__(api.api_key, api.number, api.timeout, api.limit, api.user_agent)

    @set_status_activation_mode
    def request_(self, id_: List[Tuple]):

        url = f"{url_}{self.api_key}"
        return self.get_request_to_api(
            url, inspect.stack()[0][3], self.__class__.__name__, id_)


class GetCodeActivation(SetStatusActivation):

    def __init__(self, api: Api):
        super().__init__(api)  # api.api_key,api.number,api.timeout,api.limit

    @get_code_activation_mode
    def request(self, timeout_wait_code: int, id_: List[Tuple]):

        url = f"{url_}{self.api_key}"
        return self.get_request_to_api(
            url, inspect.stack()[0][3], self.__class__.__name__, id_)
