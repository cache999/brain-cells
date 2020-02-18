import discord
import random
import importlib

Event = importlib.import_module('Event')
config = importlib.import_module('config')

executable = True


async def main(m):
    args = m.content.lower().split(' ')
    command = args[0] = args[0][len(config.prefix):]

    num1 = random.randint(10, 100)
    num2 = random.randint(10, 100)
    ans = min(num1, num2)

    # in hindsight i wrote an api nobody will be able to understand. But its flexible so who the fuck cares?
    event = Event.MessageEvent(
        lambda info: info.author == m.author,  # execute this event whenever same author responds
        m, # context message
        {
            'script': '_eventtest',
            'correct_ans': ans
        }, # execution instructions
        5, # timeout
        {
            'script': '_eventtesttimeout'
        } # timeout instructions
    )

    await m.channel.send('If we have %d sawdust and %d potatoes, how many rations can we make? You have 5 seconds to answer\
         or you will be purged.' % (num1, num2))

    return event
