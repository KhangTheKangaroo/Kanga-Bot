import discord
import json
import datetime
from Settings import bot, discord_bot_token
from datetime import timedelta, datetime, timezone

user_shop_pages = {}

with open('shop.json', 'r') as file:
    shop_pages = json.load(file)


def create_embed(page_content, user):
    embed1 = discord.Embed(
        colour=0x5865F2,
        title=page_content["title"],
        description=page_content["description"],
        timestamp=datetime.now()
    )

    embed1.set_thumbnail(
        url='https://cdn.donmai.us/sample/0b/c6/__lucid_maplestory_drawn_by_muaooooo__sample-0bc65d4dc17171ed5104e89ceae935b5.jpg'
    )

    embed1.set_image(
        url='https://cdn.donmai.us/sample/d6/b1/__lucid_maplestory_drawn_by_yoteh__sample-d6b1dfa7ec2c09867a4404ffa1730c97.jpg'
    )
    embed1.set_author(name="Kanga's Bot",
                      icon_url='https://static.wikia.nocookie.net/maplestory/images/7/76/NPCArtwork_Lucid_%28Dream_Festa_5%29.png/revision/latest?cb=20231215172053')

    embed1.set_footer(
        text="Made by @kangaroowastaken",
        icon_url=user.display_avatar.url
    )

    for field in page_content["fields"]:
        embed1.add_field(
            name=field["name"],
            value=field["value"],
            inline=field["inline"]
        )

    return embed1


@bot.command(name='shop')
async def help_command(ctx, page: int = 1):
    Kangaroo_id = 572633005894402068
    user = await bot.fetch_user(Kangaroo_id)

    if 1 <= page <= len(shop_pages):
        page_content = shop_pages[page - 1]
        embed1 = create_embed(page_content, user)
        msg = await ctx.send(embed=embed1)
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

        # Store the message ID and current page number
        user_shop_pages[msg.id] = {"page": page, "user_id": ctx.author.id}


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.id in user_shop_pages:
        page_info = user_shop_pages[reaction.message.id]

        if user.id != page_info["user_id"]:
            await reaction.remove(user=user)
            print("reaction removed")

        current_page = page_info["page"]
        new_page = current_page
        if reaction.emoji == "⬅️" and current_page > 1:
            new_page = current_page - 1
        elif reaction.emoji == "➡️" and current_page < len(shop_pages):
            new_page = current_page + 1

        if new_page != current_page:
            page_info["page"] = new_page
            page_content = shop_pages[new_page - 1]
            embed = create_embed(page_content, user)
            await reaction.message.edit(embed=embed)
        await reaction.remove(user=user)
        print('reaction removed')
