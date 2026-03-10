class ClientSession:
    def __init__(self, read_stream, write_stream):
        self.read_stream = read_stream
        self.write_stream = write_stream

    def initialize(self):
        pass
