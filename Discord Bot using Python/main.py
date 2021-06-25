import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
client=discord.Client()


sad_words=["sad","depressed","unhappy","miserable","depressing"]

starter_encouragements=[
  "Cheer up!",
  "Hang in there",
  "You are a great person/bot!"
  ]


if "responding" not in db.keys():
  db["responding"]= True



def get_quote():
  #picks up random quotes using the api 
  response=requests.get("https://zenquotes.io/api/random")
  json_data= json.loads(response.text)
  #stores them in the database
  quote=json_data[0]['q'] + "-" + json_data[0]['a']
  #displayes the quote followed by a hyphen and the authors Name
  return (quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements= db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements

  else:
    db["encouragements"]=[encouraging_message]


def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]= encouragements



@client.event
#this callback function will be called when the bot is ready to use
async def on_ready():
  print('We are logged in as {0.user}'.format(client))


@client.event
#these functions are directly linked to the discord.pi library
#which is looking for these and can be implemented easily
async def on_message(message):
  #it takes message as an input and doesn't return anything if the messsage is from ourselves
  if message.author==client.user:
    return

  msg=message.content
  #if message.content.startswith('$hello'):
    #if it senses that someones has sent $hello it replies back with Hello!
  if msg.startswith('$inspire'):
    quote=get_quote()
    #gets quote and stores in quote
    #then passes the quote and sends it to the channel when triggered with $inspire
    await message.channel.send(quote)

  if db["responding"]:
    options=starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])


    if any(word in msg  for word in sad_words):
      await message.channel.send(random.choice(options))


  if msg.startswith("$new"):
    encouraging_message= msg.split("$new",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)


  if msg.startswith("$list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value= msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"]= True
      await message.channel.send("responding is on")
    else:
      db["responding"]= False
      await message.channel.send("responding is off")


keep_alive()
#used the key and token thru secret environment since its public and can be used by anyone 
client.run(os.environ['TOKEN'])
