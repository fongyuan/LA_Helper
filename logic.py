import os
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def optimized_bid(price):
    min8 = price / 8 * 7 / 1.1 + 1
    max8 = price / 8 * 7
    min4 = price / 4 * 3 / 1.1 + 1
    max4 = price / 4 * 3

    return int(min8),int(max8),int(min4),int(max4)


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
    elif raid_type[0:2].lower() == 'vy':
        raid_type = 'vykas'
    else:
        raid_type = '-1'

    #check for 'all'
    gate_num = gate_num.lower()
    if gate_num != 'all':
        gate_num = ''.join(filter(str.isdigit, gate_num))

    return raid_type, gate_num


# ui legend before changing to single item:
# 0 Steam - English
# 1 T3 Brelshaza (1390)
# 2 Europe Central
# 3 Multiple Items
# 4 Worst case scenario
# 5 No additional materials
# ui legend after changing to single item:
# 0 Steam - English
# 1 T3 Brelshaza (1390)
# 2 Europe Central
# 3 Single Item
# 4 Weapon
# 5 Worst case scenario
# 6 No additional materials
def search_cost(target_ilvl, armor_type, armor_or_weapon):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    actions = ActionChains(driver)
    driver.implicitly_wait(5)
    driver.get("https://maxroll.gg/lost-ark/upgrade-calculator")

    # find drop down to change multi item to single item
    ui = driver.find_elements(By.CSS_SELECTOR, 'div.ui-Select')
    # for index,i in enumerate(ui):
    #     print(index,i.text)
    ui[3].click()
    actions.send_keys(Keys.ARROW_UP)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    # perform drop down selections based on input
    # changes whether weapon or armor cost is searched
    ui = driver.find_elements(By.CSS_SELECTOR, 'div.ui-Select')
    if armor_or_weapon == 'armor':
        ui[4].click()
        actions.send_keys(Keys.ARROW_UP)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    # TODO add ancient gear navigation when it comes out
    # TODO consider separate function for each armor type
    # changes which type of armor to search for
    # print('here')
    # if armor_type == '1':
    #     ui[1].click()
    #     actions.send_keys(Keys.ARROW_UP)
    #     actions.send_keys(Keys.ARROW_UP)
    #     actions.send_keys(Keys.ENTER)
    #     actions.perform()
    # elif armor_type == '2':
    #     print('op2')
    #     ui[1].click()
    #     actions.send_keys(Keys.ARROW_UP)
    #     actions.send_keys(Keys.ENTER)
    #     actions.perform()
    # TODO update for when ancient gear comes out
    # elif armor_type == '3':
    #     ui[1].click()
    #     actions.send_keys(Keys.ARROW_UP)
    #     actions.send_keys(Keys.ENTER)
    #     actions.perform()

    target = driver.find_elements(By.CSS_SELECTOR, 'input')
    # for index,i in enumerate(target):
    #     print(index,i.get_attribute(name='value'))
    # target[26] is the target ilvl
    # target[27] is failed attempts
    # target[28] is artisan energy
    target[26].send_keys(target_ilvl)
    # target[36].send_keys(target_ilvl)
    # driver.save_screenshot('here.png')

    # get worst case
    costs = driver.find_elements(By.CSS_SELECTOR, 'span.lap-value')
    # for index,i in enumerate(costs):
    #     print(index,i.text)
    worst_case = [c.text for c in costs]
    # _case = [silver, gold, shards, fusion material, stones, leapstones]
    worst_case = worst_case[11:17]

    # get average case
    ui[5].click()
    actions.send_keys(Keys.ARROW_DOWN)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    costs = driver.find_elements(By.CSS_SELECTOR, 'span.lap-value')
    avg_case = [c.text for c in costs]
    avg_case = avg_case[11:17]

    # get 1 tap
    ui[5].click()
    actions.send_keys(Keys.ARROW_DOWN)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    costs = driver.find_elements(By.CSS_SELECTOR, 'span.lap-value')
    best_case = [c.text for c in costs]
    best_case = best_case[11:17]

    #driver.save_screenshot('here.png')
    #print("done")
    #driver.quit()
    return driver,worst_case,avg_case,best_case
