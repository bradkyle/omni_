class Simulator():

    def respond(self, method, endpoint_id, args=None):
        return NotImplementedError

    def shuffle(self):
        return NotImplemented

    def wrap(self):
        return NotImplemented

    def modify(self):
        return NotImplemented

    def omit(self):
        return NotImplemented