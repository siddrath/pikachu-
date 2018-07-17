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
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

  @bot.command(passcontext=True)
    async def youtube(self, ctx, *, youtube):
        ': Search YouTube '

        query_string = urllib.parse.urlencode({
            'search_query': youtube,
        })
        html_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall('href=\\"\\/watch\\?v=(.{11})',
                                    html_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

    @bot.command(
        name="pokemon",
        aliases=["Pokemon", " pokemon", " Pokemon", "info", " info"])
    async def pokemon(self, ctx, *, pokemon):
        ''': Check info about pokemon'''
        from pokedex import pokedex
        pokedex = pokedex.Pokedex(
            version='v1',
            user_agent='ExampleApp (https://example.com, v2.0.1)')
        x = pokedex.get_pokemon_by_name(f'''{pokemon}''')
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



def setup(bot):
    bot.add_cog(BAsearch(bot))
