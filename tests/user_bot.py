import vkreal
import asyncio


token = "your token"
loop = asyncio.get_event_loop()

session = vkreal.VkApi(token = token)
vk = session.api_context()
longpoll = vkreal.VkLongPoll(session, loop = loop)

async def answer(event):
    if event["type"] == 4:
        if event["text"] == "hello":
            await vk.messages_send(
            peer_id = event["peer_id"],
            message = "Hello from vkreal!",
            random_id = 0)
            
loop.create_task(longpoll.on_event(answer))
loop.run_forever()
