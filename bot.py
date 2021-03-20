#import,variable declearation
import random 
import asyncio
import DiscordUtils
import requests
import aiohttp
import json
import keep_alive
from mcstatus import MinecraftServer
import discord
from discord.ext import commands
from datetime import date
date_today = str(date.today)
serverip = 'altitudesmp.ga'


import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix = '>')
@bot.event
async def on_ready():
    print('bot on')
    await bot.change_presence(status=discord.Status.online,activity = discord.Game('altitudesmp.ga' ))   
@bot.event
async def on_member_join(member):
    
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
@bot.command(aliases = ["server"])
async def _server(ctx):
	server = MinecraftServer.lookup(serverip)
	status = server.status()
	embed=discord.Embed(title="**SERVER STATUS**", description="THIS IS THE SERVER STATUS", color=0x00ff00)
	embed.add_field(name="PLAYERS", value="{}".format(status.players.online), inline=False)
	embed.add_field(name="SERVER PING", value="{}".format(status.latency), inline=False)
	await ctx.send(embed=embed)
	



@bot.command(aliases = ["ip"],pass_context = True)
async def _ip(ctx):
	embed=discord.Embed(title="IP", description="THIS IS THE SERVER IP", color=0x00ff00)
	embed.add_field(name="IP", value="{}".format(serverip), inline=False)
	embed.add_field(name="VERSION", value="1.16.4", inline=False)
	await ctx.send(embed=embed)
@bot.command(aliases = ['report'])
async def _report(ctx):
	channel = bot.get_channel(809339599397978122)	
	main_content = ctx.message.content[7:]
	embed=discord.Embed(title="Report", description="your report has been succesfully sent", color=0x00ff00)
	embed.add_field(name="report by", value=ctx.message.author.mention, inline=False)
	embed.add_field(name="report reason", value=main_content, inline=False)
	await channel.send(embed=embed)
	await ctx.send(embed=embed)
	
@bot.command(aliases = ['suggest'])
async def _suggest(ctx):
	channel = bot.get_channel(817434581853798470)
	main_content = ctx.message.content[8:]
	embed=discord.Embed(title="suggest", description="your suggestion has been sent succesfully", color=0x00ff00)
	embed.add_field(name="suggestion by", value=ctx.message.author.mention, inline=False)
	embed.add_field(name="suggestion", value=main_content, inline=False)
	await channel.send(embed=embed)
	await ctx.send(embed=embed)
@bot.command(aliases = ['rps'])
async def _rps(ctx):
	rps_string = ['rock','paper','scizor']
	embed=discord.Embed(title="rps", description="rock papers scissor", color=0x00ff00)
	embed.add_field(name="game played by", value=ctx.message.author.mention, inline=False)
	embed.add_field(name="altitude chose", value=random.choice(rps_string), inline=False)
	await ctx.send(embed=embed)

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"


@bot.command()
@commands.guild_only()
async def serverinfo(ctx):
    embed = discord.Embed(title="SERVER INFO", description="av5051", color=0x00ff00)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.set_thumbnail(url = str(ctx.guild.icon_url))
    embed.add_field(name = f"Information About **{ctx.guild.name}**: ", value = f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}** \n:white_small_square: Location: **{ctx.guild.region}** \n:white_small_square: Creation: **{ctx.guild.created_at.strftime(format)}** \n:white_small_square: Members: **{ctx.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
    await ctx.send(embed=embed)
@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
music = DiscordUtils.Music()

@bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect() #Joins author's voice channel

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Playing {song.name}")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Queued {song.name}")

@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused {song.name}")

@bot.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name}")

@bot.command()
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.send("Stopped")

@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for {song.name}")
    else:
        await ctx.send(f"Disabled loop for {song.name}")

@bot.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")

@bot.command()
async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@bot.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")

@bot.command()
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol / 100)) # volume should be a float between 0 to 1
    await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

@bot.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")
def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]

@bot.command()
@commands.has_permissions(kick_members=True)
async def giveaway(ctx):
  await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

  questions = ["Which channel should it be hosted in?", "What should be the duration of the giveaway? (s|m|h|d)", "What is the prize of the giveaway?"]

  answers = []

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  for i in questions:
    await ctx.send(i)

    try:
      msg = await bot.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
      await ctx.send('You didn\'t answer in time, please be quicker next time!')
      return
    else: 
      answers.append(msg.content)

  try:
    c_id = int(answers[0])
  except:
    await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
    return

  channel = bot.get_channel(c_id)

  time = convert(answers[1])
  if time == -1:
    await ctx.send(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
    return
  elif time == -2:
    await ctx.send(f"The time just be an integer. Please enter an integer next time.")
    return
  
  prize = answers[2]

  await ctx.send(f"The giveaway will be in {channel.mention} and will last {answers[1]} seconds!")

  embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

  embed.add_field(name = "Hosted by:", value = ctx.author.mention)

  embed.set_footer(text = f"Ends {answers[1]} from now!")

  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("🎉")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))

  winner = random.choice(users)

  await channel.send(f"Congratulations! {winner.mention} won the prize: {prize}!")


@bot.command()
@commands.has_permissions(kick_members=True)
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
  try:
    new_msg = await channel.fetch_message(id_)
  except:
    await ctx.send("The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))
  winner = random.choice(users)
  await channel.send(f"Congratulations the winner is: {winner.mention} for the giveaway rerolled")

keep_alive.keep_alive()

bot.run(TOKEN)
