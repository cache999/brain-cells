import importlib
import discord
import json
import asyncio

config = importlib.import_module('config')
bot = importlib.import_module(config.bot_filename)
# bot prefix doesn't really belong here, but here it is before I create another config.
Event = importlib.import_module('Event')
view = importlib.import_module('view')
Lang = view.Lang


# create functions to be patched
async def initialize(self: bot.Client):
    self.message_events = {}


async def on_ready(self: bot.Client):
    await self.initialize()
    print(f'{self.user} has connected to Discord.')


async def timeout_coroutine(self: bot.Client, timeout, event_channel_id, event_author_id):
    await asyncio.sleep(timeout)
    # if the timeout has not been terminated, purge the Event.
    print('coroutine purged because of timeout.')
    # cancel coro
    try:
        self.message_events[event_channel_id][event_author_id].timeout_coro.cancel()
    except asyncio.CancelledError:
        pass

    # execute timeout!
    e = self.message_events[event_channel_id][event_author_id]
    if e.timeout_instructions is not None:
        try:
            script = importlib.import_module('scripts.' + e.timeout_instructions['script'])
            # e.execute_info.add_message(m)
            # run
            asyncio.ensure_future(
                script.main(execution_instructions=e.execution_instructions, context_message=e.context_message)
            )
        except (NotImplementedError, AttributeError, ModuleNotFoundError) as err:
            print(err)
            print('why borken, ' + e.timeout_instructions['script'] + ' not found')


    del self.message_events[event_channel_id][event_author_id]


async def add_event(self: bot.Client, event):
    if type(event) == Event.MessageEvent:

        if self.message_events.get(event.context_message.author.id) is not None:
            # delete a current event's coroutine if it exists
            try:
                event.timeout_coro.cancel()
            except asyncio.CancelledError:
                pass

            del self.message_events[event.context_message.author.id]
        # create a nested channel dict if necessary.
        if self.message_events.get(event.context_message.channel.id) is None:
            self.message_events.update({
                event.context_message.channel.id: {
                    event.context_message.author.id: event
                }
            })
        self.message_events[event.context_message.channel.id].update({
            event.context_message.author.id: event
        })

        # submit coroutine
        event_coroutine = asyncio.ensure_future(
            self.timeout_coroutine(event.timeout,
                                   event.context_message.channel.id,
                                   event.context_message.author.id
                                   )
        )
        # add a reference to the running coroutine to the event.
        self.message_events[event.context_message.channel.id][
            event.context_message.author.id].timeout_coro = event_coroutine
        print('added event')


async def listen_for_message_events(self, m):
    fulfilled_triggers = []
    channel_dict = self.message_events.get(m.channel.id)
    if channel_dict is not None:
        for k, me in channel_dict.items():
            if me is not None:
                if me.trigger(m):
                    fulfilled_triggers.append(me)
                    # cancel the timeout.
                    try:
                        me.timeout_coro.cancel()
                    except asyncio.CancelledError:
                        pass

                    channel_dict[k] = None
                    print('coroutine canceled because trigger has been activated.')
        return fulfilled_triggers
    else:
        return []


async def execute_event(self, e, m):
    # todo: make this ensure success.
    try:
        script = importlib.import_module('scripts.' + e.execution_instructions['script'])
        # e.execute_info.add_message(m)
        # run
        asyncio.ensure_future(
            script.main(m, execution_instructions=e.execution_instructions, context_message=e.context_message)
        )
    except (NotImplementedError, AttributeError, ModuleNotFoundError) as err:
        print(err)
        print('why borken, ' + e.execution_instructions['script'] + ' not found')


async def on_message(self: bot.Client, m: discord.Message):
    if m.author == self.user:
        return

    # TODO: FIX VIEW.PY
    fulfilled_events = await self.listen_for_message_events(m)
    for e in fulfilled_events:
        await self.execute_event(e, m)

    if m.content.startswith(config.prefix):
        args = m.content.lower().split(' ')
        command = args[0] = args[0][len(config.prefix):]
        # TODO: I don't like this. This is unclean. PURGE

        # gib the Message object to the appropriate script for further handling.
        try:
            script = importlib.import_module('scripts.' + command)
            if script.executable:
                try:
                    # todo: make this use ensure_future instead of await because await tay
                    ''' 
                    script_result = asyncio.ensure_future(
                        script.main(i)
                    )
                    '''
                    script_result = await script.main(m)

                    if script_result is not None:
                        print('adding event')
                        await self.add_event(script_result)
                except (NotImplementedError, AttributeError):
                    # TODO: relegate these to view.py once it's done
                    await m.channel.send(Lang.get('general.commandNotImplemented') % command)
            else:
                # need sudo perms
                await m.channel.send(Lang.get('general.insufficientPermissions'))
        except ModuleNotFoundError:
            await m.channel.send(Lang.get('general.commandNotFound') % (command, config.prefix))


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
