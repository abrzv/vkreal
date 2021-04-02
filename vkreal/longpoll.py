import httpx
import asyncio


class EventCreationTool:

    """
    Masks for convertation events from array to dictionary by id
    """

    events_mask = {
    1: [],
    2: ["message_id", "flags", "user_id"],
    3: ["message_id", "flags", "peer_id"],
    4: ["message_id", "mask", "peer_id", "timestamp", "text", "data", "attachments"],
    5: ["message_id", "mask", "peer_id", "timestamp", "text", "data", "attachments"],
    6: ["peer_id", "message_id", "local_id"],
    7: [],
    8: ["user_id", "platform", "timestamp", "app_id", "extra", "data"],
    9: ["user_id", "flags", "timestamp", "app_id", "extra", "data"],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    20: [],
    21: [],
    51: [],
    52: [],
    61: ["user_id", "flags"],
    62: ["user_id", "chat_id"],
    63: [],
    64: ["peer_id", "user_ids", "total_count", "timestamp"],
    70: [],
    80: ["count"],
    114: []}

    """
    Convertaton tool
    """

    def convert_event(event):
        params = {"type": event[0]}
        event = event[1:]

        if params["type"] in EventCreationTool.events_mask:
            for i in range(len(EventCreationTool.events_mask[params["type"]])):
                params[EventCreationTool.events_mask[params["type"]][i]] = event[i]

        return params


"""
Main user longpoll class
"""

class VkLongPoll:
    def __init__(self, api, v = "3", mode = 10, get_pts = False, loop = None):
        self.api = api
        self.v = v
        self.ts = None
        self.mode = mode
        self.get_pts = get_pts
        self.loop = loop if loop else asyncio.get_event_loop()

    """
    Initialize variables for longpoll
    """

    async def _init_server(self, get_ts = True):
        params = {
        "lp_version": self.v,
        "need_pts": self.get_pts}

        response = await self.api.method(
        "messages.getLongPollServer",
        params)

        self.key = response["key"]
        self.server = response["server"]
        self.server_url = "https://" + self.server
        if get_ts:
            self.ts = response["ts"]
            self.pts = response["pts"]


    """
    Get one, non-converted for normal format event
    """

    async def get_event(self):
        params = {
        "act": "a_check",
        "key": self.key,
        "ts": self.ts,
        "wait": 60,
        "mode": self.mode,
        "version": self.v}

        response = await self.api.sess.get(
        url = self.server_url,
        params = params,
        timeout = 70)
        json_response = response.json()

        if "failed" in json_response:
            if json_response["failed"] == 1:
                self.ts = json_response["ts"]
            elif json_response["failed"] == 2:
                await self._init_server(get_ts = False)
            elif json_response["failed"] == 3:
                await self._init_server()

            return []

        else:
            self.ts = json_response["ts"]
            if self.get_pts:
                self.pts = json_response["pts"]

            return json_response["updates"]

    """
    Longpoll listening
    Not recommended using it with processing in cycle, because it slows down the bot.
    """

    async def listen(self):
        await self._init_server()

        while True:
            try:
                for event in await self.get_event():
                    norm_event = EventCreationTool.convert_event(event)
                    yield norm_event
            except:
                pass

    """
    Sets asynchronus longpoll event handler
    """

    async def on_event(self, function):
        while True:
            try:
                for event in await self.get_event():
                    norm_event = EventCreationTool.convert_event(event)
                    self.loop.create_task(function(norm_event))
            except:
                pass


"""
Main group longpoll class
"""

class VkBotLongPoll:
    def __init__(self, api, group_id, loop = None):
        self.api = api
        self.group_id = group_id
        self.ts = None
        self.__started__ = False
        self.loop = loop if loop else asyncio.get_event_loop()

    async def _init_server(self, get_ts = True):
        self.__started__ = True
        params = {
        "group_id": self.group_id}

        response = await self.api.method(
        "groups.getLongPollServer",
        params)

        self.key = response["key"]
        self.server = response["server"]
        self.server_url = self.server
        if get_ts:
            self.ts = response["ts"]

    async def get_event(self):
        params = {
        "act": "a_check",
        "key": self.key,
        "ts": self.ts,
        "wait": 60}

        response = await self.api.sess.get(
        url = self.server_url,
        params = params,
        timeout = 70)
        json_response = response.json()

        if "failed" in json_response:
            if json_response["failed"] == 1:
                self.ts = json_response["ts"]
            elif json_response["failed"] == 2:
                await self._init_server(get_ts = False)
            elif json_response["failed"] == 3:
                await self._init_server()

            return []

        else:
            self.ts = json_response["ts"]

            return json_response["updates"]

    async def listen(self):
        if not self.__started__:
            await self._init_server()

        while True:
            try:
                for event in await self.get_event():
                    yield norm_event
            except:
                pass

    async def on_event(self, function):
        while True:
            try:
                for event in await self.get_event():
                    self.loop.create_task(function(event))
            except:
                pass
