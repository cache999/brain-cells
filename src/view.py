from discord import Embed
import json
import importlib

config = importlib.import_module('config')
embed_templates = importlib.import_module('embed_templates')

async def send(channel, message_or_embed_or_dict: (str, Embed, dict)):
    med = message_or_embed_or_dict
    if isinstance(med, str):
        await channel.send(content=med)
    if isinstance(med, Embed):
        await channel.send(embed=med)
    if isinstance(med, dict):
        await channel.send(embed=Embed.from_dict(med))


def apply_template(embed_dict):
    """Apply a template specified in embed_dict to the embed_dict itself.

    :param embed_dict: embed_dict with template defined. If template is not defined, dict is
    returned as is.
    :return: embed_dict but with the template applied
    """
    color = embed_dict.get('color')
    if color is not None:
        embed_dict['color'] = int(color, 16)
    template = embed_dict.get('template')
    if template is None:
        return embed_dict
    del embed_dict['template']
    return {**getattr(embed_templates, template), **embed_dict}


# wrapper for language
class Lang:
    with open('languages/' + config.lang_file) as f:
        lang_file = json.loads(f.read())
        f.close()

    # load and apply templates to embeds defined in lang file
    for k, v in lang_file.items():
        if isinstance(v, dict):
            lang_file[k] = apply_template(v)

    @staticmethod
    def get(name):
        return Lang.lang_file[name].copy()
