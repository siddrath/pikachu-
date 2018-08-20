import discord
from discord.ext import commands
from pokedex import pokedex
import datetime
import random
import requests
import aiohttp
import re
from random import randint
from random import choice
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
import io





bot = commands.Bot(description='cool can do a lot more.....',command_prefix=commands.when_mentioned_or('p?'))
bot.remove_command('help')





@bot.command()
async def owner(ctx):
    ': Name of my creator'
    await ctx.send('My owner is <@411496838550781972> ')
    await ctx.message.delete()


@bot.command()
async def ping(ctx):
    ': Check your connection '
    t1 = ctx.message.created_at
    m = await ctx.send('**Pong!**')
    time = (m.created_at - t1).total_seconds() * 1000
    await m.edit(content='**Pong! Took: {}ms**'.format(int(time)))
    await ctx.message.delete()

@bot.command()
async def uptime(ctx):
    res = os.popen("uptime").read()
    matches = re.findall(r"up (\d+) days, (\d+):(\d+)", res)
    time = matches[0]
    fmtime = "{0[0]} days, {0[1]} hours {0[2]} minutes".format(time)
    await ctx.send(f'''```py\n{fmtime}```''')




@bot.command(
    name="pokemon")
async def _pokemon(ctx, *, pokemon):
    """: Check info about pokemon"""

    pokedex1 = pokedex.Pokedex(
        version='v1',
        user_agent='ExampleApp (https://example.com, v2.0.1)')
    x = pokedex1.get_pokemon_by_name(f'''{pokemon}''')
    embed = discord.Embed(
        title=f'''{x[0]['name']}''',
        description=f'''Discovered in generation {x[0]['gen']}''',
        color=discord.Colour.dark_purple())
    embed.add_field(
        name='Species', value=f'''{x[0]['species']}''', inline=False)
    if not x[0]['gender']:
        embed.add_field(name='Gender', value="No Gender", inline=False)
    else:
        embed.add_field(
            name='Gender',
            value=
            f'''Male:  {x[0]['gender'][0]}%\nFemale:  {x[0]['gender'][1]}%''',
            inline=False)
    embed.add_field(
        name='Type',
        value=f'''{', '.join(str(i) for i in x[0]['types'])}''',
        inline=False)
    embed.set_image(url=f'''{x[0]['sprite']}''')
    embed.add_field(
        name='Abilities',
        value=
        f'''{', '.join(str(i)for i in x[0]['abilities']['normal'])}''',
        inline=False)
    if not x[0]['abilities']['hidden']:
        embed.add_field(
            name='Hidden Abilities',
            value="No hidden talents like me",
            inline=False)
    else:
        embed.add_field(
            name='Hidden Abilities',
            value=
            f'''{', '.join(str(i)for i in x[0]['abilities']['hidden'])}''',
            inline=False)
    embed.add_field(
        name='Egg Groups',
        value=f'''{', '.join(str(i)for i in x[0]['eggGroups'])}''',
        inline=False)
    embed.add_field(
        name='Evolution',
        value=
        f'''{' => '.join(str(i)for i in x[0]['family']['evolutionLine'])}''',
        inline=False)
    embed.add_field(name='Height', value=x[0]['height'], inline=False)
    embed.add_field(name='Weight', value=x[0]['weight'], inline=False)
    if x[0]['legendary']:
        a = 'Legendary'
    elif x[0]['starter']:
        a = 'Starter'
    elif x[0]['mythical']:
        a = 'Mythical'
    elif x[0]['ultraBeast']:
        a = 'Ultra Beast'
    elif x[0]['mega']:
        a = 'Mega'
    else:
        a = '-'
    embed.add_field(name='Notes', value=a, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    ': Get the server info'
    guild = ctx.guild
    embed = discord.Embed(title=f'''{ctx.guild.name}''', colour=discord.Colour.dark_purple(), description='More Info Below', timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=f'''{ctx.guild.icon_url}''')
    embed.add_field(name='Server Created At :', value=f'''{ctx.guild.created_at}''', inline=False)
    embed.add_field(name='Created by :', value=f'''{ctx.guild.owner.mention}''', inline=False)
    embed.add_field(name='Region :', value=f'''  {ctx.guild.region}''', inline=False)
    embed.add_field(name='Server ID :', value=f'''{ctx.guild.id}''', inline=False)
    embed.add_field(name='Server Members :', value=f'''  {len(guild.members)}''', inline=False)
    embed.add_field(name='Online Members :',
                    value=f'''{len([I for I in guild.members if I.status is discord.Status.online])}''', inline=False)
    embed.add_field(name='Server Channel :', value=f'''  {len(guild.channels)}''', inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def avatar(ctx, user: discord.Member = None):
    """: Check AVATARS"""
    user = user or ctx.message.author
    embed = discord.Embed(title=f'''{user.name}'s Avatar''', description=f'''{user.name} looks like.....''',color=discord.Colour.dark_purple())
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def count(ctx):
    ''': Get the info about my servers'''
    total = sum(1 for m in set(ctx.bot.get_all_members()) if m.status != discord.Status.offline)
    embed = discord.Embed(title=f'''Count''', colour=discord.Colour.dark_purple(),description=f'''I am in **{len(bot.guilds)}** servers \nI am used by **{len(bot.users)}** users \nI am currently entertaining **{total}** users''')

    embed.set_thumbnail(url=f'''{bot.user.avatar_url}''')
    await ctx.send(embed=embed)
    
@bot.command(name="8ball")
async def _ball(ctx, *, question):
        ': Ask me a question'
        question = question
        answers = random.randint(1, 20)

        if question == "":
            return

        elif answers == 1:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}``` It is certain```""")

        elif answers == 2:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  It is decidedly so```""")

        elif answers == 3:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Without a doubt```""")

        elif answers == 4:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}``` Yes definitely```""")

        elif answers == 5:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  You may rely on it```""")

        elif answers == 6:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  As i see it, yes```""")

        elif answers == 7:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Most likely```""")

        elif answers == 8:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Outlook good```""")

        elif answers == 9:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Yes```""")

        elif answers == 10:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Signs point to yes```""")

        elif answers == 11:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Reply hazy try again```""")

        elif answers == 12:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Ask again later```""")

        elif answers == 13:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Better not to tell you now```""")

        elif answers == 14:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}``` Cannot predict now```""")

        elif answers == 15:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Concentrate and ask again```""")

        elif answers == 16:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Don't count on it```""")

        elif answers == 17:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  My reply is no```""")

        elif answers == 18:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  My sources say no```""")

        elif answers == 19:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Outlook not so good```""")

        elif answers == 20:
            await ctx.send(f"""\U0001f3b1 Question by {ctx.author.name}: {question}```  Very doubtful```""")


@bot.command()
async def perms(ctx, user: discord.Member = None):
    ': Find what you can do on this server'
    user = ctx.message.author if user is None else user
    if not user:
        user = ctx.author
    mess = []
    for i in user.guild_permissions:
        if i[1]:
            mess.append("\u2705 {}".format(i[0]))
        else:
            mess.append("\u274C {}".format(i[0]))
    embed = discord.Embed(title = f'''{user.name} 's permissions in the server are: ''',description ="\n".join(mess), color = discord.Colour.dark_purple())
    await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason):
    ': Kick the member if you have authority '
    if ctx.author.permissions_in(ctx.channel).kick_members:
        if reason is None:
            await member.send(f'''You have been kicked by {ctx.author.name} from {ctx.guild.name} due to __No reason given__ ''')
            em = discord.Embed(title='Kicked', colour=discord.Colour.dark_red(),
                            description=f'''{member} has been kicked''', timestamp= datetime.datetime.utcnow())
            em.set_thumbnail(url=member.avatar_url)
            em.add_field(name='Moderator', value=f'''{ctx.author.name}''', inline=False)
            em.add_field(name='Culpret', value=f'''{member}''', inline=False)
            em.add_field(name='Reason for kicking', value=f'''_No reason provided_''', inline=False)
            await ctx.send(embed=em)
            await member.kick()
        else:
            await member.send(f'''You have been kicked by {ctx.author.name} from {ctx.guild.name} due to {reason} ''')
            em = discord.Embed(title='Kicked', colour=discord.Colour.dark_red(),
                                description=f'''{member} has been kicked''', timestamp=datetime.datetime.utcnow())
            em.set_thumbnail(url=member.avatar_url)
            em.add_field(name='Moderator', value=f'''{ctx.author.name}''', inline=False)
            em.add_field(name='Culprit', value=f'''{member}''', inline=False)
            em.add_field(name='Reason for kicking', value=f'''{reason}''', inline=False)
            await ctx.send(embed=em)
            await member.kick()
    else:
        message = await ctx.send(f'''{ctx.author.mention} you are not eligible for this''', delete_after= 3)
        await message.add_reaction('\u2623')

@bot.command()
async def purge(ctx, limit: int):
    ': Delete messages'
    if ctx.author.permissions_in(ctx.channel).manage_messages:
        await ctx.channel.purge(limit=limit)
        await ctx.send(f'''Deleted {limit} message(s)''')
    else:
        return

@bot.command()
async def prune(ctx, days: int):
    ': Prune the inactive members'
    if ctx.author.permissions_in(ctx.channel).ban_members:
        await ctx.guild.prune_members(days=days)
    else:
        await ctx.send(f'''{ctx.author.mention} you are not Eligible for this''',delete_after = 3)

@bot.command()
async def warn(ctx, member: discord.Member , *, reason = None):
    ''': SoftWarn a person'''
    if ctx.author.permissions_in(ctx.channel).kick_members or ctx.author.permissions_in(ctx.channel).manage_messages:
        if reason is None:
            await ctx.send(f'''{ctx.author.mention} \n ```A reason needed to warn``` ''')
        else:
            embed = discord.Embed(title='Warning', colour=discord.Colour.gold(),
                                    description =f'''You have been warned by {ctx.author.name} for {reason}''', timestamp=datetime.datetime.utcnow())
            await member.send(embed=embed)
            em = discord.Embed(title='Warned', colour=discord.Colour.gold(),
                                description=f'''{member} has been warned''', timestamp=datetime.datetime.utcnow())
            em.set_thumbnail(url=member.avatar_url)
            em.add_field(name='Moderator', value=f'''{ctx.author.name}''', inline=False)
            em.add_field(name='Culprit', value=f'''{member}''', inline=False)
            em.add_field(name='Reason for warning', value=f'''{reason}''', inline=False)
            await ctx.send(embed=em)
    else:
        await ctx.send(f'''{ctx.author.mention} you aren't eligible for this''', delete_after= 3)





@bot.command(pass_context=True)
async def poke(ctx, member: discord.Member):
    """poke someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    poke = "**{0} poked {1}!**"

    choices = ['https://pa1.narvii.com/6021/b50b8078fa1d8e8f6d2ebfb085f106c642141723_hq.gif',
               'https://media1.tenor.com/images/8fe23ec8e2c5e44964e5c11983ff6f41/tenor.gif',
               'https://media.giphy.com/media/WvVzZ9mCyMjsc/giphy.gif',
               'https://media.giphy.com/media/pWd3gD577gOqs/giphy.gif',
               'http://gifimage.net/wp-content/uploads/2017/09/anime-poke-gif-12.gif', 'https://i.gifer.com/S00v.gif',
               'https://i.imgur.com/1NMqz0i.gif']

    image = random.choice(choices)

    embed = discord.Embed(description=poke.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def hug(ctx, member: discord.Member):
    """hug someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    hug = "**{0}Aww, I see you are lonely, take a hug <3{1}!**"

    choices = ['https://cdn.discordapp.com/attachments/447337220895145998/466226631778893824/hug-rk_6GyncG.gif',
               'https://cdn.discordapp.com/attachments/447337220895145998/466227315110576129/hug-ry6o__7D-.gif',
               'https://cdn.discordapp.com/attachments/447337220895145998/466227511165190175/hug-Bk5haAocG.gif',
               'https://cdn.discordapp.com/attachments/447337220895145998/466228974326906891/hug-BkBs2uk_b.gif',
               'https://cdn.discordapp.com/attachments/447337220895145998/466229286966394881/hug-HkfgF_QvW.gif'
               'https://cdn.discordapp.com/attachments/447337220895145998/466230001872666635/hug-BkZngAYtb.gif'
               'https://cdn.discordapp.com/attachments/447337220895145998/466230123209687040/hug-Bk5T2_1Ob.gif'
               'https://cdn.discordapp.com/attachments/447337220895145998/466230234795212802/hug-Hy4hxRKtW.gif']


    image = random.choice(choices)

    embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def slap(ctx, member: discord.Member):
    """Slap someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    slap = "**{0}Hmm, why do you want this?Slaps.{1}!**"

    choices = ['https://cdn.discordapp.com/attachments/447337220895145998/466229677300908042/slap-rJYqQyKv-.gif',
               'https://cdn.discordapp.com/attachments/447337220895145998/466229535059345408/slap-r1PXzRYtZ.gif',
               'https://cdn.discordapp.com/attachments/447337220895145998/466229453236731904/slap-SkSCyl5yz.gif'
               'https://cdn.discordapp.com/attachments/447337220895145998/466231429337055242/slap-B1-nQyFDb.gif',
               'https://cdn.discordapp.com/attachments/447337220895145998/466231614352130048/slap-HkskD56OG.gif'
               'https://cdn.discordapp.com/attachments/447337220895145998/466231875120267284/slap-By2iXyFw-.gif'
               'https://cdn.discordapp.com/attachments/447337220895145998/466232154112917504/slap-SkKn-xc1f.gif'
               'https://cdn.discordapp.com/attachments/447337220895145998/466232493889290241/slap-rJrnXJYPb.gif']


    image = random.choice(choices)

    embed = discord.Embed(description=slap.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)

    await ctx.send(embed=embed)






@bot.command(pass_context=True, no_pm=True)
async def insult(ctx, user : discord.Member=None):
    """Insult the user"""

    msg =" How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
    if user != None:
        if user.id == ctx.bot.user.id:
            user = ctx.message.author
            await ctx.send(user.mention + msg)
        else:
            await ctx.send(user.mention + msg + random.choice(msg))
    else:
        await ctx.send(ctx.message.author.mention + msg + random.choice(msg))


@bot.command()
async def profile(ctx, member: discord.Member = None):
    ''': See your profile'''
    member = member or ctx.message.author
    x = Image.open("pngs/FBI.png")
    x.load()
    async with aiohttp.ClientSession() as cs:
        async with cs.get(member.avatar_url_as(format='png')) as r:
            b = io.BytesIO(await r.read())
    x1 = Image.open(b)
    x1.load()
    font_type = ImageFont.truetype('arialbd.ttf', 15)
    font_type1 = ImageFont.truetype('arialbd.ttf', 14)
    draw = ImageDraw.Draw(x)
    x.paste(x1.resize((75, 75)), (195, 55))
    draw.text(xy=(80, 166), text=member.name, fill=(0, 0, 0), font=font_type)
    draw.text(xy=(75, 204), text=ctx.guild.name, fill=(0, 0, 0), font=font_type1)
    draw.text(xy=(68, 223), text=member.top_role.name, fill=(0, 0, 0), font=font_type1)
    x.save("profile.png")
    await ctx.send(file=discord.File("profile.png"))
    os.system("rm profile.png")

@bot.command()
async def wanted(ctx, member: discord.Member = None):
    ''': Hunt someone'''
    member = member or ctx.message.author
    x = Image.open("pngs/Wanted.png")
    x.load()
    async with aiohttp.ClientSession() as cs:
        async with cs.get(member.avatar_url_as(format='png')) as r:
            b = io.BytesIO(await r.read())
    x1 = Image.open(b)
    x3 = x.resize((400, 600))
    x3.paste(x1.resize((300, 250)), (50, 160))
    x3.save("wanted.png")
    await ctx.send(file=discord.File("wanted.png"))
    os.system("rm wanted.png")


@bot.command()
async def dog(ctx):
    ''''sends cute dog pics'''
    r = requests.get("https://dog.ceo/api/breeds/image/random").json()
    embed=discord.Embed()
    embed.set_image(url=r["message"])
    await ctx.send(embed=embed)



@bot.command(pass_context=True)
async def bite(ctx, member: discord.Member):
    """bites  someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    bite = "**{0}bites you.{1}!**"

    choices = ['https://cdn.discordapp.com/attachments/456701536912015361/466571069973856256/bite-HkutgeXob.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466571762339938304/bite-ry00lxmob.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466572007258193920/bite-H1_Jbemjb.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466572188372434964/bite-H1hige7sZ.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466572377233293322/bite-Hk1sxlQjZ.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466572552739880961/bite-rkakblmiZ.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466572804385669120/bite-BJXRmfr6-.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466573024078987284/bite-ry3pQGraW.gif']


    image = random.choice(choices)

    embed = discord.Embed(description=bite.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def cuddle(ctx, member: discord.Member):
    """cuddle  someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    cuddle = "**cuddles you.{1}!**"

    choices = ['https://cdn.discordapp.com/attachments/456701536912015361/466573538841591809/cuddle-SJn18IXP-.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466573996201082900/cuddle-r1s9RqB7G.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466574139805794306/cuddle-SJceIU7wZ.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466574279127859200/cuddle-r1XEOymib.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466574467070427156/cuddle-S1T91Att-.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466574644577697792/cuddle-BkZCSI7Pb.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466574850375548939/cuddle-Byd1IUmP-.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466575399862665216/cuddle-BkN0rIQDZ.gif']


    image = random.choice(choices)

    embed = discord.Embed(description=cuddle.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def pat(ctx, member: discord.Member):
    """pat someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    pat = "**you have been patted .{1}!**"

    choices = ['https://cdn.discordapp.com/attachments/456701536912015361/466577618771378176/pat-rktsca40-.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466577986209185812/pat-rkZbJAYKW.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466578464619626496/pat-SJva1kFv-.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466578677090484224/pat-BkJBQlckz.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466578825468182538/pat-H1s5hx0Bf.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466579159435706380/pat-rJMskkFvb.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466579338490544128/pat-rkBZkRttW.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466579500117917727/pat-Sk2FyQHpZ.gif']


    image = random.choice(choices)

    embed = discord.Embed(description=pat.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def kiss(ctx, member: discord.Member):
    """kiss someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    kiss = "**  kissed you.{1}!**"

    choices = ['https://cdn.discordapp.com/attachments/456701536912015361/466579840070582284/kiss-B1MJ2aODb.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466580423116324874/kiss-Hkt-nTOwW.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466581686591946763/kiss-r1VWnTuPW.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466582897755947017/kiss-BkUJNec1M.gif',
               'https://cdn.discordapp.com/attachments/456701536912015361/466583102047780914/kiss-Sk1k3TdPW.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466583257341755392/kiss-BJv0o6uDZ.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466583404222087168/kiss-S1PCJWASf.gif'
               'https://cdn.discordapp.com/attachments/456701536912015361/466583780736499712/kiss-SJ3dXCKtW.gif']


    image = random.choice(choices)

    embed = discord.Embed(description=kiss.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command(pass_context=True, name='youtube', no_pm=True)
async def youtube(ctx, *, query: str):
    """Search on Youtube"""
    try:
        url = 'https://www.youtube.com/results?'
        payload = {'search_query': ''.join(query)}
        headers = {'user-agent': 'Red-cog/1.0'}
        conn = aiohttp.TCPConnector()
        session = aiohttp.ClientSession(connector=conn)
        async with session.get(url, params=payload, headers=headers) as r:
            result = await r.text()
        session.close()
        yt_find = re.findall(r'href=\"\/watch\?v=(.{11})', result)
        url = 'https://www.youtube.com/watch?v={}'.format(yt_find[0])
        await ctx.send (url)
    except Exception as e:
        message = 'Something went terribly wrong! [{}]'.format(e)
        await  ctx.send(message)

@bot.command(pass_context=True, name='wikipedia', aliases=['wiki', 'w'])
async def wikipedia(ctx, *, query: str):
    """
    Get information from Wikipedia
    """
    try:
        url = 'https://en.wikipedia.org/w/api.php?'
        payload = {}
        payload['action'] = 'query'
        payload['format'] = 'json'
        payload['prop'] = 'extracts'
        payload['titles'] = ''.join(query).replace(' ', '_')
        payload['exsentences'] = '5'
        payload['redirects'] = '1'
        payload['explaintext'] = '1'
        headers = {'user-agent': 'Red-cog/1.0'}
        conn = aiohttp.TCPConnector(verify_ssl=False)
        session = aiohttp.ClientSession(connector=conn)
        async with session.get(url, params=payload, headers=headers) as r:
            result = await r.json()
        session.close()
        if '-1' not in result['query']['pages']:
            for page in result['query']['pages']:
                title = result['query']['pages'][page]['title']
                description = result['query']['pages'][page]['extract'].replace('\n', '\n\n')
            em = discord.Embed(title='Wikipedia: {}'.format(title), description=u'\u2063\n{}...\n\u2063'.format(description[:-3]), color=discord.Color.blue(), url='https://en.wikipedia.org/wiki/{}'.format(title.replace(' ', '_')))
            em.set_footer(text='Information provided by Wikimedia', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Wikimedia-logo.png/600px-Wikimedia-logo.png')
            await ctx.send(embed=em)
        else:
            message = 'I\'m sorry, I can\'t find {}'.format(''.join(query))
            await ctx.send('```{}```'.format(message))
    except Exception as e:
        message = 'Something went terribly wrong! [{}]'.format(e)
        await ctx.send('```{}```'.format(message))

class Fun():
    """fun random commands"""

    def __init__(ctx, bot):
        ctx.bot = bot
        ctx.toggle = False
        ctx.nsword = ctx.nlove = ctx.nsquat = ctx.npizza = ctx.nbribe = ctx.ndad = ctx.ncalc \
            = ctx.nbutt = ctx.ncom = ctx.nflirt = ctx.nup = 0


@bot.command(pass_context=True)
async def sword(ctx,  *, user: discord.Member):
    """Sword Duel!"""
    author = ctx.message.author
    if user.id == ctx.bot.user.id:
        await ctx.send("I'm not the fighting kind")
    else:
        await ctx.send(author.mention + " and " + user.mention + " dueled for " + str(randint(2, 120)) +
                            " gruesome hours! It was a long, heated battle, but " +
                            choice([author.mention, user.mention]) + " came out victorious!")
    ctx.counter(n)

@bot.command(pass_context=True)
async def love(ctx, user: discord.Member):
    """Found your one true love?"""
    author = ctx.message.author
    if user.id == ctx.bot.user.id:
        await ctx.send("I am not capable of loving like you can. I'm sorry." )
    else:
        await ctx.send(author.mention + " is capable of loving " + user.mention + " a whopping " +
                            str(randint(0, 100)) + "%!")
    ctx.counter(n)

@bot.command(pass_context=True)
async def squat(ctx):
    """How is your workout going?"""
    author = ctx.message.author
    await ctx.send(author.mention + " puts on their game face and does " + str(randint(2, 1000)) +
                        " squats in " + str(randint(4, 90)) + " minutes. Wurk it!")
    ctx.counter(n)

@bot.command(pass_context=True)
async def pizza(ctx):
    """How many slices of pizza have you eaten today?"""
    author = ctx.message.author
    await ctx.send(author.mention + " has eaten " + str(randint(2, 120)) + " slices of pizza today.")
    ctx.counter(n)

@bot.command(pass_context=True)
async def bribe(ctx):
    """Find out who is paying under the table"""
    author = ctx.message.author
    await ctx.send(author.mention + " has bribed " + ctx.bot.user.mention + " with " +
                        str(randint(10, 10000)) + " dollars!")
    ctx.counter(n)

@bot.command(pass_context=True)
async def daddy(ctx):
    """Pass the salt"""
    author = ctx.message.author
    await ctx.send("I'm kink shaming you, " + author.mention)
    ctx.counter(n)

@bot.command()
async def calculated(ctx):
    """That was 100% calculated!"""
    await ctx.send("That was " + str(randint(0, 100)) + "% calculated!")
    ctx.counter(n)

@bot.command()
async def butts(ctx):
    """butts"""
    await ctx.send("ლ(́◉◞౪◟◉‵ლ)")
    ctx.counter(n)

@bot.command(name="commands")
async def _commands(ctx):
    """Command the bot"""
    await ctx.send("Don't tell me what to do.")
    ctx.counter(n)

@bot.command()
async def flirt(ctx):
    """Slide into DMs"""
    await ctx.send("xoxoxoxoxo ;)) ))) hey b a b e ; ; ;))) ) ;)")
    ctx.counter(n)

@bot.command()
async def updog(ctx):
    """This is updog"""
    await ctx.send("What's updog?")
    ctx.counter(n)

@bot.command()
async def invite(ctx):
    """Invite me to your server"""
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=457903893079392256&scope=bot&permissions=2146958591")
    ctx.counter(n)
@bot.command()
async def server(ctx):
    """Join bot server"""
    await ctx.send("https://discord.gg/cRPH8VK")
    ctx.counter(n)

@bot.command(pass_context=True)
async def help(ctx):
    """: help commands"""
    embed = discord.Embed(title=f'''commands''', description=f'''pikachu bot prefix : p?''',color=discord.Colour.dark_purple())
    embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTv16_7xeYF7jboCqijoHf2SzQrBgszZ90YzWP0klBCa-dyu6TnrA')
    embed.add_field(name='Fun Commands :', value=f'''' rps 8ball bite bribe butts calculated cuddle poke daddy flirt hug insult dog kiss love pat pizza slap updog sword wanted profile ''', inline=False)
    embed.add_field(name='Admin commands :', value=f''' warn perms kick prune purge ''', inline=False)
    embed.add_field(name='pokedex :', value=f''' pokemon''', inline=False)
    embed.add_field(name='search :', value=f''' youtube wikipedia ''', inline=False)
    embed.add_field(name=' server :', value=f'''Serverinfo invite server avatar''', inline=False)
    embed.add_field(name=' Whats New :', value=f''' Now i will welcome users through DMS when they join server by default no need to set it everytime for every server''', inline=False)
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def pepe(ctx, member: discord.Member):
    """kiss someone!"""
    author = ctx.message.author.mention
    mention = member.mention

    pepe = "**  kissed you.{1}!**"

    choices = ["http://i.imgur.com/vpIyEue.png",
               "http://i.imgur.com/0koMC0v.jpg",
               "http://i.imgur.com/9Q6KMZa.png",
               "http://i.imgur.com/54xy6jr.png",
               "http://i.imgur.com/QvCngiJ.jpg",
               "http://i.imgur.com/ftWgrOE.jpg",
               "http://i.imgur.com/rhDSqRv.jpg",
               "http://i.imgur.com/89NZ3zM.jpg",
               "http://i.imgur.com/I4cIH5b.png",
               "http://i.imgur.com/GIFc4uX.png",
               "http://i.imgur.com/bgShJpZ.png",
               "http://i.imgur.com/jpfPLyn.png",
               "http://i.imgur.com/pZeYoej.png",
               "http://i.imgur.com/M8V9WKB.jpg",
               "http://i.imgur.com/ZBzHxNk.jpg",
               "http://i.imgur.com/xTyJ6xa.png",
               "http://i.imgur.com/TOozxRQ.png",
               "http://i.imgur.com/Eli5HdZ.png",
               "http://i.imgur.com/pkikqcA.jpg",
               "http://i.imgur.com/gMF8eo5.png",
               "http://i.imgur.com/HYh8BUm.jpg",
               "http://i.imgur.com/ZGVrRye.jpg",
               "http://i.imgur.com/Au4F1px.jpg",
               "http://i.imgur.com/gh36k9y.jpg",
               "http://i.imgur.com/MHDoRuN.png",
               "http://i.imgur.com/V3MJfyK.png",
               "http://i.imgur.com/QGGTipc.jpg",
               "http://i.imgur.com/PRFrTgz.png",
               "http://i.imgur.com/9UBJrwM.jpg",
               "http://i.imgur.com/WQY9Vhb.jpg",
               "http://i.imgur.com/sIbQdou.jpg",
               "http://i.imgur.com/LlUMg00.jpg",
               "http://i.imgur.com/MmijlWa.png",
               "http://i.imgur.com/i0CrtrX.png",
               "http://i.imgur.com/Dfpudwp.jpg",
               "http://i.imgur.com/hhg0wVF.gif",
               "http://i.imgur.com/7VDiIHN.jpg",
               "http://i.imgur.com/nxvXpNV.jpg",
               "http://i.imgur.com/DZYEjrW.gif",
               "http://i.imgur.com/mnyQ0Rh.jpg",
               "http://i.imgur.com/aHawbbs.jpg",
               "http://i.imgur.com/g8cCHV7.jpg",
               "http://i.imgur.com/E2cMU7Y.jpg",
               "http://i.imgur.com/PkmcgGF.jpg",
               "http://i.imgur.com/7qLQ1xl.jpg",
               "http://i.imgur.com/7qLQ1xl.jpg",
               "http://i.imgur.com/arSsPwf.png",
               "http://i.imgur.com/xcYh4iC.png",
               "http://i.imgur.com/9692WND.jpg",
               "http://i.imgur.com/diAK5Nu.jpg",
               "http://i.imgur.com/zDs0tRW.jpg",
               "http://i.imgur.com/PEM87nV.jpg",
               "http://i.imgur.com/zlCzlND.jpg",
               "http://i.imgur.com/n0OHxDl.jpg",
               "http://i.imgur.com/TQRf1WH.png",
               "http://i.imgur.com/zi9ad15.jpg",
               "http://i.imgur.com/b8A6Qke.jpg",
               "http://i.imgur.com/YuLapEu.png",
               "http://i.imgur.com/fWFXkY1.jpg",
               "http://i.imgur.com/i5vNvWU.png",
               "http://i.imgur.com/oXwUwtJ.jpg",
               "http://i.imgur.com/hadm4jV.jpg",
               "http://i.imgur.com/gbCvkqo.png",
               "http://i.imgur.com/wDiiWBG.jpg",
               "http://i.imgur.com/Mvghx4V.jpg",
               "http://i.imgur.com/SnTAjiJ.jpg",
               "http://i.imgur.com/QvMYBnu.png",
               "http://i.imgur.com/WkzPvfB.jpg",
               "http://i.imgur.com/PfAm4ot.png",
               "http://i.imgur.com/SIk4a45.png",
               "http://i.imgur.com/aISFmQq.jpg",
               "http://i.imgur.com/sMQkToE.png",
               "http://i.imgur.com/7i3cBrP.png",
               "http://i.imgur.com/1oMSz6e.png",
               "http://i.imgur.com/nVCRnRv.png",
               "http://i.imgur.com/FzWmxmi.jpg",
               "http://i.imgur.com/rpUI20F.jpg",
               "http://i.imgur.com/FDmnFDZ.jpg",
               "http://i.imgur.com/40Z1Yyg.jpg",
               "http://i.imgur.com/osy5Nu4.png",
               "http://i.imgur.com/4w81MSS.jpg",
               "http://i.imgur.com/qRXQFYa.png",
               "http://i.imgur.com/A1af62j.jpg",
               "http://i.imgur.com/wOc6fUe.jpg",
               "http://i.imgur.com/Z6ILiJ4.jpg",
               "http://i.imgur.com/537UpEJ.jpg",
               "http://i.imgur.com/HDc6kko.png",
               "http://i.imgur.com/oyLpuXq.jpg",
               "http://i.imgur.com/iCmGtJS.jpg",
               "http://i.imgur.com/MjpnlQm.png",
               "http://i.imgur.com/c6MWRQ9.jpg"]


    image = random.choice(choices)

    embed = discord.Embed(description=pepe.format(author, mention), colour=discord.Colour(0xba4b5b))
    embed.set_image(url=image)


@bot.command(pass_context=True)
async def rps(ctx, choice):
    """"""
    choices = ["rock", "paper", "scissors"]
    await ctx.send("You chose {} | CPU chose {}".format(choice, random.choice(choices)))





@bot.listen()
async def on_member_join(member):
    await member.send(f"{member.name}Welcome to {member.guild.name}")

@bot.event
async def on_ready():
    options = ('help via p?help', 'to ꧁ uchiha꧂#2508', f'on {len(bot.guilds)} servers')
    while True:
        await bot.change_presence(activity=discord.Streaming(name=random.choice(options), url='https://www.twitch.tv/cohhcarnage'))
        await asyncio.sleep(10)





bot.run("NDU3OTAzODkzMDc5MzkyMjU2.DlG8fw.rvN6FqhbTm1HUqyqtgDQF_i1a_A")