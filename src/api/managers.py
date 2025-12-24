messages = []
return_messages = []

class MessageQueue:
    def __init__(self):
        self.messages = messages
        self.return_messages = return_messages

    def add_messages(self,data=None):
        self.messages.append(data)

    def get_messages(self,data=None):
        self.return_messages.append(data)

Message = MessageQueue()