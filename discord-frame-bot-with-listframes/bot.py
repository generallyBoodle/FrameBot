import os
import discord
from discord.ext import commands
from discord.ui import View, Select
from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

bot.remove_command("help")
@bot.command()
async def help(ctx):
    help_text = """
**🖼 FrameBot Commands**

`!frame` – Apply a frame based on your top server role  
`!frame @user` – Apply a frame to someone else's avatar  
`!listframes` – Preview available frames using a dropdown

**🔧 How It Works**
• The bot looks in the `frames/` folder for PNG files named after role names  
• If no matching role frame is found, it uses `default.png`

**📂 Example Frames Folder**
frames/ ├── admin.png ├── vip.png └── default.png

Want to add more frames? Just name them after server roles and drop them into the folder!
"""
    await ctx.send(help_text)

@bot.command()
async def frame(ctx, user: discord.Member = None):
    user = user or ctx.author
    role_names = [r.name.lower() for r in user.roles if r.name != "@everyone"]
    chosen_role = role_names[-1] if role_names else "default"
    frame_path = f"frames/{chosen_role}.png"

    try:
        frame_image = Image.open(frame_path).convert("RGBA")
    except:
        try:
            frame_image = Image.open("frames/default.png").convert("RGBA")
        except:
            await ctx.send("❌ Could not load any frame.")
            return

    avatar_url = user.avatar.url
    response = requests.get(avatar_url)
    avatar_img = Image.open(BytesIO(response.content)).convert("RGBA")
    avatar_img = avatar_img.resize(frame_image.size)

    combined = Image.alpha_composite(avatar_img, frame_image)
    buffer = BytesIO()
    combined.save(buffer, format="PNG")
    buffer.seek(0)

    await ctx.send(file=discord.File(fp=buffer, filename="framed_avatar.png"))

class FrameSelect(discord.ui.Select):
    def __init__(self, user):
        self.user = user
        frame_files = [f for f in os.listdir("frames") if f.endswith(".png")]
        options = [discord.SelectOption(label=f[:-4]) for f in frame_files]

        super().__init__(
            placeholder="Choose a frame...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_frame = self.values[0]
        frame_path = f"frames/{selected_frame}.png"

        try:
            frame_image = Image.open(frame_path).convert("RGBA")
        except:
            await interaction.response.send_message("❌ Failed to load frame.", ephemeral=True)
            return

        avatar_url = self.user.avatar.url
        response = requests.get(avatar_url)
        avatar_img = Image.open(BytesIO(response.content)).convert("RGBA")
        avatar_img = avatar_img.resize(frame_image.size)

        combined = Image.alpha_composite(avatar_img, frame_image)
        buffer = BytesIO()
        combined.save(buffer, format="PNG")
        buffer.seek(0)

        await interaction.response.send_message(
            content=f"🖼 Frame `{selected_frame}` applied!",
            file=discord.File(fp=buffer, filename="framed_avatar.png")
        )

class FrameView(View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.add_item(FrameSelect(user))

@bot.command()
async def listframes(ctx, user: discord.Member = None):
    user = user or ctx.author
    frame_files = [f for f in os.listdir("frames") if f.endswith(".png")]

    if not frame_files:
        await ctx.send("⚠️ No frame files found in the `frames/` folder.")
        return

    embeds = []
    for f in frame_files:
        file_path = os.path.join("frames", f)
        file = discord.File(file_path, filename=f)
        embed = discord.Embed(title=f"🖼 Frame: {f[:-4]}")
        embed.set_image(url=f"attachment://{f}")
        embeds.append((embed, file))

    await ctx.send("🎨 Available Frames (see images below):")

    for embed, file in embeds:
        await ctx.send(embed=embed, file=file)

    await ctx.send(
        f"🔽 Now select a frame to preview it on {user.display_name}’s avatar:",
        view=FrameView(user)
    )


bot.run(TOKEN)
