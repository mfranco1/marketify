import asyncio


class Runner:
    def __init__(self, tasks):
        """
        :param tasks: iterable of async tasks to run
        """
        self.loop = asyncio.get_event_loop()
        self.clients = asyncio.gather(
            *tasks
        )

    def run(self):
        try:
            self.loop.run_until_complete(self.clients)
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
