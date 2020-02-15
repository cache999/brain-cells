import importlib
import datetime

Info = importlib.import_module('Info')


class Event(object):
    def __init__(self, trigger, executor_info, execute_info: Info.Info, timeout):
        self.trigger = trigger
        
        self.executor_info = executor_info
        self.execute_info = execute_info

        self.timeout = timeout
        self.timeout_coro = None

    def execute(self):
        raise NotImplementedError("To be overridden.")


class MessageEvent(Event):
    def __init__(self, trigger, executor_info, execute_info: Info.Info, timeout):
        super().__init__(trigger, executor_info, execute_info, timeout)

    async def execute(self):
        i = self.execute_info
        try:
            script = importlib.import_module('scripts.' + self.execute_info.command)
            try:
                await script.main(i)
            except (NotImplementedError, AttributeError):
                await i.send(i.command + ' is not implemented. Try again at a later date!')

        except ModuleNotFoundError:
            await i.send(i.command + ' is not a valid command. Type ' + prefix + 'help for more info.')
