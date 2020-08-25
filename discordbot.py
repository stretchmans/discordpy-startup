from discord.ext import commands
import os
import traceback
import random

bot = commands.Bot(command_prefix='c')
token = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()
client_id = conf['client_id']

@client.event
async def on_ready():
    print('Logged in')
    print('-----')

@client.event
async def on_message(message):
    # 開始ワード
    if message.content.startswith('dice'):
        # 送り主がBotではないか
        if client.user != message.author:
            info = parse('dice {}d{} {}', message.content)
            if info:
                if info[1].isdecimal() and info[0].isdecimal():
                    dice_num = int(info[0])
                    dice_size = int(info[1])
                    key = info[2]
                    # メッセージを書きます
                    m = message.author.name + ' '
                    if key == '一時的狂気':
                        m = temp_madness()
                    elif key == '不定の狂気':
                        m = ind_madness()
                    elif key == 'dice':
                        m = simple_dice(dice_size, dice_num)
                    else:
                        chara = get_charactor(str(message.author))
                        msg, result = judge(chara, key, dice_size, dice_num)
                        m += msg
                        if result:
                            d = damage(chara, key)
                        else:
                            d = None
                        if d is not None:
                            m += '\nダメージ: ' + str(np.sum(d)) + ' = ' + str(d)
                    # メッセージが送られてきたチャンネルへメッセージを送ります
                    await client.send_message(message.channel, m)

client.run(client_id)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def cb(ctx):
    num = random.randint(1, 100)
    await ctx.send(num)

bot.run(token)
