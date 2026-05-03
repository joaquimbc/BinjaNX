from binaryninja.binaryview import BinaryView, BinaryReader, BinaryWriter
from binaryninja.architecture import Architecture
from binaryninja.enums import Endianness, SegmentFlag
from io import BytesIO

from kaitaistruct import KaitaiStream
from .formats.kip1 import Kip1
from .parse import blz_decompress


class Kip1View(BinaryView):
    name = "KIP1-NX"
    long_name = "KIP1"
    # reader = BinaryReader
    # writer = BinaryWriter

    def __init__(self, data):
        # BinaryView.__init__(self, file_metadata=data.file, parent_view=data)
        self.raw = data
        self.breader = BinaryReader(data, Endianness.LittleEndian)
        self.bwriter = BinaryWriter(data, Endianness.LittleEndian)

        pqp = self.breader.read(0, data.end)

        if pqp is not None:
            self.data = Kip1(KaitaiStream(BytesIO(pqp)))
        
        self.hdr = self.data.header

        unc_text = blz_decompress(self.data.body.text)
        unc_ro = blz_decompress(self.data.body.ro)
        unc_data = blz_decompress(self.data.body.data)

        self.breader.seek(0)
        header = self.breader.read(0x100, 0)

        if header is not None:
            self.raw = b"".join([header, unc_text, unc_ro, unc_data])

        data.write(0, self.raw)
        BinaryView.__init__(self, file_metadata=data.file, parent_view=data)
    
    @classmethod
    def is_valid_for_data(cls, data) -> bool:
        return data.read(0, 4) == b'KIP1'
    
    def perform_is_executable(self) -> bool:
        return True

    def perform_get_address_size(self) -> int:
        return 8
    
    def init(self):
        self.add_auto_segment(0x0, self.hdr.text_segment.size, 0x0, 0x10F000, SegmentFlag.SegmentExecutable | SegmentFlag.SegmentReadable)
        return True
    
    #def parse(self):
    #    self.data = Kip1(KaitaiStream(self.raw))
    #    self.hdr = self.data.header




