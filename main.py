import discord
import time

import pickle
'''
i am actually sorry for the code ahead.
i was on some strong stuff when creating this i tell ya.
so i am sorry but the commenting is pretty trash since i don't know what most of it does myself.

basically it levels people up when they help people, the bot knows who is helping because the person helped will run the command /bump [@user], you get to the next level when you get bumped as many times as squared of the next level 
oh and ignore pickles ik its bad practice and i should use a database but i couldnt be bothered.
'''

class MyClass:
    def __init__(self):
        try:
            with open('levels.pkl', 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

    def update_or_add(self, name):
        if name not in self.data:
            # If the name does not exist, add it with two zeros
            self.data[name] = (1, 1)
        else:
            # If the name exists, update the values
            current_value = self.data[name]
            new_counter = current_value[0] + 1
            new_level = current_value[1] # Initialize new_level with the current level
            if new_counter >= (current_value[1] + 1) ** 2:
                new_level = current_value[1] + 1
            self.data[name] = (new_counter, new_level)
        self.save_data()
        return self.data[name]
    '''
    def check_values(self, name):
        # This method returns the current values without updating them
        current_value = self.data[name]
        return current_value[0], current_value[1]
'''
    def save_data(self):
        with open('levels.pkl', 'wb') as f:
            pickle.dump(self.data, f)

levels = MyClass()


# Record the start time
start_time = time.perf_counter()
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # dont talk to itself
        if message.author == self.user:
            return

        # ping used to test if the bot is working. it returns time since downtime and the latency to the user
        if message.content == 'ping':
            latency = round(client.latency * 1000)
            end_time = time.perf_counter()
            timer = end_time - start_time
            timer = round(timer / 3600, 2)
            message_text = f"pong! \n```latency: {latency} ms \ntime since downtime: {timer} hours```"
            await message.channel.send(message_text)
            
        # bump user
        elif message.content.startswith('/bump'):
            name = message.content.split(' ', 1)[1]
            print(name, " bumped")
            counter, level = levels.update_or_add(name)
            nxt_lvl2 = (level + 1) ** 2
            to_send = f"thank you for helping: {name} your current help count is: {counter}, which is {nxt_lvl2 - counter} away from the next level, {level + 1}"
            await message.channel.send(to_send)

        # level check
            '''
        elif message.content.startswith('/rank'):
            print(message.author.name, " checked rank")
            counter, level = levels.check_values(message.author)
            nxt_lvl2 = (level + 1) ** 2
            to_send = f"hello {message.author.name} ```Bumps: {counter} \nLevel: {level} \nTo next level: {nxt_lvl2 - counter}```"
            await message.channel.send(to_send)
            '''

#start discord 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('TOKEN')
