import csv
import os
import time
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, InputPeerEmpty
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError

api_id = "20571351"
api_hash = "c5ec13176dffebee494d33ba87fe7083"
phoneNumber = "94789991578"
all_participants = []

async def main():

    # create the TelegramClient with the new event loop
    client = TelegramClient(phoneNumber,api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        client.send_code_request(phoneNumber)

        try:
           await client.sign_in(phoneNumber, input("Enter the Code: "))

        except SessionPasswordNeededError:

            while True:

                try:
                    await client.sign_in(password=input("Enter Your Two-Step Verification password: "))
                    break

                except PasswordHashInvalidError:
                    print("The password you entered is incorrect. Please try again.")

    all_channels = await client (GetDialogsRequest(offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty(), limit = 100, hash = 0))
   #for entity in all_channels.chats:
   #    print("\r" + "_" * os.get_terminal_size().columns, end = "", flush=True )
   #    print(entity.id)
   #    print(entity.title)

    input("Press Enter to get all userse from channel")

    channelUsername = "srilankansapi"
    channelAddUsername = "Testingdontmsg";

    channel = await client.get_entity(channelUsername)
    addChannel = await client.get_entity(channelAddUsername)

    offset_id = 0
    limit = 100
    
    while True:

        participants = await client(GetParticipantsRequest(channel, ChannelParticipantsSearch(''), max(offset_id, 0), limit, hash=0))

        if not participants.users:
            break

        all_participants.extend(participants.users)
        offset_id = participants.users[-1].id

        if offset_id > 2147483647:
            break

    add_participants = await client(GetParticipantsRequest(addChannel, ChannelParticipantsSearch(''), 0, 100, hash=0))

    #input("Press Enter to add users to new group");
    #for user in all_participants:
    #    print(user.id)
    #    if user.id in add_participants.users:
    #        print("User is already in the group")
    #    else:
    #        try:
    #            await client(InviteToChannelRequest(channelAddUsername, [user.id]))
    #            print("User Added Successfully.")
    #        except Exception as e:
    #            print(f"Could not add user: {str(e)}")

def saveCSV(fileName, users, path = ""):
    # Default path set to .\Save CSV(default) folder
    path = path if path != "" else ".\Save CSV(default)"

    userData = []
    filePath = os.path.join(path, str(fileName) + ".csv")

    if not os.path.isfile(filePath):
        userData.append(["ID", "Username", "Phone Number", "First Name", "Last Name"])

        for user in users:
            userData.append([user.id, user.username, user.phone, user.first_name, user.last_name])

        # writing to CSV new File
        with open(filePath, "w", encoding="utf-8") as csvUserNewFile:
            csvWrite = csv.writer(csvUserNewFile)
            csvWrite.writerows(userData)

        print(f"Successfully write user data to new '{filePath}'")
    else:

        for user in users:
            userData.append([user.id, user.username, user.phone, user.first_name, user.last_name])

        with open(filePath, "a", encoding="utf-8") as csvUserOldFile:
            csvWrite = csv.writer(csvUserOldFile)
            csvWrite.writerows(userData)

        print(f"Successfully write user data to old '{filePath}'")

# Run the main function as an asyncio task
asyncio.run(main())

file_name = input("Enter the CSV file name: ")
path = input("Enter file path(Just enter to set default):")

saveCSV(file_name, all_participants, path)

#numberOfUsers = 0
#try:
#    columns = os.get_terminal_size().columns
#except OSError:
#    columns = 100 # or a default value
#
#for user in all_participants:
#    print("\r" + "_" * columns, end="", flush=True)
#    time.sleep(0.1)
#    print("ID:", user.id)
#    print("Username: ", user.username)
#    print("First name: ", user.first_name)
#    print("Last name: ", user.last_name)
#    print("Phone number: ", user.phone)
#    numberOfUsers += 1
#
#print(numberOfUsers)

