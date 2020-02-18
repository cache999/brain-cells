import importlib
import datetime
import discord

# Info = importlib.import_module('Info')


class Event(object):
    def __init__(self, trigger, context_message: discord.Message, execution_instructions: dict, timeout, timeout_instructions):
        self.trigger = trigger

        self.context_message = context_message # direct copy of the Info passed onto the executor.

        self.execution_instructions = execution_instructions # instructions determining what script will be run
        # and with what parameters.

        self.timeout = timeout
        self.timeout_instructions = timeout_instructions
        self.timeout_coro = None

    def execute(self):
        raise NotImplementedError("To be overridden.")


class MessageEvent(Event):
    def __init__(self, trigger, context_message: discord.Message, execution_instructions: dict, timeout,
                 timeout_instructions = None):
        super()
        super().__init__(trigger, context_message, execution_instructions, timeout, timeout_instructions)

    '''
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
    '''
