import dropdowns

import discord
from discord.ext import commands
from discord.ui import Select, View

def armor(interaction, view):

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