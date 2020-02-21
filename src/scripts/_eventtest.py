from importlib import import_module
view = import_module('.view', package='src')


executable = False

async def main(m, execution_instructions, context_message):
    ans = execution_instructions['correct_ans']
    msg = int(m.content)
    if msg == ans:
        await view.send(m.channel, view.Lang.get('embed.eventTestCorrect'))
    else:
        if msg > ans:
            await view.send(m.channel, view.Lang.get('embed.eventTestOver'))
        if ans > msg:
            await view.send(m.channel, view.Lang.get('embed.eventTestUnder'))