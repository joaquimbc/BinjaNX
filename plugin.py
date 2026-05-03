from binaryninja.binaryview import BinaryView
from binaryninja.architecture import Architecture
from binaryninja.enums import SegmentFlag

from kaitaistruct import KaitaiStream
from formats.kip1 import Kip1
from parse import blz_decompress


class Kip1View(BinaryView):
    name = "KIP1-NX"
    long_name = "KIP1"

    def __init__(self, data):
        BinaryView.__init__(self, file_metadata=data.file, parent_view=data)
        
        self.data = Kip1(KaitaiStream(data))
        
        self.hdr = self.data.header

        unc_text = blz_decompress(self.data.body.text)
        unc_ro = blz_decompress(self.data.body.ro)
        unc_data = blz_decompress(self.data.body.data)

        self.raw = b"".join([unc_text, unc_ro, unc_data])
    


    @classmethod
    def is_valid_for_data(cls, data) -> bool:
        return data.read(0, 4) == b'KIP1'
    
    def perform_is_executable(self) -> bool:
        return True

    def perform_get_address_size(self) -> int:
        return 8
    
    #def parse(self):
    #    self.data = Kip1(KaitaiStream(self.raw))
    #    self.hdr = self.data.header




