import importlib
view = importlib.import_module('view')
Info = importlib.import_module('Info')


async def main(i: Info.Info):
    await i.channel.send(embed=view.default_embed())