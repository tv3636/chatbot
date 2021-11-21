import os, discord, openai, time, json, re
from dotenv import load_dotenv
from discord.ext import tasks
from collections import defaultdict

load_dotenv()

# Discord Constants
discordToken = os.getenv('DISCORD_TOKEN')
botUser = os.getenv('BOT_USERNAME')
client = discord.Client()

# OpenAI Constants
openai.api_key = os.environ.get('OPENAI_KEY')
model = os.environ.get('OPENAI_MODEL')
completion = openai.Completion()
delimiter = '\n###\n'

# History Constants
directory_prefix = "./channel_history_"
last_n = 10

def ask(sender, question):
	global model
	
	response = completion.create(
		prompt=sender + ': ' + question + '\n' + delimiter + '\n', 
		model=model, 
		temperature=0.7,
		top_p=1,
		stop=[" END"],
		frequency_penalty=0, 
		presence_penalty=0.5, 
		best_of=1,
		max_tokens=64
	)

	return response.choices[0].text.strip().replace(delimiter, '')

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

	# Bot response with OpenAI tuned model

	if not message.author.bot and botUser and message.content.split()[0] == '!' + botUser:

		sender = str(message.author).split('#')[0]
		text = ' '.join(message.content.split()[1:])
		aiResponse = ask(sender, text)

		print(aiResponse.split('\n' + botUser + ':'))

		for response in aiResponse.split('\n' + botUser + ':'):
			validResponse = True
			
			for token in response.split():
				if token[-1] == ":":
					validResponse = False
			
			if not validResponse:
				break
			elif response:
				if '<@' in response:
					for match in re.findall('<@!?([0-9]*)>', response):
						username = await client.fetch_user(int(match))
						response = response.replace(response[response.find('<'):response.find('>') + 1], '@' + str(username)[:str(username).find('#')])

				if '\n' in response:
					for out in response.split('\n'):
						if out and out != '###' and out[0] != '<':
							await message.channel.send(out)
							time.sleep(.2)
				else:
					if response and response != '###' and response[0] != '<':
						await message.channel.send(response)
						time.sleep(.2)
	
	# Collect chat history to build fine-tuning datasets
	"""
	elif not message.author.bot and message.content.split()[0] == '!history':
		last = []
		lastSender = None
		thisResponse = ''
		channelName = str(message.channel)

		if not os.path.exists(directory_prefix + channelName):
			os.makedirs(directory_prefix + channelName)

		async for msg in message.channel.history(limit=None, oldest_first=True):
			sender = str(msg.author).split('#')[0]
			context = ''

			print(sender, ': ', msg.content)

			if sender != lastSender and thisResponse:

				switch = False
				for text in reversed(last[:-1]):
					if switch or (not switch and text['author'] != lastSender):
						context = text['author'] + ': ' + text['message'] + '\n' + context
						switch = True
				
				f = open(directory_prefix + channelName + '/' + lastSender.replace('/', '') + ".jsonl", "a")
				f.write(
					str(
						json.dumps(
							{
								'prompt': context,
								'completion': thisResponse.strip()
							},
							ensure_ascii=False
						)
					)
					+ '\n'
				)

				thisResponse = sender + ': ' + msg.content + '\n'
			else:
				thisResponse += sender + ': ' + msg.content + '\n'

			lastSender = sender
			last.append({'author': sender, 'message': msg.content})

			if len(last) > last_n:
				last = last[1:]
	"""


client.run(discordToken)
