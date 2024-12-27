from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from tasks import Task
import query
import events

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
            new_task: Task = query.parse_query(user_input)
            # get all times we are free:
            free_times: list = events.get_free_time_with_durations(new_task)
            
            # compare all times and find ones fit for task:
            suitable_times: list = []
            for i in free_times:
                if i[2] >= new_task.duration:
                    # suitable
                    suitable_times.append([i[0], i[1]])
            
            if len(suitable_times) == 0:
                return "sorry, could not allocate task because of no space in schedule, increase due date?"
            
            # allocate tasks for that day.
            suitable_time: list = [0, 0]
            if new_task.priority == 0: # doesnt matter do it the last day
                suitable_time[0] = suitable_times[-1][0]
                suitable_time[1] = suitable_times[-1][1]
            else: # assign as early as possible
                suitable_time[0] = suitable_times[0][0]
                suitable_time[1] = suitable_times[0][1]
            
            # save event in calendar: TODO
            events.save_in_calendar(suitable_time[0], suitable_time[1], new_task)
            
            # return success message
            return "generated task successfully: " + str(new_task)
    except Exception as e:
        print(e)
    
    return "bad format OR not implemented yet :)"

# connecting discord activities with python functions we just defined.
@client.event
async def on_ready() -> None:
    print("now up and running.")

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