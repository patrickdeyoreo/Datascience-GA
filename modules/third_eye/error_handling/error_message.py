class ErrorMessage(object):

    _messages = {
        'TypeError': "attr. '{}' must be of type {}",
    }

    def __init__(self):
        self._messages = ErrorMessage._messages.copy()

    @property
    def messages(self):
        return self._messages
    
    def disp(self, key, *args):
        print(self.gen(key, *args))

    def gen(self, key, *args):
        return self._messages[key].format(*args)
