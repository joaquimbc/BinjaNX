from io import BytesIO
import traceback

from binaryninja.binaryview import BinaryView, BinaryViewType
from binaryninja.architecture import Architecture
from binaryninja.platform import Platform
from binaryninja.enums import SegmentFlag, SymbolType
from binaryninja.types import Symbol
from binaryninja.log import log_error, log_info

from kaitaistruct import KaitaiStream
from .formats.kip1 import Kip1
from .parse import blz_decompress

# I dont think this is right, it starts at nnMain, but im not sure how to demangle anything yet
IMAGE_BASE = 0x0


class Kip1View(BinaryView):
    name = "KIP1-NX"
    long_name = "Nintendo Switch KIP1"

    def __init__(self, data):
        # no need for some magical shenenigans to remap/recreate a bv,
        # just load it raw and map it as memory later. Shoudln't have 
        # drawbacks I think
        BinaryView.__init__(self, parent_view=data, file_metadata=data.file)
        self.platform = Platform['switch-aarch64']
        # self.platform
        self.raw = data

    @classmethod
    def is_valid_for_data(cls, data) -> bool:
        return data.read(0, 4) == b'KIP1'

    def init(self) -> bool:
        try:
            raw_bytes = self.raw.read(0, self.raw.end)
            kip = Kip1(KaitaiStream(BytesIO(raw_bytes)))
            self.kip = kip
            hdr = kip.header

            log_info(f"KIP1: loading {hdr.name} (program_id={hex(hdr.program_id)})")

            # Apparently I can just cast the damn thing into bytes instead of that
            # utter mess that Google told me to do.... 
            text = bytes(blz_decompress(kip.body.text))
            ro   = bytes(blz_decompress(kip.body.ro))
            data = bytes(blz_decompress(kip.body.data))

            # Compute virtual addresses from the header. Lacks padding
            # for now, but I don't know if that's relevant
            text_va = IMAGE_BASE + hdr.text_segment.offset
            ro_va   = IMAGE_BASE + hdr.ro_segment.offset
            data_va = IMAGE_BASE + hdr.data_segment.offset
            bss_va  = IMAGE_BASE + hdr.bss_segment.offset

            RX = SegmentFlag.SegmentReadable | SegmentFlag.SegmentExecutable
            R  = SegmentFlag.SegmentReadable
            RW = SegmentFlag.SegmentReadable | SegmentFlag.SegmentWritable

            # Map each decompressed section directly into virtual memory
            # !!WARNING!!! this will make the regions be duplicated every time a
            # saved dabatase is loaded, I should gate this under some condition.
            # I'm just not sure how for now....
            mm = self.memory_map
            mm.add_memory_region("text", text_va, text, RX)
            mm.add_memory_region("ro",   ro_va,   ro,   R)
            mm.add_memory_region("data", data_va, data, RW)

            # bss is unbacked
            if hdr.bss_segment.size > 0:
                mm.add_memory_region("bss", bss_va, None,
                                     flags=RW, length=hdr.bss_segment.size)

            # Temporary "entry point"
            self.add_entry_point(text_va)
            self.define_auto_symbol(Symbol(SymbolType.FunctionSymbol, text_va, "_start"))

            return True
        except Exception:
            log_error(traceback.format_exc())
            return False

    def parse_mod(self):
        self.u64 = self.parse_type_string("uint64_t")

    def perform_is_executable(self) -> bool:
        return True

    def perform_get_address_size(self) -> int:
        return 8

    def perform_get_entry_point(self) -> int:
        return IMAGE_BASE + self.kip.header.text_segment.offset
    


class HorizonAarchPlatform(Platform):
    name = "switch-aarch64"


# Yes i just copy pasted this because including the other file was making it buggy
def blz_decompress(section: Kip1.BlzSection) -> bytearray:
    cmp_and_hdr_size = section.footer.compressed_size 
    header_size = section.footer.footer_size
    addl_size = section.footer.additional_size 

    compressed = section.body

    # Build the working buffer: compressed data padded out to final size
    out_size = cmp_and_hdr_size + addl_size
    buf = bytearray(out_size)
    buf[:len(compressed)] = compressed          # compressed data at the start

    cmp_ofs = cmp_and_hdr_size - header_size    # read cursor  (moves backward)
    out_ofs = out_size                           # write cursor (moves backward)

    while out_ofs > 0:
        cmp_ofs -= 1
        control = buf[cmp_ofs]

        for _ in range(8):
            if control & 0x80:                  # back-reference
                cmp_ofs -= 2
                seg_val = (buf[cmp_ofs + 1] << 8) | buf[cmp_ofs]
                seg_size = ((seg_val >> 12) & 0xF) + 3
                seg_ofs  = (seg_val & 0x0FFF) + 3

                seg_size = min(seg_size, out_ofs)   # clamp to remaining output
                out_ofs -= seg_size

                # byte-by-byte copy (overlapping reference is intentional)
                for j in range(seg_size):
                    buf[out_ofs + j] = buf[out_ofs + j + seg_ofs]

            else:                               # literal byte
                cmp_ofs -= 1
                out_ofs -= 1
                buf[out_ofs] = buf[cmp_ofs]

            control = (control << 1) & 0xFF     # ← the one place masking matters
            if out_ofs == 0:
                return buf

    return buf