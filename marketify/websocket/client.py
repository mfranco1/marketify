import json
import logging
from abc import abstractmethod

from rx import operators as rx_ops
from rx.subject import Subject
import websockets


class WSClient:
    invalid_dict = {"is_valid": False}

    def __init__(self, source_map, crypto="BTC", currency="USD", debounce_interval=2):
        """
        :param source_map:  (dict) that maps the details of an API
        :param crypto:      cryptocurrency code
        :param currency:    fiat currency code
        """
        self.crypto = crypto.upper()
        self.currency = currency.upper()

        self.source = source_map[self.get_exchange()]
        self.websocket_msg = self.source[
            "{}{}".format(self.crypto, self.currency)
        ]["message"]
        self.url = self.source["url"]

        self.subject = Subject()
        filtered_data = self.subject.pipe(
            rx_ops.debounce(debounce_interval),
            rx_ops.distinct_until_changed(),
        )

        def on_error(err):
            self.log(msg=f"subject error: {err}")

        filtered_data.subscribe(on_next=self.get_on_next(), on_error=on_error)

    async def run(self):
        async with websockets.connect(self.url, ssl=True) as ws:
            await ws.send(json.dumps(self.websocket_msg))

            while True:
                try:
                    msg = await ws.recv()
                    market_values = self.map_response(self.parse_response(msg))

                    if market_values["is_valid"] is False:
                        continue

                    self.subject.on_next(market_values)
                # special case of catch all to avoid killing all tasks in this thread
                except Exception as exc:
                    self.log(msg=f"Catch-all triggered on: {exc}")

    def parse_response(self, resp):
        return json.loads(resp)

    def validate_mapped_response(self, resp):
        """
        :param resp:    dict result of self.map_response
        """
        if "last_price" not in resp.keys():
            return False

        return True

    def log(self, msg=""):
        logging.warning(msg=msg)

    @abstractmethod
    def map_response(self, resp):
        """ abstract method to convert raw ws response to dict """

    @abstractmethod
    def get_exchange(self):
        """ abstract method that returns an exchange name """

    @abstractmethod
    def get_on_next(self):
        """ abstract method that returns a function to perform """

