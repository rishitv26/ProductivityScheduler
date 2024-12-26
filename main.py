from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import query

# load token:
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# bot stuff
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# message stuff
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('intents not enabled')
        return
    
    if is_private := user_message[0] == ":": # if user wants message privately, message him privately
        user_message = user_message[1:]
        
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)        

# generate all responses here.
def get_response(user_input: str) -> str:
    user_input: str = user_input.lower()
    try:
        if user_input == '':
            return 'wat'
        else:
            new_task = query.parse_query(user_input)
            # todo ALLOCATE IN CALENDAR; if cannot be allocated for some reason let user know AND save it in 'to_allocated'
            return "generated task successfully: " + str(new_task)
    except Exception as e:
        print(e)
    
    return "bad format OR not implemented yet :)"

# connecting discord activities with python functions we just defined.
@client.event
async def on_ready() -> None:
    print("now up and running.")
    # todo: load notion/google calender stuff

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return # if this message is the bot, dont bother doing anything
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    print(f'[{channel}] {username}: {user_message}')
    await send_message(message, user_message)
    
# python entry point for code.
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()