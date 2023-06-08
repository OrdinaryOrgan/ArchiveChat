class FileSplitterReader:
    def __init__(self, filename, part_size = 1024) -> None:
        self.fllename = filename 
        self.file = open(filename, 'rb')
        self.part_size = part_size
        self.file.seek(0, 2)
        self.file_size = self.file.tell()
        self.part_count = int(self.file_size/part_size)
        self.file.seek(0, 0)
        self.part_send = 0
        self.at_eof = False

    def set_pos(self, i):
        self.part_send = i
        self.file.seek(i*self.part_size, 0)

    def read(self):
        self.part_send = self.part_send + 1
        r = self.file.read(self.part_size)
        if len(r) == 0:
            self.at_eof = True
        return self.part_send, r
    
    def eof(self):
        return self.at_eof

    def __del__(self):
        self.file.close()

class FileSplitterWriter:
    def __init__(self, filename, part_size = 1024) -> None:
        self.filename = filename
        self.file = open(filename, 'wb+')
        self.part_recv = 0
        self.part_size = part_size

    def set_pos(self, i):
        self.part_recv = i
        self.file.seek(i*self.part_size, 0)

    def test_pos(self, i):
        return self.part_recv + 1 == i

    def write(self, buf):
        self.part_recv = self.part_recv + 1
        self.file.write(buf)

    def __del__(self):
        self.file.close()