import MySQLdb
import discord
import asyncio
import requests
from discord.ext import commands
from discord import app_commands

db = MySQLdb.connect(
    host="discord_mysql",
    user="",
    passwd="",
    db="user_data"
)

cursor = db.cursor()

db_setup = """
    CREATE TABLE IF NOT EXISTS auth_keys (
        discordID BIGINT NOT NULL,
        authKey VARCHAR(100) NOT NULL,
        
        CONSTRAINT auth_keys_pk
            PRIMARY KEY (discordID)
        );
"""
cursor.execute(db_setup)

newUser = """
    INSERT INTO auth_keys (discordID, authKey)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        discordID = VALUES(discordID), authKey = VALUES(authKey);
"""

getUsers = """
    SELECT discordID, authKey FROM auth_keys
"""

class Client(commands.Bot):
    def get_data(self, token): # get assignment info via api token
        response = []
        authentication = {
            'Authorization': 'Token ' + token
        }
        assignmentData = requests.get('http://assignme.fyi/accounts/api/?format=json', headers=authentication).json()
        for assignment in assignmentData:
            due = assignment['days_until_due']
            name = assignment['title']
            if 0 < due < 2:
                response.append(f'{name} is due in {due} day(s).')
        return response
    async def send_assignments(self, id, key): # asyncio task to get send assignment info
        user = await self.fetch_user(id)
        while True:
            response = self.get_data(key)
            for each in response:
                await user.send(f'{each}')
                await asyncio.sleep(2)
            await asyncio.sleep(86400)
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.tree.sync()
        cursor.execute(getUsers)
        users = cursor.fetchall()
        for id, key, in users:
            self.loop.create_task(self.send_assignments(id, key)) #create a asyncio task, which sends a DM with assignment info to all users in database

intents = discord.Intents.default() # define default permissions
#intents.message_content = True
client = Client(command_prefix="!", intents=intents) # link client with intent (pemissions)

@client.tree.command(name="set-token", description="Set your assignMe token to configure bot", guild=discord.Object(id=1096570772107055185))
async def set_token(interaction: discord.Interaction, token: str):
    discord_id = interaction.user.id
    cursor.execute(newUser, (discord_id, token)) # create new user via SQL
    db.commit()
    client.loop.create_task(client.send_assignments(discord_id, token)) # if asyncio task is already running, then this basically just refreshes it with the new user added to the database, so they get their data too.
    await interaction.response.send_message(f'Token set: {token}. Check your DMs!', ephemeral=True)

client.run('') # run client with token