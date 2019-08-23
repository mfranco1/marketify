import asyncio


class Runner:
    def __init__(self, tasks):
        """
        :param tasks: awaitable
        """
        self.loop = asyncio.get_event_loop()
        self.tasks = tasks

    def run(self):
        try:
            self.loop.run_until_complete(self.tasks)
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
