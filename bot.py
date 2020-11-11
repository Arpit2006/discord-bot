import os
import random
import discord
import requests
from datetime import date
date_today = str(date.today)

GUILD = "arpit's server"

TOKEN = 'your token here'

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
  
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    hi = 'hi' 
    
    if message.content == hi:
        await message.channel.send('hello')
    if message.content.startswith('http'):
        await message.delete()
        await message.channel.send('please dont send links this is a warning to you ')
    if message.content.startswith('!'):
        if message.content == '!rolldice':
            await message.channel.send(f'you rolled a {random.randint(0,6)} ')
        if message.content.startswith('!news'):
            topic = message.content[5:]
            
        
            main_url = f"http://newsapi.org/v2/everything?q={topic}&from={date_today}&sortBy=publishedAt&apiKey={your api key}"

            # fetching data in json format 
            open_bbc_page = requests.get(main_url).json() 

            # getting all articles in a string article 
            article = open_bbc_page["articles"] 

            # empty list which will 
            # contain all trending news 
            results = [] 
            
            for ar in article: 
                results.append(ar["title"]) 
                
            for i in range(len(results)): 
                
                # printing all trending news 
                await message.channel.send(f'{i+1}.{results[i]}') 
		
        if message.content == '!help':
            await message.channel.send('this is the Av5051 bot
 \n it has some commands like \n if you type "hi" it will tell hello')
            await message.channel.send('some other commands are "!rolldice" and "!news"')
    if message.content == 'how u doing':
        await message.channel.send('im nice thanks for asking')

    


    
client.run(TOKEN)
