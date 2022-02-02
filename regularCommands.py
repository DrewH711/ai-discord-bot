from discord.ext import commands
import discord
import openai
import messageClassification
import asyncio
class regularCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, cooldown:list):
        self.bot=bot
        self.cooldown=cooldown
        print("Regular commands loaded")

    #ping command
    @commands.command(name="ping", description="Pong")
    async def ping(self, ctx):
        await ctx.send(f"Pong! Responded in {int(self.bot.latency)}ms")

    #help command
    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title='Help', description='List of commands', color=0x00ff00)
        embed.add_field(name='help', value='Shows this message', inline=False)
        embed.add_field(name='status', value='Shows the status of the bot', inline=False)
        embed.add_field(name='ping', value='Shows the latency of the bot', inline=False)
        embed.add_field(name='request [engine name]', value='Requests a response from the API', inline=False)
        embed.add_field(name='explaincode [language] [code]', value='Explains a code snippet', inline=False)
        embed.add_field(name='writecode [language] [description]', value='Writes a code snippet--works best with python', inline=False)
        embed.add_field(name='translatecode [starting language] [ending language] [code]', value='Translates a code snippet', inline=False)
        embed.add_field(name='ask [question]', value='Ask the bot a question', inline=False)
        embed.add_field(name='paragraph_completion [paragraph]', value='Offers sentence suggestions to continue a paragraph', inline=False)
        embed.add_field(name='summarize [text]', value='Summarizes a text in a way that anyone can understand', inline=False)
        await ctx.send(embed=embed)

    #status command
    @commands.command(name="status")
    async def status(self, ctx):
        import urllib
        from discord import Embed
        try:
            x = openai.Engine.retrieve("code-cushman-001")
            codex_status = x.ready
        except:
            codex_status = False
        try:
            x = openai.Engine.retrieve("text-babbage-001")
            babbage_status = x.ready
        except:
            babbage_status = False
        try:
            x = openai.Engine.retrieve("text-curie-001")
            curie_status = x.ready
        except:
            curie_status = False
        try:
            site_code=urllib.request.urlopen("https://bot.themaddoxnetwork.com").getcode()
        except:
            site_code=0
        if codex_status:
            codex_status = ":white_check_mark:"
        else:
            codex_status = ":x:"
        if babbage_status:
            babbage_status = ":white_check_mark:"
        else:
            babbage_status = ":x:"
        if curie_status:
            curie_status = ":white_check_mark:"
        else:
            curie_status = ":x:"
        if site_code==200:
            site_status = ":white_check_mark:"
        else:
            site_status = ":x:"
        embedVar = Embed(title="System Status", description="", color=0x779ee4)
        embedVar.add_field(name="Discord bot", value=":white_check_mark:", inline=False)
        embedVar.add_field(name="Website", value=site_status, inline=False)
        embedVar.add_field(name="Coding AI", value=codex_status, inline=False)
        embedVar.add_field(name="Chatting and Pragraph Analysis AI", value=babbage_status, inline=False)
        await ctx.send(embed=embedVar)

    #request command
    @commands.command(name="request")
    async def request(self, ctx, engine: str):

        try:
            x = openai.Engine.retrieve(f"{engine}")
            if(x.ready):
                await ctx.send(f"{x.id} is available")
            else:
                await ctx.send(f"{x.id} is not available")
        except openai.APIError:
            await ctx.send(f"{engine} is not a valid engine")

    #ask command
    @commands.command(name="ask")
    async def ask(self, ctx, *, question: str):
        if self.cooldown.count(ctx.author.id)==0:A='p'
        else:await ctx.send('Please wait. You are on a cooldown.');return
        contentScore = messageClassification.checkMessageContent(question)
        if contentScore=="2":
            await ctx.send("Our content filter has detected that your question may contain offensive content. If you know this is not the case, please try again.")
            return
        if len(question)>300:
            await ctx.send(f'{ctx.author.mention} Sorry, that question is too long. Please keep your questions under 300 characters.')
            return
        response = openai.Completion.create(
        engine="babbage-text-001", #curie-instruct-beta-v2 is better if it's not too expensive
        prompt=f"Answer the question as accurately as possible while giving as much information as possible, but make it relatively easy to understand.\n question: {question} \n answer: ",
        max_tokens=80,
        temperature=0,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
        stop=["question:"],
        user=f"{ctx.author.id}"
        )
        response=response.choices[0].text.replace('\n','')
        if messageClassification.checkMessageContent(response)=="2":
            await ctx.send(f"{ctx.author.mention} Our content filter has detected that your response may contain offensive content, and will not be shown. Unfortunately the AI is not perfect, and this is beyond our control. Please try again.")
            return  
        else:
            await ctx.send(f'{ctx.author.mention}\n Question: {question}\n Answer: **{response}**')
        if self.cooldown.count(ctx.author.id)==0:self.cooldown.append(ctx.author.id);await asyncio.sleep(5);self.cooldown.remove(ctx.author.id)

    #paragraph completion command
    @commands.command(name="paragraph_completion")
    async def paragraph_completion(self, ctx, *, paragraph: str):
        if self.cooldown.count(ctx.author.id)==0:A='p'
        else:await ctx.send('Please wait. You are on a cooldown.');return
        contentScore = messageClassification.checkMessageContent(paragraph)
        if contentScore=="2":
            await ctx.send("Our content filter has detected that your question may contain offensive content. If you know this is not the case, please try again.")
            return
        if len(paragraph)>600:
            await ctx.send(f'{ctx.author.mention} Sorry, that paragraph is too long. Please keep your paragraphs under 600 characters.')
            return
        with open('prompts/paragraphSuggestionPrompt.txt', 'r') as f:
            examples = f.read()
            f.close()

        response = openai.Completion.create(
        engine="text-curie-001",
        prompt=f"{examples} {paragraph}\n output:",
        max_tokens=100,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0.7,
        presence_penalty=2,
        stop=["Input:", '4.'],
        user=f"{ctx.author.id}"
        )
        print(response)
        if messageClassification.checkMessageContent(response)=="2":
            await ctx.send(f"{ctx.author.mention} Our content filter has detected that your response may contain offensive content, and will not be shown. Unfortunately the AI is not perfect, and this is beyond our control. Please try again.")
            return  
        else:
            await ctx.send(f'{ctx.author.mention}\n Your paragraph:\n{paragraph}\n\n**{response.choices[0].text}**')
        if self.cooldown.count(ctx.author.id)==0:self.cooldown.append(ctx.author.id);await asyncio.sleep(45);self.cooldown.remove(ctx.author.id)

    #summarize command
    @commands.command(name="summarize")
    async def summarize(self, ctx, *, text: str):
        if self.cooldown.count(ctx.author.id)==0:A='p'
        else:await ctx.send('Please wait. You are on a cooldown.');return
        contentScore = messageClassification.checkMessageContent(text)
        if contentScore=="2":
            await ctx.send("Our content filter has detected that your question may contain offensive content. If you know this is not the case, please try again.")
            return
        if len(text)>800:
            await ctx.send(f'{ctx.author.mention} Sorry, that paragraph is too long. Please keep your paragraphs under 800 characters.')
            return
        with open('prompts/summarizePrompt.txt', 'r') as f:
            examples = f.read()
            f.close()


        response = openai.Completion.create(
        engine="text-curie-001", #curie-instruct-beta-v2 is better if it's not too expensive
        prompt=f"{examples} {text}\n rephrasing:",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0,
        stop=["Rephrase this passage in a way that a young child could understand:"],
        user=f"{ctx.author.id}"
        )
        print(response)
        if messageClassification.checkMessageContent(response)=="2":
            await ctx.send(f"{ctx.author.mention} Our content filter has detected that your response may contain offensive content, and will not be shown. Unfortunately the AI is not perfect, and this is beyond our control. Please try again.")      
        else:
            await ctx.send(f'{ctx.author.mention}\nYour text:\n{text}\nSummary: **{response.choices[0].text}**')
        if self.cooldown.count(ctx.author.id)==0:self.cooldown.append(ctx.author.id);await asyncio.sleep(45);self.cooldown.remove(ctx.author.id)