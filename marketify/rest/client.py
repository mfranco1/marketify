import asyncio
import logging
from abc import abstractmethod

import aiohttp
from rx import operators as rx_ops
from rx.subject import Subject


class RestClient:
    invalid_dict = {"is_valid": False}

    def __init__(
        self, source_map, crypto="BTC", currency="USD", debounce_interval=2
    ):
        self.crypto = crypto.upper()
        self.currency = currency.upper()
        self.url = source_map[self.get_exchange()]

        self.subject = Subject()
        filtered_data = self.subject.pipe(
            rx_ops.debounce(debounce_interval), rx_ops.distinct_until_changed()
        )

        def on_error(err):
            self.log(msg=f"subject error: {err}")

        filtered_data.subscribe(on_next=self.get_on_next(), on_error=on_error)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            url = f"{self.url}{self.get_url_extension()}"
            while True:
                try:
                    await self.fetch(session=session, url=url)
                # special case of catch all to avoid killing all tasks in this thread
                except Exception as exc:
                    self.log(msg=f"Catch-all triggered on: {exc}")
                finally:
                    self.get_timer_func()()

    async def fetch(self, session, url):
        async with session.get(url) as resp:
            resp = await resp.json()
            market_values = self.map_response(self.parse_response(resp))

            await asyncio.sleep(self.get_sleep_interval())
            if market_values["is_valid"] is False:
                return

            self.subject.on_next(market_values)

    def parse_response(self, resp):
        return resp

    def validate_mapped_response(self, resp):
        """
        :param resp:    dict result of self.map_response
        """
        if "last_price" not in resp.keys():
            return False

        return True

    def log(self, msg=""):
        logging.warning(msg=msg)

    def get_timer_func(self):
        pass

    def get_sleep_interval(self):
        return 2

    @abstractmethod
    def map_response(self, resp):
        """ abstract method to convert raw response to dict """

    @abstractmethod
    def get_exchange(self):
        """ abstract method that returns an exchange name """

    @abstractmethod
    def get_on_next(self):
        """ abstract method that returns a function to perform """

    @abstractmethod
    def get_url_extension(self):
        """ abstract method that returns the url extension """
