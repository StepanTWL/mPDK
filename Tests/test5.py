class Command:

    def __init__(self, parent=None):
        super(self).__init__(parent)
        self.queue = queue
        self.transmit_frame = transmit_frame
        self.transmit_size = transmit_size
        self.receive_frame = receive_frame
        self.receive_size = receive_size
        self.errors = dict()
        self.delay = delay

    def


