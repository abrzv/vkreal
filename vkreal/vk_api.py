import httpx


class ApiError(Exception):
    source = None


"""
Class for calling vk api methods as ordinary class methods
"""

class ApiContext:
    def __init__(self, api):
        self.api = api

    async def _method_call(self, **kwargs):
        return await self.api.method(self.__temp__, kwargs)

    def __getattr__(self, method):
        self.__temp__ = method.replace("_", ".")
        return self._method_call


"""
Main api class
"""

class VkApi:
    def __init__(self, token, sess = None, v = "5.125"):
        self.token = token
        self.sess = sess if sess else httpx.AsyncClient()
        self.v = v

    def api_context(self):
        return ApiContext(self)

    async def method(self, name, params):
        temp_params = params.copy()

        temp_params["access_token"] = self.token
        temp_params["v"] = self.v

        response = await self.sess.get(
        url = "https://api.vk.com/method/" + name,
        params = temp_params)
        json_response = response.json()

        if "error" in json_response:
            error = ApiError(f"[{json_response['error']['error_code']}] {json_response['error']['error_msg']}")
            error.source = json_response["error"]
            raise error
        else:
            return json_response["response"]
