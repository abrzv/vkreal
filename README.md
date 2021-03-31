# vkreal
Simple asynchronus wrapper for vk_api.

Version 1.0.0.

It isn't ideal, but it works...

![Орех](https://user-images.githubusercontent.com/65618248/112987857-d4a45600-916b-11eb-87a0-1e5a88e542ca.png "Орехус")

_____
_____
_____
## Documentation

### vkreal.VkApi(token, sess = None, v = "5.125")
- token

Token from vk api, that you can get, using oauth.vk.com
- sess

httpx.AsyncClient. You can use your own session, for example for using methods with proxy.
- v

Vk api version.
_______
### vkreal.VkApi.api_context()
Creates and initializes [ApiContext](#vkrealapicontextapi) object with current VkApi object.
_______
### vkreal.VkApi.method(name, params)
- name

Method name. You can see a list of all methods [here](https://vk.com/dev/methods).
- params

Parameters, with which method will be called.
You can see it in https://vk.com/dev/method.name
_______
### vkreal.ApiContext(api)
Wrapper, for using api methods as ordinary class methods.

- api

Initialized VkApi object.
_______
### vkreal.VkLongPoll(api, v = "3", mode = 10, get_pts = False, loop = None)

- api

VkApi object for longpoll initialization.

- v

Longpoll version.

- mode

Longpoll mode.

- get_pts

This parameter reserved.

- loop

Asyncio loop, which will be used by event listener and handlers.
________
### vkreal.VkLongPoll._init_server(get_ts = True)

Saving credintails for longpoll.

- get_ts

This parameter reserved.
________
### vkreal.VkLongPoll.get_event()
Getting one not-parsed event from longpoll.
________
### vkreal.VkLongPoll.listen()
Longpoll-listening generator, yield parsed events.
________
### vkreal.VkLongPoll.on_event(function)
Adding an async event handler.

- function

Asynchronus callback function, that will handle events.
on_event listener call this function with passing event in first argument.
________
### vkreal.VkBotLongPoll(api, group_id, loop = None)

Group longpoll using the same functions, as user longpoll.

- api

VkApi object for group longpoll initialization.

- group_id

Id of group, in which longpoll will be setted.

- loop

Asyncio loop, which will be used by event listener and handlers.
________
### vkreal.EventCreationTool.convert_event(event)

Parsing array-event to dict.

- event

Source array-event.
