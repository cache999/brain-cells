import discord
import random
import importlib

Event = importlib.import_module('Event')
Info = importlib.import_module('Info')

executable = True


async def main(i):
    num1 = random.randint(10, 100)
    num2 = random.randint(10, 100)
    ans = min(num1, num2)

    # in hindsight i wrote an api nobody will be able to understand. But its flexible so who the fuck cares?
    event = Event.MessageEvent(
        trigger=lambda info: info.author == i.author,  # execute this event whenever same author responds
        executor_info=i,
        execute_info=Info.Info(
            message=None,
            args=[ans],  # args are a simple way to pass information. Of course, models are better.
            command='_eventtest'
        ),
        timeout=5
    )

    await i.m.channel.send('If we have %d sawdust and %d potatoes, how many rations can we make? You have 5 seconds to answer\
         or you will be purged.' % (num1, num2))

    return event
