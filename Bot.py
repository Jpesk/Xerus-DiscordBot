#! python3
from __future__ import print_function
import discord
global tmp
import random
import requests
import cleverbot
import urllib.request
import json

#8ball Choices
choices = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely',
           'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good',
           'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later',
           'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
           "Don't count on it", 'My reply is no', 'My sources say no',
           'Outlook not so good', 'Very doubtful', 'This is stupid' ]

client = discord.Client()
cleverbot_client = cleverbot.Cleverbot()

# reads the credentials file for login info
# format -- example@email.com:password
f_creds = open("credentials.txt")
creds = f_creds.read().split(":")
f_creds.close()

# Reads commands file
f_commands = open("commands")
commands = f_commands.read()
commands_discord = ('```' + commands + '```')
f_commands.close()

# about
f_about = open("About")
about = f_about.read()
about_discord = ('```' + about + '```')
f_about.close()

#csgoskins
f_Csgo = open("Csgoskins.txt")
Csgoskins = f_Csgo.read().split(":")
f_Csgo.close()

#wears
Wears = ['Battle Scared', 'Well Worn', 'Field Tested', 'Minimal Wear',
           'Factory New' ]

@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(server, fmt.format(member, server))

# Basic information
@client.event
async def on_ready():
    print('Welcome!!')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Connected to')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(':test'):
        tmp = await client.send_message(message.channel, 'It works!!')
    elif message.content.startswith(':about'):
        tmp = await client.send_message(message.channel, message.author.mention + about_discord)
    elif message.content.startswith(':id'):
        tmp = await client.send_message(message.channel, message.author.mention + " Your id is " + message.author.id)
    elif message.content.startswith(':name'):
        tmp = await client.send_message(message.channel, "My name is " + client.user.name)
    elif message.content.startswith(':help'):
         msg = await client.send_message(message.author, "Hi")
         msg = await client.send_message(message.author, "I am xerus")
         msg = await client.send_message(message.author, "Here is the server where i am from -- https://discord.gg/0kvPIGKKEACoKQ8C")
         msg = await client.send_message(message.author, commands_discord)
         tmp = await client.send_message(message.channel, 'Ok,' + message.author.mention + "I sent you a list of commands and other information about me via DM!")
    elif message.content.startswith(':red'):
        msg = await client.send_message(message.channel, message.author.mention)
    elif message.content.startswith(':flip'):
        a = ["Heads!", "Tails!"]
        msg = await client.send_message(message.channel, random.choice(a))
    elif message.content.startswith(':join'):
        f_server = message.content.split("g/")
        try:
            server_id = f_server[1]
        except IndexError:
            tmp = await client.send_message(message.channel,
                                            message.author.mention + ' The server Url Provided was Invalid')
        try:
            await client.accept_invite(server_id)
            tmp = await client.send_message(message.channel, 'Server Joined!!')
        except UnboundLocalError:
            tmp = await client.send_message(message.channel, )
    elif message.content.startswith(':guess'):
        await client.send_message(message.channel, 'Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))
    elif message.content.startswith(':cat'):
        cat_image = requests.get("http://thecatapi.com/api/images/get")
        await client.send_message(message.channel, cat_image.url)
    elif message.content.startswith(':talk'):
        cb1 = cleverbot.Cleverbot()
        unsplit = message.content.split("talk")
        split = unsplit[1]
        answer = (cb1.ask(split))
        tmp = await client.send_message(message.channel, answer)
    elif message.content.startswith(':8ball '):
        tmp = await client.send_message(message.channel,  message.author.mention + ":crystal_ball: " + random.choice(choices) + " :crystal_ball:")
    elif message.content.startswith(':8ball'):
        tmp = await client.send_message(message.channel, message.author.mention + " You need to ask a question")
    elif message.content.startswith(':head'):
        tmp = await client.send_message(message.channel, discord.version_info)
    elif message.content.startswith(':drop'):
        tmp = await client.send_message(message.channel, message.author.mention + "received a " + random.choice(Csgoskins) + " " +"(" + random.choice(Wears) + ")")
    elif message.content.startswith(':google '):
        site = message.content.split(":google ")
        site1 = "https://www.google.com.au/search?site=&source=hp&q=" + site[1]
        print(site1)
        tmp = await client.send_message(message.channel, site1)
    elif message.content.startswith(':weather '):
        location = message.content.split(":weather ")
        location2 = location[1]
        weather = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q={" + location2 + "}&APPID=fc75f2216dd9e5fde9ec6d0de124b914").read()
        tmp = await client.send_message(message.channel, weather)

client.run(creds[0], creds[1])
