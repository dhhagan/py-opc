''' Custom exceptions for the Alphasense OPC-N2 Library '''

class OpcError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
