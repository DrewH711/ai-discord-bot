import openai
from openai import error
import discord
from discord.ext import commands
import os
from os import getenv
from dotenv import load_dotenv

load_dotenv("C:/Users/holla/Documents/aibot/keys.env")
BOTSTATUS="under construction"

bot = commands.Bot(command_prefix='ai.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='in development'), status=discord.Status.do_not_disturb)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Responded in {bot.latency * 1000:.0f}ms')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='List of commands', color=0x00ff00)
    embed.add_field(name='ai.help', value='Shows this message', inline=False)
    embed.add_field(name='ai.status', value='Shows the status of the AI', inline=False)
    embed.add_field(name='ai.ping', value='Shows the latency of the bot', inline=False)
    embed.add_field(name='ai.request', value='Requests a response from the API', inline=False)
    embed.add_field(name='ai.explaincode [language] [code]', value='Explains a code snippet--some languages work better than others', inline=False)
    embed.add_field(name='ai.writecode [language] [description]', value='Writes a code snippet--smom elanauges work better than others', inline=False)
    embed.add_field(name='ai.translatecode [starting language] [ending language] [code]', value='Translates a code snippet--some languages work better than others', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    embed = discord.Embed(title='Status', description=f"Currently I am {BOTSTATUS}", color=0xffa500)
    await ctx.send(embed=embed)

@bot.command()
async def request(ctx, engine):
    openai.api_key = os.getenv('OPENAI_KEY')

    x = openai.Engine.retrieve(f"{engine}")
    #if anyone knows how to actually make this handle the exception properly, please let me know
    #I've tried all kinds of variations of "openai.error.APIError" but it still doesn't work 
    try:
        await ctx.send(f"{x.id} is available: {x.ready}")
    except error.APIError:
        await ctx.send(f"{engine} is not a valid engine")

@bot.command()
async def explaincode(ctx, language, *, code):
    openai.api_key = os.getenv('OPENAI_KEY')
    code=code.replace('```','')
    code=code.replace('`','')
    response=openai.Completion.create(
    engine="davinci-codex",
    prompt=f"explain the following {language} code: \n{code}",
    max_tokens=500,
    temperature=0,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["\n\n\n"]
    )
    print(response)
    if(language!="python"):
        response.choices[0].text=response.choices[0].text.replace('#','//')
    await ctx.send(f'{ctx.author.mention}```{language}\n{response.choices[0].text}```')

@bot.command()
async def writecode(ctx, language, *, prompt):
    openai.api_key = os.getenv('OPENAI_KEY')
    response=openai.Completion.create(
    engine="davinci-codex",
    prompt=f"write the following {language} code: \n{prompt}:\n",
    max_tokens=500,
    temperature=0,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["\n\n\n"]
    )
    print(response)
    await ctx.send(f'{ctx.author.mention}```{language}\n{response.choices[0].text}```')

@bot.command()
async def translatecode(ctx, language1, language2, *, code):
    openai.api_key = os.getenv("OPENAI_KEY")
    code=code.replace('```','')
    code=code.replace('`','')    
    response = openai.Completion.create(
    engine="davinci-codex",
    prompt=f"translate this {language1} code into equivalent {language2}:\n\n{code}\n\n{language2} code goes here:\n",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=['"""','\n\n\n']
    )
    print(response)
    response.choices[0].text=response.choices[0].text.replace('\n\n\n','\n')
    await ctx.send(f'{ctx.author.mention}```{language2}\n{response.choices[0].text}```')


bot.run(os.getenv('DISCORD_TOKEN'))


