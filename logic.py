import os


def optimized_bid(price):
    for8 = price / 8 * 7 / 1.1 + 50
    for4 = price / 4 * 3 / 1.1 + 50

    return int(for8),int(for4)


def query_raid(raid_type, gate_num):
    if gate_num != 'all':
        name = raid_type + '_' + 'G' + gate_num + '.png'
    else:
        name = raid_type + '_' + 'all.png'
    fname = 'images/' + name
    if not os.path.exists(fname):
        return '-1'

    return fname


def raid_cleanup(raid_type, gate_num):
    if raid_type[0].lower() == 'b':
        raid_type = 'brel'
    elif raid_type[0].lower() == 'k' or raid_type.lower() == 'clown':
        raid_type = 'kakul'
    elif raid_type[0:1].lower() == 'vy':
        raid_type = 'vykas'
    else:
        raid_type = '-1'

    gate_num = ''.join(filter(str.isdigit, gate_num))

    return raid_type, gate_num


def search_cost(target_ilvl, armor_type):
    #TODO: do queries for honor shards, destruction/guardian stones, honor leapstones, silver, and gold
    #TODO: grab above for worst case, average case and best case
    return
