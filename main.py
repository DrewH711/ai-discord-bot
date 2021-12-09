import openai
import discord
from discord.ext import commands
import os

BOTSTATUS="under construction"

bot = commands.Bot(command_prefix='ai.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.change_presence(activity=discord.Game(name='in development'), status=discord.Status.do_not_disturb)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='List of commands', color=0x00ff00)
    embed.add_field(name='ai.help', value='Shows this message', inline=False)
    embed.add_field(name='ai.status', value='Shows the status of the AI', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    embed = discord.Embed(title='Status', description='Current status of the AI', color=0xffa500)
    embed.add_field(name='Status', value=f"Currently I am {BOTSTATUS}", inline=False)
    await ctx.send(embed=embed)

bot.run('DISCORD_KEY')


