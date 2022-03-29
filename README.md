# chatbot

AI Discord chat bot using OpenAI fine-tuning

## Installation

`pip install -r requirements.txt`

`pip install --upgrade openai`

`cp .env.example .env`

## Setup

### Create a Discord Bot:
1. Navigate to https://discord.com/developers 
2. Add an application
3. Click on the bot tab to add a bot to the application
4. Click on OAuth2 -> URL Generator and select bot to generate a unique URL to add the bot to a server where you have admin privileges
<img width="884" alt="Screen Shot 2021-11-20 at 4 39 33 PM" src="https://user-images.githubusercontent.com/1606986/142744981-06ef3d8d-61a2-4fa0-b9ab-441f3a15de8b.png">
5. Save your bot's token (Under the bot tab, as pictured below) as DISCORD_TOKEN in .env
<img width="1255" alt="Screen Shot 2022-03-29 at 3 51 11 PM" src="https://user-images.githubusercontent.com/1606986/160719544-151966fb-6b21-4a2b-afe0-60a83a82faff.png">

### Populate the required variables in `.env`:
- `DISCORD_TOKEN`: As specified above, the unique token for the Discord bot you've created
- `BOT_USERNAME`: Sets the command which the bot will respond to. For example if `BOT_USERNAME = test`, then the bot will respond to messages starting with `!test`
- `OPENAI_KEY`: OpenAI API Key
- `OPENAI_MODEL`: ID of the OpenAI model for the bot to use. This can be a standard model such as `curie` or a custom model you have fine-tuned based on chat history.

## Usage

`python bot.py` to start the bot

- In a discord server with the bot, send the message `!history` to have the bot log the current channel's history, by user. 

  - This will create `.jsonl` files for each user in the channel, which can then be input to OpenAI's fine-tuning feature.

- Select a user you'd like to model the AI on, and prepare the data:

`openai tools fine_tunes.prepare_data -f channel_[channel_name]/[user].jsonl`

- It is recommended to accept all of the edits that OpenAI suggests - these will be saved in a new file. Finally, submit the prepared data to OpenAI:

`openai api fine_tunes.create -t "channel_[channel_name]/[user]_prepared.jsonl" --batch_size 1`

- Once the model is created, update `.env` to use this model, and interact with the bot using `![BOT_USER]`. For example, if your bot is based on the Discord user `test`, then the bot will respond to messages starting with `!test`


## Questions?

Contact tv#3636 on Discord with any questions
