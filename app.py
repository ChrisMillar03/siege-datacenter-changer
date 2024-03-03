import asyncio, os, time
from dotenv import load_dotenv
from siegeapi import Auth

datacenter_list = [
	"default",
	"playfab/australiaeast",
	"playfab/brazilsouth",
	"playfab/centralus",
	"playfab/eastasia",
	"playfab/eastus",
	"playfab/japaneast",
	"playfab/northeurope",
	"playfab/southafricanorth",
	"playfab/southcentralus",
	"playfab/southeastasia",
	"playfab/uaenorth",
	"playfab/westeurope",
	"playfab/westus"
]

class Profile:
	def __init__(self, uuid, username):
		self.uuid = uuid
		self.username = username

async def get_profiles(auth, uuid_list):
	profiles = []

	for i in uuid_list:
		player = await auth.get_player(uid=i)
		profiles.append(Profile(i, player.name))

	return profiles

async def main():
	load_dotenv()

	auth = Auth(os.getenv("EMAIL"), os.getenv("PASS"))
	game_dir = os.path.join(os.getenv("USERPROFILE"), "Documents", "My Games", "Rainbow Six - Siege")
	uuid_list = [f.path.split("\\")[-1] for f in os.scandir(game_dir) if f.is_dir()]
	profiles = await get_profiles(auth, uuid_list)

	await auth.close()

	selected_profile = None

	for i, profile in enumerate(profiles):
		number = str(i + 1) + " " if i < 9 else str(i + 1)

		print(f"{number} =  {profile.username}")

	while not selected_profile:
		selection = input("\n=> ")

		if not selection.isnumeric():
			print("\nSelection must be numeric!")
			continue

		selection = int(selection)

		if selection < 1 or selection > len(profiles):
			print("\nInvalid profile selection!")
			continue

		selected_profile = profiles[selection - 1]

	print()

	selected_datacenter = None

	for i, datacenter in enumerate(datacenter_list):
		number = str(i + 1) + " " if i < 9 else str(i + 1)

		if datacenter == "default":
			print(f"{number} =  default (ping based)")
		else:
			print(f"{number} =  {datacenter}")

	while not selected_datacenter:
		selection = input("\n=> ")

		if not selection.isnumeric():
			print("\nSelection must be numeric!")
			continue

		selection = int(selection)

		if selection < 1 or selection > len(datacenter_list):
			print("\nInvalid datacenter selection!")
			continue

		selected_datacenter = datacenter_list[selection - 1]

	settings_file = os.path.join(game_dir, selected_profile.uuid, "GameSettings.ini")
	settings = []

	with open(settings_file, "r") as file:
		for line in file:
			if line.startswith("DataCenterHint"):
				settings.append(f"DataCenterHint={selected_datacenter}\n")
			elif line.startswith("Console"):
				settings.append("Console=1\n")
			else:
				settings.append(line)

	with open(settings_file, "w") as file:
		for line in settings:
			file.write(line)

	selected_datacenter = selected_datacenter.split("/")[-1]

	print(f"\nSuccessfully changed datacenter for {selected_profile.username} to {selected_datacenter}")
	time.sleep(5)

if __name__ == "__main__":
	asyncio.run(main())
