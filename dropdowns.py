import discord
from discord.ui import Select, View


def get_armor_select():
    selections = [
            discord.SelectOption(label='Fresh T3 (1302)',value='1'),
            discord.SelectOption(label='Valtan/Vykas Relic Gear (1340)',value='2'),
            discord.SelectOption(label='Brel Gear (1390)',value='3')]

    return selections


def get_armor_lvl_select(min=1, max=20):
    selections = []
    for i in range(min, max + 1):
        label = '+' + str(i)
        selections.append(discord.SelectOption(label=label,value=str(i)))

    return selections
