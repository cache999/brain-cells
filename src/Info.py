import discord


# TODO: Deprecate this class. Replace with a modified instance of discord.message.
# an information class to be passed to scripts, and to be passed from scripts to view.
class Info:
    def __init__(self, message: discord.Message = None, args: list = [], command: str = None):
        self.message = message
        self.args = args
        self.command = command
        self.m = self.message  # alias
        # these are just so my life is more convenient
        if message is not None:
            self.author = message.author
            self.channel = message.channel

    async def send(self, msg):
        await self.message.channel.send(msg)
        raise Warning('Usage of Info.send is discouraged.')

    def add_message(self, message):
        self.message = message
        self.m = message
        self.author = message.author
        self.channel = message.channel
