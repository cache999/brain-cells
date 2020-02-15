executable = False

async def main(i, executor_info):
    ans = i.args[0]
    msg = int(i.m.content)
    if msg == ans:
        await i.m.channel.send('Good job our loyal comrade!')
    else:
        if msg > ans:
            await i.m.channel.send('Comrade, you have overestimated the number of rations! These capitalistic actions will '
                             'not be condoned. The KGB shall be at your door shortly.')
        if ans > msg:
            await i.m.channel.send('Comrade, you have underestimated the number of rations! Your failure to fulfill the '
                             '5-year plan is unacceptable. Prepare to be deported to siberia.')