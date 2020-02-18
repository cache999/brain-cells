executable = False

async def main(m, execution_instructions, context_message):
    ans = execution_instructions['correct_ans']
    msg = int(m.content)
    if msg == ans:
        await m.channel.send('Good job our loyal comrade!')
    else:
        if msg > ans:
            await m.channel.send('Comrade, you have overestimated the number of rations! These capitalistic actions will '
                             'not be condoned. The KGB shall be at your door shortly.')
        if ans > msg:
            await m.channel.send('Comrade, you have underestimated the number of rations! Your failure to fulfill the '
                             '5-year plan is unacceptable. Prepare to be sent to gulag.')