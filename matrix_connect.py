
from nio import AsyncClient, MatrixRoom, RoomMessageText ,RoomMessage, RoomMessageNotice, RoomMessagesResponse, DeviceList, SyncResponse, SyncError
from nio.store import MatrixStore
from nio.crypto import * 
import asyncio

DEVICE_ID=''
USER_ID=''
async def sync_cb(response):
   print(f"We synced, token: {response.next_batch}")

async def cb_print_messages(room: MatrixRoom, event: RoomMessageText) -> None:
        """Callback to print all received messages to stdout.

        Arguments:
            room {MatrixRoom} -- Provided by nio
            event {RoomMessageText} -- Provided by nio
        """
        if event.decrypted:
            encrypted_symbol = "🛡 "
        else:
            encrypted_symbol = "⚠️ "
        print(
            f"{room.display_name} |{encrypted_symbol}| {room.user_name(event.sender)}: {event.body}"
        )
        
async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )
    
async def EncryptMessage(client : AsyncClient, roomid : str, msg :str) :
    return await client.encrypt(room_id=roomid, message_type=RoomMessageText,content=msg)

def CloseSession(client : AsyncClient) :
    print ("peace out")
    client.close()
    exit()

async def login_and_sync( homeserver_url, username, password):
    # Create an AsyncClient instance
    client = AsyncClient(homeserver=homeserver_url,user="nikreed",ssl=False)
    client.add_event_callback(message_callback, RoomMessageText)
    client.add_response_callback(sync_cb, SyncResponse)
   
    login_response = await client.login( password)
   
    # Check if login was successful
    if login_response:
        print(login_response)
    else:
        print("Login failed.")
        return
    USER_ID = '@nikreed:aria-net.org'
    DEVICE_ID = login_response.device_id
    store = MatrixStore(USER_ID,DEVICE_ID,'./',database_name="matrix_Store")
    
    print("Display Name: %s" % client.get_displayname('@nikreed:aria-net.org'))
  
    # Sync with the server
    try :
        # await client.sync()
        await client.sync()
    except :
        print("****ERROR*****")
        await client.close()
        return
    print("done")
    # Do something with the client, such as joining a room or sending messages
    # Example: Join a room and print messages
    ROOM_ID = room_id = "!lIppryFduYlBdEdKzn:aria-net.org" #input("Enter the room ID to join: ")
    room = await client.join(room_id)
    print("room:",room)
    room = client.rooms[ROOM_ID]
    print(f"Room {room.name} is encrypted: {room.encrypted}")
    # Print messages in the room
    # for device in device_store:
    #     print(device.user_id, device.device_id)   
    # Keep the script running until user stops it
    # user_set = client.get_missing_sessions(ROOM_ID)
    # for k,v in user_set.items() :
    #     print(k , " : ", v)
    if input() == 'q' :
        CloseSession(client)
    while True:
        await client.sync()
        msg = input("Enter a message")
        resp = await client.room_send(
    # Watch out! If you join an old room you'll see lots of old messages
            room_id=room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": msg},
    )
        messages = await  client.room_messages(ROOM_ID,'')
        m = messages.chunk
        for i in m :
            print("Messages:",i)
    
        await client.sync()
        pass

    # Remember to gracefully close the client when done
    await client.close()


async def RegisterForHomeserver(client :AsyncClient, username: str, password : str, homeserver : str) :
    await client.register(username, password, )
