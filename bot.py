import logic
import dropdowns
from config import token
from config import guild_ids

import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import Option


def run_discord_bot():
    intents = discord.Intents.all()
    bot = commands.Bot(intents=intents)

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))
        await bot.sync_commands()

    @bot.slash_command(name='optimal', description='Optimal bid', guild_ids=guild_ids)
    async def optimal(interaction,
                      current_price: Option(int, "Enter a price integer (ie. 8000)", required=True)):

        for8,for4 = logic.optimized_bid(current_price)
        await interaction.response.send_message(f'The optimal bid for an 8 person instance is {for8}\n'
                                                f'The optimal bid for a 4 person instance is {for4}')

    @bot.slash_command(name='raid', description='Grab raid strats (ie: brel g4 or brel all)', guild_ids=guild_ids)
    async def raid(interaction,
                   raid_type: Option(str, "Enter a raid type (ie. brel, kakul, vykas, etc...)", required=True),
                   gate: Option(str, "Enter a gate number (ie. G1, 2, gate 3, etc...)", required=True)):

        raid_type,gate = logic.raid_cleanup(raid_type, gate)
        file_name = logic.query_raid(raid_type, gate)
        if file_name == '-1':
            await interaction.response.send_message('Raid not found.')
        else:
            await interaction.response.send_message(file=discord.File(file_name))

    @bot.slash_command(name='hone', description='Get the cost of honing', guild_ids=guild_ids)
    async def hone(interaction):
        armor = Select(placeholder='Armor type',options=dropdowns.get_armor_select())
        view = View(armor)
        armor_level = Select(placeholder='Target ilvl you want to reach')
        armor_or_weapon = Select(placeholder='Weapon or armor?')

        async def armor_callback(inter):
            armor.disabled = True
            # update for when +25 is available for brel and brel hard gear
            if armor.values[0] == '1' or armor.values[0] == '3':
                armor_min = 1
                armor_max = 20
            else:
                armor_min = 1
                armor_max = 25

            armor_level.options = dropdowns.get_armor_lvl_select(armor_min, armor_max)
            armor_level.callback = armor_level_callback
            view.add_item(armor_level)
            await inter.response.edit_message(view=view)

        async def armor_level_callback(inter):
            armor_level.disabled = True
            armor_or_weapon.options = dropdowns.get_armor_or_weapon_select()
            armor_or_weapon.callback = armor_or_weapon_callback
            view.add_item(armor_or_weapon)
            await inter.response.edit_message(view=view)

        async def armor_or_weapon_callback(inter):
            armor_or_weapon.disabled = True
            await inter.response.edit_message(view=view)
            driver, worst_case, avg_case, best_case = logic.search_cost(armor_level.values[0],
                                                                armor.values[0],
                                                                armor_or_weapon.values[0])
            await interaction.send(f'Worst case:\n'
                                   f'\t\t\t\tSilver: {worst_case[0]}\n'
                                   f'\t\t\t\tGold: {worst_case[1]}\n'
                                   f'\t\t\t\tShards: {worst_case[2]}\n'
                                   f'\t\t\t\tFusion Mat: {worst_case[3]}\n'
                                   f'\t\t\t\tG/D Stones: {worst_case[4]}\n'
                                   f'\t\t\t\tLeapstones: {worst_case[5]}\n'
                                   f'Average Case:\n'
                                   f'\t\t\t\tSilver: {avg_case[0]}\n'
                                   f'\t\t\t\tGold: {avg_case[1]}\n'
                                   f'\t\t\t\tShards: {avg_case[2]}\n'
                                   f'\t\t\t\tFusion Mat: {avg_case[3]}\n'
                                   f'\t\t\t\tG/D Stones: {avg_case[4]}\n'
                                   f'\t\t\t\tLeapstones: {avg_case[5]}\n'
                                   f'1 Tap:\n'
                                   f'\t\t\t\tSilver: {best_case[0]}\n'
                                   f'\t\t\t\tGold: {best_case[1]}\n'
                                   f'\t\t\t\tShards: {best_case[2]}\n'
                                   f'\t\t\t\tFusion Mat: {best_case[3]}\n'
                                   f'\t\t\t\tG/D Stones: {best_case[4]}\n'
                                   f'\t\t\t\tLeapstones: {best_case[5]}')
            driver.quit()

        armor.callback = armor_callback

        view = View(armor)

        await interaction.send(view=view)
        await interaction.response.send_message("Choose an armor/weapon type and the target ilvl")

    bot.run(token)
