import logic
import dropdowns

import discord
from discord.ext import commands
from discord.ui import Select, View


def run_discord_bot():
    intents = discord.Intents.all()
    bot = commands.Bot(intents=intents)
    guild_ids=[345444924029796353]

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))
        await bot.sync_commands()

    @bot.slash_command(name='optimal', description='Optimal bid', guild_ids=guild_ids)
    async def optimal(interaction, current_price: int):
        for8,for4 = logic.optimized_bid(current_price)
        await interaction.response.send_message(f'The optimal bid for an 8 person instance is {for8}\n'
                                                f'The optimal bid for a 4 person instance is {for4}')

    @bot.slash_command(name='hone', description='Get the cost of honing', guild_ids=guild_ids)
    async def test(interaction):
        armor = Select(placeholder='Armor type',options=dropdowns.get_armor_select())
        view = View(armor)
        armor_level = Select()
        cost_type = Select()

        async def armor_callback(inter):
            armor.disabled = True
            if armor.values[0] == '3':
                armor_min = 12
                armor_max = 20
            else:
                armor_min = 0
                armor_max = 25

            armor_level = Select(placeholder='Target ilvl you want to reach',
                                 options=dropdowns.get_armor_lvl_select(armor_min, armor_max))
            v = View(armor_level)
            await inter.response.edit_message(view=view)
            await interaction.send(view=v)

        async def armor_level_callback(inter):
            armor_level.disabled = True
            await inter.response.edit_message(view=view)
            costs = logic.optimized_bid(armor_level.values[0],armor.values[0])
            await inter.response.send_message('The shard cost is: ')



        armor.callback = armor_callback
        armor_level.callback = armor_level_callback


        view = View(armor)

        await interaction.send(view=view)
        await interaction.response.send_message("Choose an armor type and the target ilvl")


    bot.run('MTA3MjgwNDk3MDkwNDE1ODIyOA.GeGKCc.OLgRajSRJwihc3o6rswIPzJmrpWiuBGoqsTgzQ')