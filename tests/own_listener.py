import vkreal
import asyncio


token = "Your token"
loop = asyncio.get_event_loop()

session = vkreal.VkApi(token = token)
vk = session.api_context()
longpoll = vkreal.VkLongPoll(session, loop = loop)

async def worker(peer_id, some_data):
    await vk.messages_send(
    peer_id = peer_id,
    message = some_data,
    random_id = 0)
    
async def listener():
    async for event in longpoll.listen():
        if event["type"] == 4:
            if event["text"] == "hello":
                loop.create_task(worker(event["peer_id"], "hello, hello"))
                

loop.create_task(listener())
loop.run_forever()