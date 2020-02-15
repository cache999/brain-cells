import importlib
import discord
import json
import asyncio

with open('src/arch-config.json') as file:
    cfg = json.loads(file.read())
    file.close()
print("Architecture level config loaded from arch-config.json...")
bot = importlib.import_module(cfg['bot_filename'])
# bot prefix doesn't really belong here, but here it is before I create another config.
prefix = cfg['prefix']
Info = importlib.import_module('Info')
Event = importlib.import_module('Event')
View = importlib.import_module('view')
Lang = View.Lang


# create functions to be patched
async def initialize(self: bot.Client):
    self.message_events = {}


async def on_ready(self: bot.Client):
    await self.initialize()
    print(f'{self.user} has connected to Discord.')


async def timeout_coroutine(self: bot.Client, timeout, event_author_id):
    await asyncio.sleep(timeout)
    # if the timeout has not been terminated, purge the Event using the author ID.
    print('coroutine purged because of timeout.')
    try:
        self.message_events[event_author_id].timeout_coro.cancel()
    except asyncio.CancelledError:
        pass

    self.message_events[event_author_id] = None



async def add_event(self: bot.Client, event):
    if type(event) == Event.MessageEvent:
        if self.message_events.get(event.executor_info.author.id) is not None:
            # delete a current event's coroutine if it exists
            try:
                event.timeout_coro.cancel()
            except asyncio.CancelledError:
                pass
            self.message_events[event.executor_info.author.id] = None
        # update the dict with the event.
        self.message_events.update({event.executor_info.author.id: event})
        # schedule a coroutine
        event_coroutine = asyncio.ensure_future(
            self.timeout_coroutine(event.timeout, event.executor_info.author.id)
        )
        # add a reference to the running coroutine to the event.
        self.message_events[event.executor_info.author.id].timeout_coro = event_coroutine
        print('added event')


async def listen_for_message_events(self, i):
    fulfilled_triggers = []
    for k, me in self.message_events.items():
        if me is not None:
            if me.trigger(i):
                fulfilled_triggers.append(me)
                # cancel the timeout.
                try:
                    me.timeout_coro.cancel()
                except asyncio.CancelledError:
                    pass

                self.message_events[k] = None
                print('coroutine canceled because trigger has been activated.')
    return fulfilled_triggers


async def execute_event(self, e, m):
    try:
        script = importlib.import_module('scripts.' + e.execute_info.command)
        e.execute_info.add_message(m)
        # print(e.execute_info.message)
        asyncio.ensure_future(
            script.main(e.execute_info, executor_info=e.executor_info)
        )
    except (NotImplementedError, AttributeError, ModuleNotFoundError) as err:
        print(err)
        print('why borken, ' + e.execute_info.command + ' not found')


async def on_message(self: bot.Client, m: discord.message):
    if m.author == self.user:
        return

    i = Info.Info(
        message=m,
        args=None,
        command=None
    )

    # TODO: deprecate the Info object and just use discord.message with a few added things.
    # TODO: add a language file and FIX VIEW.PY
    fulfilled_events = await self.listen_for_message_events(i)
    for e in fulfilled_events:
        # todo: make this ensure success.
        await self.execute_event(e, m)

    if i.m.content.startswith(prefix):
        # gib an Info object to the appropriate script for further handling.
        i.args = i.m.content.split(' ')
        i.command = i.args[0][len(prefix):]

        try:
            script = importlib.import_module('scripts.' + i.command)
            if script.executable:
                try:
                    '''
                    script_result = asyncio.ensure_future(
                        script.main(i)
                    )
                    '''
                    script_result = await script.main(i)
                    if script_result is not None:
                        await self.add_event(script_result)
                except (NotImplementedError, AttributeError):
                    # TODO: relegate these to view.py once it's done
                    await i.m.channel.send(Lang.get('general.commandNotImplemented') % i.command)
            else:
                # need sudo perms
                await i.m.channel.send(Lang.get('general.insufficientPermissions'))
        except ModuleNotFoundError:
            await i.m.channel.send(Lang.get('general.commandNotFound') % (i.command, prefix))


# patch the functions into the bot
bot.Client.initialize = initialize
bot.Client.timeout_coroutine = timeout_coroutine
bot.Client.listen_for_message_events = listen_for_message_events
bot.Client.execute_event = execute_event
bot.Client.add_event = add_event
bot.Client.on_ready = on_ready
bot.Client.on_message = on_message
# start the bot
print('Starting the bot...')
bot.init_bot()
