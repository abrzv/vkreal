import vkreal
import asyncio


token = "your token"
id = 1 # your_group_id
loop = asyncio.get_event_loop()

session = vkreal.VkApi(token = token)
vk = session.api_context()
longpoll = vkreal.VkBotLongPoll(session, id, loop = loop)

async def answer(event):
    if event["type"] == "message_new":
        if event["object"]["message"]["text"] == "hello":
            await vk.messages_send(
            peer_id = event["object"]["message"]["peer_id"],
            message = "Hello from vkreal!",
            random_id = 0)
            
loop.create_task(longpoll.on_event(answer))
loop.run_forever() 
