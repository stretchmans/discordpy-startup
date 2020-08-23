from discord.ext import commands
import os
import traceback
import random

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
async def on_message(message):
    i = message.content
    m = message.content.replace("/","")
    text_list = m.split("d")
    sum = 0
    for i in range(int(text_list[0])):
        one = random.randint(1, int(text_list[1]))
        sum = sum + one
    s = sum
    
    await client.send_massage(message.channel, s)

bot.run(token)
