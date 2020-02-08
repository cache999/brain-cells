import discord


# an information class to be passed to scripts, and to be passed from scripts to view.
class Info:
    def __init__(self, message: discord.Message, args: list):
        self.message = message
        self.args = args
        # these are just so my life is more convenient
        self.command = self.args[0][1:]
        self.channel = message.channel

    async def send(self, msg):
        await self.message.channel.send(msg)
        raise Warning('Usage of Info.send is discouraged.')
