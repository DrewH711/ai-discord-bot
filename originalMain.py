import openai
from openai import error
import discord
from discord.ext import commands
import os
from os import getenv
from dotenv import load_dotenv
from discord_slash import SlashCommand, SlashContext

load_dotenv("C:/Users/drewh/Documents/aibot/keys.env")
BOTSTATUS="under construction"

bot = commands.Bot(command_prefix='ai.')
slash=SlashCommand(bot, sync_commands=True)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='in development'), status=discord.Status.do_not_disturb)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"{ctx.author.mention}, that command does not exist")

@slash.slash(name='ping',description='latency test')
async def ping(ctx: SlashContext):
    await ctx.reply(f'Pong! Responded in {bot.latency * 1000:.0f}ms')

@slash.slash(name='help',description='shows help menu')
async def help(ctx: SlashContext):
    embed = discord.Embed(title='Help', description='List of commands', color=0x00ff00)
    embed.add_field(name='help', value='Shows this message', inline=False)
    embed.add_field(name='status', value='Shows the status of the bot', inline=False)
    embed.add_field(name='ping', value='Shows the latency of the bot', inline=False)
    embed.add_field(name='request [engine name]', value='Requests a response from the API', inline=False)
    embed.add_field(name='explaincode [language] [code]', value='Explains a code snippet--some languages work better than others', inline=False)
    embed.add_field(name='writecode [language] [description]', value='Writes a code snippet--some languages work better than others', inline=False)
    embed.add_field(name='translatecode [starting language] [ending language] [code]', value='Translates a code snippet--some languages work better than others', inline=False)
    embed.add_field(name='ask [question]', value='Ask the bot a question', inline=False)
    embed.add_field(name='paragraph_completion [paragraph]', value='Offers sentence suggestions to continue a paragraph', inline=False)
    embed.add_field(name='summarize [text]', value='Summarizes a text in a way that anyone can understand', inline=False)
    await ctx.send(embed=embed)

@slash.slash(name='status',description='shows the status of the bot')
async def status(ctx: SlashContext):
    embed = discord.Embed(title='Status', description=f"{BOTSTATUS}", color=0xffa500)
    await ctx.send(embed=embed)

@slash.slash(name='request',description='requests a response from the API')
async def request(ctx: SlashContext, engine):
    openai.api_key = os.getenv('OPENAI_KEY')

    x = openai.Engine.retrieve(f"{engine}")
    #if anyone knows how to actually make this handle the exception properly, please let me know
    #I've tried all kinds of variations of "openai.error.APIError" but it still doesn't work 
    try:
        await ctx.reply(f"{x.id} is available: {x.ready}")
    except error.APIError:
        await ctx.reply(f"{engine} is not a valid engine")

@slash.slash(name='explaincode',description='explains a code snippet--some languages work better than others')
async def explaincode(ctx: SlashContext, language, *, code):
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
    await ctx.reply(f'{ctx.author.mention}```{language}\n{response.choices[0].text}```')

@slash.slash(name='writecode',description='writes a code snippet--some languages work better than others')
async def writecode(ctx: SlashContext, language, *, prompt):
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
    if(language=="python"):
        commentchar='#'
    else:
        commentchar='//'
    await ctx.reply(f'{ctx.author.mention}```{language}\n{commentchar}{prompt} in {language}\n {response.choices[0].text}```')

@slash.slash(name='translatecode',description='translates a code snippet--some languages work better than others')
async def translatecode(ctx: SlashContext, language1, language2, *, code):
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
    await ctx.reply(f'{ctx.author.mention}```{language2}\n{response.choices[0].text}```')

@slash.slash(name='ask', description='Ask the ai a question. Keep in mind that it has very limited knowledge of current events.')
async def ask(ctx: SlashContext, *, question):
    openai.api_key = os.getenv('OPENAI_KEY')
    response = openai.Completion.create(
    engine="babbage-instruct-beta", #curie-instruct-beta-v2 is better if it's not too expensive
    prompt=f"Answer the question as accurately as possible while giving as much information as possible, but make it relatively easy to understand.\n question: {question} \n answer: ",
    max_tokens=80,
    temperature=0.8,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["question:"]
    )
    print(response)
    response=response.choices[0].text.replace('\n','')
    await ctx.reply(f'{ctx.author.mention}\n Question: {question}\n Answer: **{response}**')

@slash.slash(name='paragraph_completion', description='Suggests a sentence to continue a given paragraph')
async def paragraph_completion(ctx: SlashContext, *, paragraph):
    with open('C:/Users/holla/Documents/aibot/paragraphSuggestionPrompt.txt', 'r') as f:
        examples = f.read()
    openai.api_key = os.getenv('OPENAI_KEY')
    response = openai.Completion.create(
    engine="curie",
    prompt=f"{examples} {paragraph}\n output:",
    max_tokens=100,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0.7,
    presence_penalty=0,
    stop=["Input:", '4.']
    )
    print(response)
    await ctx.reply(f'{ctx.author.mention}\n Your paragraph:\n{paragraph}\n\n**{response.choices[0].text}**')

@slash.slash(name='summarize', description='Summarizes a given text')
async def summarize(ctx: SlashContext, *, text):
    with open('C:/Users/holla/Documents/aibot/summarizePrompt.txt', 'r') as f:
        examples = f.read()
    
    openai.api_key = os.getenv("OPENAI_KEY")

    response = openai.Completion.create(
    engine="curie-instruct-beta-v2",
    prompt=f"{examples} {text}\n rephrasing:",
    temperature=0.5,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0,
    stop=["Rephrase this passage in a way that a young child could understand:"]
    )
    print(response)
    await ctx.send(f'{ctx.author.mention}\nYour text:\n{text}\nSummary: **{response.choices[0].text}**')


bot.run(os.getenv('DISCORD_TOKEN'))


