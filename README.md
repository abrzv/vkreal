# vkreal
Simple asynchronus wrapper for vk_api.

Version 1.0.0.
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
_______
### vkreal.VkApi.api_context()
Creates and initializes ApiContext class with current VkApi class.
_______
_______
### vkreal.VkApi.method(name, params)
- name

Method name. You can see a list of all methods [here](https://vk.com/dev/methods).
- params

Parameters, with which method will be called.
You can see it in https://vk.com/dev/method.name
_______
_______
