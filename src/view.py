from discord import Embed


async def send_raw(info, message):
    await info.send(message)

def default_embed():
    """
    Generate a default embed for sending messages.
    :return: RichEmbed
    """
    embed = Embed(
        title = 'test embed title',
        color = 0xff0000,
        description = 'test embed description',
    )
    embed.add_field(name = 'field name', value = 'field value')
    return embed