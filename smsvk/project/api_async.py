import asyncio
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError, ClientConnectorError
from aiohttp.client_exceptions import ContentTypeError, ClientHttpProxyError
from aiohttp.client_exceptions import WSServerHandshakeError, ClientOSError
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientSSLError
#from asyncio.streams import IncompleteReadError
from asyncio import TimeoutError
from .logwr import logging
from random_useragent.random_useragent import Randomize


class Api:

    def __init__(
            self,
            api_key,
            count_phone_number,
            timeout,
            limit,
            user_agent):
        self.api_key = api_key
        self.number = count_phone_number
        self.timeout = timeout
        self.limit = limit
        self.user_agent = user_agent

    async def fetch(self, url, session, fname, class_name):
        try:
            logging.info(f"Send from \"{class_name}\" get request to {url}")
            type_, device = self.user_agent
            head = {'User-Agent': Randomize().random_agent(type_, device)}
            async with session.get(url, timeout=self.timeout, headers=head, raise_for_status=True) as resp:
                assert resp.status == 200, f"Only 200 response status code, code:{resp.status}"
                if fname == 'request_json':
                    r = await resp.json(content_type=None)
                    logging.info(f"Content ({class_name}) from {url} - {r}")
                    return r
                else:
                    r = await resp.text()
                    logging.info(f"Content ({class_name}) from {url} - {r}")
                    return r
        except (ClientResponseError, ClientConnectorError, TimeoutError,
                ContentTypeError, ClientHttpProxyError,  # IncompleteReadError,
                WSServerHandshakeError, ClientProxyConnectionError,
                AssertionError, ClientSSLError) as e:
            logging.error(f"Error ({class_name}) api get request: {e}")
            return f"Error api get request: {e}"

    async def bound_fetch(self, sem, url, session, fname, i, class_name):
        async with sem:

            html = await self.fetch(url, session, fname, class_name)
            if class_name == 'GetCodeActivation' or class_name == 'SetStatusActivation':
                return i[0], i[1], i[2], html
            else:
                return i, html

    async def run(self, *args):
        url, fname, class_name, *_ = args

        sem = asyncio.Semaphore(self.limit)
        async with ClientSession() as session:
            if class_name == 'SetStatusActivation':
                url = f"{url}&action=setStatus&status={{}}&id={{}}"
                tasks = [asyncio.ensure_future(self.bound_fetch(
                    sem, url.format(i[3], i[1]), session, fname, i, class_name)
                ) for i in _[0]]
            elif class_name == 'GetCodeActivation':
                url = f"{url}&action=getStatus&id={{}}"
                tasks = [asyncio.ensure_future(self.bound_fetch(
                    sem, url.format(i[1]), session, fname, i, class_name)
                ) for i in _[0]]
            else:
                tasks = [asyncio.ensure_future(self.bound_fetch(
                    sem, url, session, fname, i, class_name)
                ) for i in range(1, self.number + 1)]

            responses = asyncio.gather(*tasks)
            return await responses

    def get_request_to_api(self, *args):

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(*args))
        data = loop.run_until_complete(future)
        return data
