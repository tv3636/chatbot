# chatbot

AI Discord bot using OpenAI fine-tuning

## Installation

`pip install -r requirements.txt`

`pip install --upgrade openai`

`cp .env.example .env`

## Usage

`python bot.py` to run the bot

Populate the variables in the .env file as needed. To run the Discord bot, you will need `DISCORD_TOKEN` and `BOT_USERNAME`. For OpenAI, `OPENAI_KEY`, and once you have a fine-tuned model, `OPENAI_MODEL`. 

You may also use a standard model instead - to do so, update the `completion.create` in bot.py to use `engine` rather than `model` as specified in the OpenAI documentation.

To add to Discord: 
1. Navigate to https://discord.com/developers 
2. Add an application
3. Click on the bot tab to add a bot to the application
4. Click on OAuth2 -> URL Generator and select bot to generate a unique URL to add the bot to a server where you have admin privlieges
<img width="884" alt="Screen Shot 2021-11-20 at 4 39 33 PM" src="https://user-images.githubusercontent.com/1606986/142744981-06ef3d8d-61a2-4fa0-b9ab-441f3a15de8b.png">

- Once the bot is in Discord, send a message `!history` to have the bot log a channel's history, by user. 

  - This will create `.jsonl` files for each user in the channel, which can then be input to OpenAI's fine-tuning feature.

- Select the user you'd like to model the AI on, and prepare the data:

`openai tools fine_tunes.prepare_data -f channel_[channel_name]/[user].jsonl`

- It is recommended to accept all of the edits that OpenAI suggests - these will be saved in a new file. Finally, submit the prepared data to OpenAI:

`openai api fine_tunes.create -t "channel_[channel_name]/[user]_prepared.jsonl" --batch_size 1`

- Once the model is created, update `.env` to use this model, and interact with the bot using `![BOT_USER]`!
