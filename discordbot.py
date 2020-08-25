from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

def dice(dice_size):
    num = np.random.randint(1, int(dice_size))
    return num

def simple_dice(dice_size, dice_num):
    dice_val = np.array([], dtype=np.int64)
    for i in range(dice_num):
        dice_val = np.append(dice_val, dice(dice_size))
    msg = 'dice: ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
    return msg

def judge(charactor, key, dice_size, dice_num):
    dice_val = np.array([], dtype=np.int64)
    for i in range(dice_num):
        dice_val = np.append(dice_val, dice(dice_size))
    if int(charactor[key]) >= np.sum(dice_val):
        msg = key + ' ' + str(charactor[key]) + ' >= ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
        if np.sum(dice_val) <= 5:
            msg += ' 【クリティカル】'
        msg += ' Success'
        return msg, True
    else:
        msg = key + ' ' + str(charactor[key]) + ' < ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
        if np.sum(dice_val) >= 96:
            msg += ' 【ファンブル】'
        msg += ' Fail'
        return msg, False
    
def damage(charactor, key):
    d = np.array([], dtype=np.int64)
    if key == 'こぶし':
        d = np.append(d, dice(3))
    elif key == '頭突き':
        d = np.append(d, dice(4))
    elif key == 'キック':
        d = np.append(d, dice(6))
    else:
        return None

    if 'd' in charactor['db']:
        result = parse('{}d{}', charactor['db'])
        dice_size = int(result[1])
        dice_num = int(result[0])
        for i in range(np.abs(dice_num)):
            if dice_num < 0:
                d = np.append(d, -dice(dice_size))
            else:
                d = np.append(d, dice(dice_size))
    return d

def temp_madness():
    roll = {}
    roll[1] = '鸚鵡返し（誰かの動作・発言を真似することしか出来なくなる）'
    #(中略)
    roll[20] = '過信（自分を全能と信じて、どんなことでもしてしまう）'
    msg = roll[dice(20)]
    msg += '\n一時的狂気(' + str(dice(10)+4) + 'ラウンドまたは' + str(dice(6)*10+30) + '分)'
    return msg

def ind_madness():
    roll = {}
    roll[1] = '失語症（言葉を使う技能が使えなくなる）'
    #(中略)
    roll[10] = '殺人癖（誰彼構わず殺そうとする） '
    msg = roll[dice(10)]
    msg += '\n不定の狂気(' + str(dice(10)*10) + '時間)'
    return msg

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
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
bot.run(token)
