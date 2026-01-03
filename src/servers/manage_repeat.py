import requests


class DefaultInterfaceUrl:
    LOCALHOST = 'localhost'
    PORT = 8000
    GETINTERFRACEIRL = "/api/inside/get/"
    POSTINTERFRACEIRL = "/api/inside/post/"

class MessagesRepeat:
    def __init__(self):
        self.requests = requests.Session()
        self.default = DefaultInterfaceUrl()
        self.localhost = self.default.LOCALHOST
        self.get = self.default.GETINTERFRACEIRL
        self.post = self.default.POSTINTERFRACEIRL
        self.port = self.default.PORT

    def sendmessage(self,message):
        url = f"http://{self.localhost}:{self.port}/{self.post}"
        try:
            self.requests.post(url,data=message)
        except requests.exceptions.ConnectionError:
            print("Connection error")

    def getmessage(self):
        url = f"http://{self.localhost}:{self.port}/{self.get}"
        data = self.requests.get(url)
        return data