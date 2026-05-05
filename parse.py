from kaitaistruct import KaitaiStream

from .formats import ini1k
from .formats import kip1

from pathlib import Path

def ini1_parse(ini1_file: str, outdir: str):
    Ini1 = ini1k.Ini1
    out_dir = Path("kip1")
    out_dir.mkdir(exist_ok=True)

    with open("D:/Pessoal/nx/binaries/INI1.bin", "rb") as f:
        result = Ini1(KaitaiStream(f))

    for i, kip in enumerate(result.kip1_program):

        print(f"KIP1 {i}: {kip.header.name}")
        print(f"Title ID: {hex(kip.header.program_id)}")
        print(f"Compressed .text size: {hex(kip.header.text_segment.compressed_size)}")
        print(f"Compressed .ro size: {hex(kip.header.ro_segment.compressed_size)}")
        print(f"Compressed .data size: {hex(kip.header.data_segment.compressed_size)}")
        print(f".bss (mapped) size: {hex(kip.header.bss_segment.size)}")
        print(f"Priotity: {kip.header.mthread_priority}")
        print(f"Core: {kip.header.mthread_affinity_mask}")

        path = out_dir / f"{kip.header.name}.kip"
        try:
            with path.open("xb") as out:
                out.write(kip._raw_header + kip.body)
                print(f"Saved dumped KIP1 to kip1/{kip.header.name}.kip1")
        
        except FileExistsError:
            print(f"{kip.header.name}.kip1 already exists, skipping!")

        print("")

Kip1 = kip1.Kip1

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



# D:/Pessoal/nx/binaries/INI1.bin


ini1_parse("a", "a")

with open("D:/Pessoal/nx/code/parser/kip1/FS.kip", "rb") as f:
        result = Kip1(KaitaiStream(f))

print(f"Loaded built-in sysmodule: {result.header.name}")
print(f"Title ID: {hex(result.header.program_id)}")
print(f"Version: {result.header.version}")
print(f"Main thread priority: {result.header.mthread_priority}")
print(f"Main thread core affinity: {result.header.mthread_affinity_mask}")

with open("porraaa.kip", "wb") as f:
    f.write(blz_decompress(result.body.text))
    f.write(blz_decompress(result.body.ro))
    f.write(blz_decompress(result.body.data))


