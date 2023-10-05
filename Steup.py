import csv
import os
import time
import sys
import asyncio
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, InputPeerEmpty, ChatForbidden, PeerChannel, InputPeerUser
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError, ChatAdminRequiredError

all_participants = []

# this will create the title during the software runing
def createTitle(lineType = "Title", title = ""):
    columns = os.get_terminal_size().columns
    lineType = lineType.lower()

    if (lineType == "title" and title != ""):
        halfColumns = int((columns - len(title))/2) - 1
        print(f"\n{'-' * (halfColumns)}|{title}|{'-' * (halfColumns)}")
    elif (lineType == "line"):
        print(f"{'-' * columns}", end = "\n\n")

async def saveSessionUserCount():
    currentDateTime = datetime.now().strftime("%H.%M_%Y-%m-%d")
    fileName = currentDateTime + f" {login.get_account_name()}-{login.get_phone_number()}"

    saveCSV(fileName, all_participants)

# this is the login page for the software
class logIn():
    def __init__(self):
        self.__api_id = None
        self.__api_hash = None
        self.__phoneNumber = None
        self.__accountName = None
        self.__private_path = ".\Data\AccountDetails.csv"

    def __call__(self):
        os.system("cls")
        title = "=|Login Page|="
        halfColumns = int((os.get_terminal_size().columns - len(title)) / 2)
        print("\r" + "-" * halfColumns + title + "-" * halfColumns , end = "", flush = True)

        if not os.path.isfile(self.__private_path):
            self.enter_api_ID()
            self.enter_api_hash()
            self.enter_phone_number()
            self.enter_account_name()

            self.write_private_details()
        else:
            self.read_private_details()

    def enter_api_ID(self):
        self.__api_id = str(input("Enter your api ID: "))
    def enter_api_hash(self):
        self.__api_hash = input("Enter your api hash: ")
    def enter_phone_number(self):
        self.__phoneNumber = str(input("Enter your phone number(9477XXXXXXX): "))
    def enter_account_name(self):
        self.__accountName = input("Enter name for you account(only for recognize): ");

    def get_api_ID(self):
        return self.__api_id
    def get_api_hash(self):
        return self.__api_hash
    def get_phone_number(self):
        return self.__phoneNumber
    def get_account_name(self):
        return self.__accountName

    def write_private_details(self):
        privateUserData = [self.__api_id, self.__api_hash, self.__phoneNumber, self.__accountName]

        if not os.path.isfile(self.__private_path):
            new_private_user_data = [["api_ID", "api_hash", "Phone Number", "Account Name"], privateUserData]

            with open(self.__private_path, "w", newline = "") as privateFile:
                csvWrite = csv.writer(privateFile)
                csvWrite.writerows(new_private_user_data)
        else:
            with open(self.__private_path, "a", newline = "") as privateFile:
                csvWrite = csv.writer(privateFile)
                csvWrite.writerows([privateUserData])

    def read_private_details(self):
        with open(self.__private_path, "r") as oldPrivateFile:
            csvRead = csv.reader(oldPrivateFile)

            oldPrivateData = []
            for row in csvRead:
                oldPrivateData.append(row)

        if (input("Do you wanna change the account(just press enter key for default)(y)\n: ").lower() == "y"):
            selectedNumber = self.append_private_details(oldPrivateData)
        else:
            selectedNumber = 1

        try:
            self.__api_id = oldPrivateData[selectedNumber][0]
            self.__api_hash = oldPrivateData[selectedNumber][1]
            self.__phoneNumber = oldPrivateData[selectedNumber][2]
            self.__accountName = oldPrivateData[selectedNumber][3]
        except IndexError as e:
            print(f"Can't find the account: reason-{e}")
            self.read_private_details()


    def append_private_details(self, oldPrivateData):
        for i in range(len(oldPrivateData)):
            print(f"|{i}| {oldPrivateData[i]} |")
            if i == 0:
                print("\r" + "-"* os.get_terminal_size().columns, end="", flush = True)
        createTitle("line")

        if (input("Do you wanna add new account(just press enter to choose a account from the list)(y)\n: ").lower() == "y"):
            while True:
                self.enter_api_ID()
                self.enter_api_hash()
                self.enter_phone_number()
                self.enter_account_name();

                self.write_private_details()
                if (input("Do you wanna add another new account?(y): ").lower() == "y"):
                    self.read_private_details()
                    break
        else:
            while True:
                try:
                    select = int(input("Enter the account row number from the list: "))
                    break
                except ValueError:
                    pass
            return select

# Main Account this will be create the telegram account and other TAPI function runing
class main():
    def __init__(self):
        # create the TelegramClient with the new event loop
        self.__client = TelegramClient(login.get_phone_number(), login.get_api_ID(), login.get_api_hash())

    async def initTelegram(self):
        await self.__client.connect()

        if not await self.__client.is_user_authorized():
            try:
                await self.__client.send_code_request(login.get_phone_number())

            except NameError:
                print("Phone number is not defined!")
                input("Press enter key to login again")
                login()

            try:
               await self.__client.sign_in(login.get_phone_number, input("Enter the Login code(check you telegram): "))

            except SessionPasswordNeededError:
                while True:
                    try:
                        await self.__client.sign_in(password=input("Enter Your Two-Step Verification password: "))
                        break

                    except PasswordHashInvalidError:
                        print("The password you entered is incorrect. Please try again.")

            except NameError as e:
                print(f'invalid entering "{e}"')
                input("Press enter key to login again")
                login()

    # See all channels and groups in your account
    async def get_all_channel_group(self):
        self.__all_dialogs = await self.__client (GetDialogsRequest(offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty(), limit = 1000, hash = 0))

        #self.__all_channels = [dialog for dialog in self.__all_dialogs.chats if dialog.is_channel]
        for i in reversed(range(len(self.__all_dialogs.chats))):
            time.sleep(0.1)
            print("\r" + "-" * os.get_terminal_size().columns, end = "", flush=True )
            if isinstance(self.__all_dialogs.chats[i], ChatForbidden):
                print(f"|{i}| |{self.__all_dialogs.chats[i].id}| |{self.__all_dialogs.chats[i].title}|Access Forbidden|")
            else:
                print(f"|{i}| |{self.__all_dialogs.chats[i].id}| |{self.__all_dialogs.chats[i].title}|{self.__all_dialogs.chats[i].participants_count}|")
        print(f"\n    All Group Count: {len(self.__all_dialogs.chats)}")

    # Get all users in you selected channel or group
    async def get_users_from_channel_group(self):
        participantsFromThisChannel = []
        userInput = input("Enter the Channel or Group username/ID/URL that you want to get users\n(exit or e for return to dashborad)\n: ")

        if (userInput.lower() == "e" or userInput.lower() == "exit"):
            return

        else:
            try:
                self.__channel = await self.__client.get_entity(PeerChannel(int(userInput)))
            except ValueError:
                self.__channel = await self.__client.get_entity(userInput)

            self.__offset_id = 0

            try:
                self.__limit = int(input("-|Enter the number of users(default = 10)(the limit is 10,000)\n: "))
            except ValueError:
                self.__limit = 10

            if (self.__limit > 10000):
                self.__limit = 9999

            input(f'-|Press Enter to get {self.__limit} users from "{self.__channel.title}"')
            while True:
                try:
                    participants = await self.__client(GetParticipantsRequest(self.__channel, ChannelParticipantsSearch(''), max(self.__offset_id, 0), self.__limit, hash = 0))
                    print(f"\n--|You have successfully get {self.__limit} users from \"{self.__channel.title}\" channel|--\n")
                except ChatAdminRequiredError:
                    print(f"\n--|You have no access to get users from \"{self.__channel.title}\" channel|--\n")
                    await self.get_users_from_channel_group()
                    return

                if not participants.users:
                    break

                participantsFromThisChannel.extend(participants.users)
                self.__offset_id = participants.users[-1].id

                if self.__offset_id > 2147483647:
                    break

            all_participants.extend(participantsFromThisChannel)

            fileName = input("-|Enter a name for CSV file(default set channel id + title)\n: ")
            if (fileName == ""):
                fileName = f"{self.__channel.id}_{self.__channel.title}"
            saveCSV(fileName, participantsFromThisChannel)

            if (input("-|Do you wanna see the all users you got(y)(just Enter to continue)\n: ") == "y"):
                try:
                    columns = os.get_terminal_size().columns
                except OSError:
                    columns = 100 # or a default value
    
                for user in participantsFromThisChannel:
                    print("\r" + "_" * columns, end="", flush=True)
                    time.sleep(0.2)
                    print(f"|ID:{user.id}|Username:{user.username}|First Name:{user.first_name}|Last Name:{user.last_name}|Phone Number:{user.phone}|")

            if(input("-|Do you wanna add users from another group/channel(y)(just Enter to continue)\n: ") == "y"):
                print(f"\n  Participants count from {self.__channel.id}: {len(participantsFromThisChannel)} Users\n")
                createTitle("line")
                await self.get_users_from_channel_group()

    # Add all users to a new channel or group
    #  you can get users from CSV file or user count in the software
    async def add_users_to_new_channel_group(self):
        print(f"    All Participants Count: {len(all_participants)}")

        userInput = input("Enter the Channel or Group username/ID/URL that you want to add the users\n(exit or e for return to dashborad)\n: ")
        if(userInput.lower() == "e" or userInput.lower() == "exit"):
            return
        else:
            try:
                addChannel = await self.__client.get_entity(PeerChannel(int(userInput)))
            except:
                addChannel = await self.__client.get_entity(userInput)
    
            add_participants = await self.__client(GetParticipantsRequest(addChannel, ChannelParticipantsSearch(''), 0, 9999, hash=0))
    
            input("Press Enter to add users to new group")
            for user in all_participants:
                createTitle("line")
                if user.id in add_participants.users:
                    print(f"|ID: {user.id}| Username: {user.username}| Status: User is already in the Group/Channel")
                else:
                    try:
                        await self.__client(InviteToChannelRequest(addChannel, [user.id]))
                        print(f"|ID: {user.id}| Username: {user.username}| Status: Added successfully")
                    except Exception as e:
                        print(f"|ID: {user.id}| Username: {user.username}| Status: Could not Add User| Reason: {str(e)}")

    async def get_Users(self, users):
        usersFromCSVfile = []
        for user in range(len(users)):
            if (user != 0):
                usersFromCSVfile.append(await self.__client.get_entity(InputPeerUser(int(users[user][0]), int(users[user][1]))))
        all_participants.extend(usersFromCSVfile)
        print("successfully readed CSV file")
        print(f"    Participant Count From CSV file: {len(usersFromCSVfile)}")

# saveCSV is use to save all users data comming from telegrame
#   Default path set to .\Save CSV(default) folder
def saveCSV(fileName, users, path = ".\Save CSV(default)"):

    userData = []
    filePath = os.path.join(path, str(fileName) + ".csv")

    if not os.path.isfile(filePath):
        userData.append(["ID","Access Hash", "Username", "Phone Number", "First Name", "Last Name"])

        for user in users:
            userData.append([user.id, user.access_hash, user.username, user.phone, user.first_name, user.last_name])

        # writing to CSV new File
        with open(filePath, "w", encoding = "utf-8", newline = "") as csvUserNewFile:
            csvWrite = csv.writer(csvUserNewFile)
            csvWrite.writerows(userData)

        print(f"Successfully write user data to new '{filePath}'")
    else:

        for user in users:
            userData.append([user.id, user.access_hash, user.username, user.phone, user.first_name, user.last_name])

        with open(filePath, "a", encoding = "utf-8", newline = "") as csvUserOldFile:
            csvWrite = csv.writer(csvUserOldFile)
            csvWrite.writerows(userData)

        print(f"Successfully write user data to old '{filePath}'")

async def readCSV(fileName, tlSession = "" , path = ".\Save CSV(default)"):
    filePath = os.path.join( path, str(fileName) + ".csv")
    usersDetailsFromCSVfile = []

    with open(filePath, "r", encoding = "utf-8") as readCSVfiles:
        csvRead = csv.reader(readCSVfiles)
        for row in csvRead:
            usersDetailsFromCSVfile.append(row)

    if (tlSession != ""):
        await tlSession.get_Users(usersDetailsFromCSVfile)


# Dashboard for the Software
#   controll all application functionality
async def dashboard(telegram):
    os.system("cls")

    columns = os.get_terminal_size().columns

    menuList = [
        "Dashboard",
        "New Dashboard",
        "See all Channels/Groups",
        "Automate User add",
        "Get Users From Channels/Groups",
        "Add Users to New Channel/Group",
        "Get Users From CSV File",
        "Log Out"
        ]

    for i in range(len(menuList)):
        menu = f"|{i}| {menuList[i]}"
        halfColumns = int((columns - len(menu))/2)
        if (i == 0):
            print("\r" + "-" * columns)
            print(f"| API ID: {login.get_api_ID()} | Account Name: {login.get_account_name()} | Users Count: {len(all_participants)}")
            print(f"{'-' * (halfColumns + 2)}|{menuList[i]}|{'-' * (halfColumns + 1)}", end = "\n\n")
        else:
            print(f"{' ' * halfColumns}{menu}{' ' * halfColumns}")
    print("\r" + "-" * columns)

    while True:
        selectNumber = input("|Enter the number(exit or e)(new or n): ").lower()

        match selectNumber:
            case "new" | "n" | "1":
                await dashboard(telegram)
            case "2":
                createTitle("title", "Get All Channel and Group from Telegram")
                await telegram.get_all_channel_group()
                createTitle("line")
            case "3":
                input("Enter for the continue")
            case "4":
                createTitle("title", "Get Users From Channel or Group")
                await telegram.get_users_from_channel_group()
                createTitle("line")
                print(f"    Users Count: {len(all_participants)}\n")
            case "5":
                createTitle("title", "Add Users to New Channel or Group")
                await telegram.add_users_to_new_channel_group()
                createTitle("line")
            case "6":
                createTitle("title", "Get Users From CSV File")
                filename = input("-|Enter the CSV file name(you don't want to include .csv)\n: ")
                filePath = input("-|Enter the CSV file path(just Enter for the default path)\n:")
                if (filePath == ""):
                    await readCSV(filename, telegram)
                else:
                    await readCSV(filename, telegram, filePath)
                createTitle("line")
                print(f"    Users Count: {len(all_participants)}")
            case "7":
                login()
                input("Enter for the contie.")
                await dashboard(telegram)
            case "exit" | "e" | "8":
                await saveSessionUserCount()
                exit()

# initialize the software functions

# Run the main function as an asyncio task
async def init_telegram():
    newTelegram = main()
    await newTelegram.initTelegram()
    await dashboard(newTelegram)

login = logIn()
login()

asyncio.run(init_telegram())

