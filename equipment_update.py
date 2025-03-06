from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # To automatically manage the driver
import time

WEAPON_MAPPING={
	"LONG_SWORD": "Great Sword",
	"SHORT_SWORD": "Sword & Shield",
	"TWIN_SWORD": "Dual Blades",
	"TACHI": "Long Sword",
	"HAMMER": "Hammer",
	"WHISTLE": "Hunting Horn",
	"LANCE": "Lance",
	"GUN_LANCE": "Gun Lance",
	"SLASH_AXE": "Switch Axe",
	"CHARGE_AXE": "Charge Blade",
	"ROD": "Insect Glaive",
	"BOW": "Bow",
	"HEAVY_BOWGUN": "Heavy Bowgun",
	"LIGHT_BOWGUN": "Light Bowgun",
}

ELEMENT_MAPPING = {
	"1": "Fire",
	"2": "Water",
	"3": "Lightning",
	"4": "Ice",
	"5": "Dragon",
	"6": "Poison",
	"7": "Sleep",
	"8": "Paralysis",
	"9": "Blast"
}

KIRANICO_BASE_URL = "https://mhwilds.kiranico.com"

def skill_splitter(skill_string):
	return re.sub(r'(\+\d)(\w)', r'\1,\2', skill_string)

def get_all_armors():
	armors = []

	path = KIRANICO_BASE_URL+"/data/armor-series/"
	response = requests.get(path)
	if response.status_code == 200:
		armor_list_html = response.text
	else:
		print(f"Failed to connect to {path}")
		return armors

	armor_list_soup = BeautifulSoup(armor_list_html,'html.parser')
	a_tags = armor_list_soup.find_all('a', href=lambda href:href and 'data/armor-series/' in href)
	for tag in a_tags:
		for armor in process_armor_set(tag['href']):
			armors.append(armor)
	return armors		

def process_armor_set(armor_set_url_ext):
	armor_set_url = KIRANICO_BASE_URL+armor_set_url_ext

	armor_set = armor_set_url.split("/")[-1].replace("-"," ").title()
	response = requests.get(armor_set_url)
	armors = []
	if response.status_code == 200:
		print(f'Processing {armor_set} from {armor_set_url}')
		armor_set_html = response.text
		armor_set_soup = BeautifulSoup(armor_set_html,'html.parser')
		tr_elements = armor_set_soup.find_all('tr')
			
		for tr in tr_elements:
			table_data = [td.get_text(strip=True) for td in tr.find_all('td')]

			match len(table_data):
				case 2:
					curr_armor = {
							"set":armor_set,
							"name":table_data[0],
							"description":table_data[1]
					}

					armor_index = -1
					for i, armor in enumerate(armors):
						if armor.get("name") == table_data[0]:
							armor_index = i
						if armor_index == -1:armors.append(curr_armor)
						else:
							for k,v in curr_armor.items(): armors[armor_index][k] = v

				case 4:#deco slots and skills
					deco_slots = table_data[2].replace('[',"").replace(']',"")
					lvl_1_slots = deco_slots[0]
					lvl_2_slots = deco_slots[1]
					lvl_3_slots = deco_slots[2]

					curr_armor = {
							"set":armor_set,
							"name":table_data[1],
							"slot":table_data[0],
							"level_1_decoration_slots":lvl_1_slots, 
							"level_2_decoration_slots":lvl_2_slots, 
							"level_3_decoration_slots":lvl_3_slots, 
							"skills":skill_splitter(table_data[3])
					}

					armor_index = -1
					for i, armor in enumerate(armors):
						if armor.get("name") == table_data[1]:
							armor_index = i
							break
					if armor_index == -1: armors.append(curr_armor)
					else: 
						for k,v in curr_armor.items(): armors[armor_index][k] = v

				case 8:#defense and resistances
					curr_armor = {
							"set":armor_set,
							"name":table_data[1],
							"slot":table_data[0],
							"defense":table_data[2],
							"fire_res":table_data[3],
							"water_res":table_data[4],
							"thunder_res":table_data[5],
							"ice_res":table_data[6],
							"dragon_res":table_data[7],
					}

					armor_index = -1
					for i, armor in enumerate(armors):
						if armor.get("name") == table_data[1]:
							armor_index = i
							break
					if armor_index == -1:armors.append(curr_armor)
					else:
						for k,v in curr_armor.items(): armors[armor_index][k] = v
	else:
		print(f'Failed to process {armor_set} from {armor_set_url}')

	return armors

def get_all_weapons():
	weapons = []
	path = KIRANICO_BASE_URL+"/data/weapons"
	
	service = Service(ChromeDriverManager().install())  # Automatically installs ChromeDriver if needed
	driver = webdriver.Chrome(service=service, options=Options())
	driver.get(path)
	time.sleep(1)
	
	weapon_buttons = driver.find_elements(By.XPATH, '//*[contains(@id, ":-trigger-")]')
	for button in weapon_buttons:
		button_id = button.get_attribute('id')
		button.click()
		time.sleep(1)

		weapon_type = WEAPON_MAPPING.get(button_id.split('-')[-1])
		print(f'Processing {weapon_type}s')

		weapon_html = driver.page_source
		for weapon in process_weapon_type(weapon_type,weapon_html):
			weapons.append(weapon)
	return weapons

def process_weapon_type(weapon_type, weapon_html):
	weapons = []
	weapon_soup = BeautifulSoup(weapon_html,'html.parser')
	tr_elements = weapon_soup.find_all('tr')
	for tr in tr_elements:
		table_data = []
		for i,td in enumerate(tr.find_all('td')):
			td_text = td.get_text(strip=True)
			img = td.find('img')
			if img:
				link = img['src']
				if "element" in link.lower():
					td_text+=link.split("/")[-1].strip('.png')

			if i == 6:
				sharpness_base = []
				sharpness_handicraft = []
				if len(td.find_all('rect')) > 0:
					for i,rect in enumerate(td.find_all('rect')):
						if i < 7:
							table_data.append(rect["width"])
						if i > 7 and i <15:
							table_data.append(rect["width"])
				else:
					table_data.extend([0]*14)
			else:
				table_data.append(td_text)
		lvl_1_slots,lvl_2_slots,lvl_3_slots = table_data[2].split('-')
		
		element_buildup,element_type = 0,'N/A'
		affinity_mod, defense_mod = 0,0

		if table_data[4] != '':
			split_elements = table_data[4].split("ElementType")
			element_buildup = split_elements[0]
			if len(split_elements)>1:
				element_type = ELEMENT_MAPPING.get(split_elements[1]) 

		if table_data[5] != '':
			affinity_match = re.search(r"([+-]?\d+%)",table_data[5]) # Matches percentage (e.g., +15%, -30%)
			defense_match = re.search(r"([+-]?\d+ Def)",table_data[5]) # Matches defense (e.g., +30 Def, -50 Def)
			if affinity_match: affinity_mod = affinity_match.group(1).replace("%","")
			if defense_match: defense_mod = defense_match.group(1).replace(" Def","").replace("+","")
		weapons.append({
			"type":weapon_type,

			"name": table_data[1],
			"damage":table_data[3],

			"element_buildup":element_buildup,
			"element_type":element_type,

			"affinity_mod":affinity_mod,
			"defense_mod": defense_mod,

			"special":table_data[20],
			"skills":skill_splitter(table_data[21]),

			"level_1_decoration_slots":lvl_1_slots,
			"level_2_decoration_slots":lvl_2_slots, 
			"level_3_decoration_slots":lvl_3_slots, 

			"sharpness_base_red":table_data[6],
			"sharpness_base_orange":table_data[7],
			"sharpness_base_yellow":table_data[8],
			"sharpness_base_green":table_data[9],
			"sharpness_base_blue":table_data[10],
			"sharpness_base_white":table_data[11],
			"sharpness_base_purple":table_data[12],

			"sharpness_max_red":table_data[13],
			"sharpness_max_orange":table_data[14],
			"sharpness_max_yellow":table_data[15],
			"sharpness_max_green":table_data[16],
			"sharpness_max_blue":table_data[17],
			"sharpness_max_white":table_data[18],
			"sharpness_max_purple":table_data[19],
			})
	return weapons