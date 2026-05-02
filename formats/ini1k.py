# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Ini1(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Ini1, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.ini1_file_header = Ini1.Ini1Header(self._io, self, self._root)
        self.kip1_program = []
        for i in range(self.ini1_file_header.kip_count):
            self.kip1_program.append(Ini1.Kip1Program(self._io, self, self._root))



    def _fetch_instances(self):
        pass
        self.ini1_file_header._fetch_instances()
        for i in range(len(self.kip1_program)):
            pass
            self.kip1_program[i]._fetch_instances()


    class Ini1Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Ini1.Ini1Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x49\x4E\x49\x31":
                raise kaitaistruct.ValidationNotEqualError(b"\x49\x4E\x49\x31", self.magic, self._io, u"/types/ini1_header/seq/0")
            self.size = self._io.read_u4le()
            self.kip_count = self._io.read_u4le()
            self.reserved = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class Kip1Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Ini1.Kip1Header, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x4B\x49\x50\x31":
                raise kaitaistruct.ValidationNotEqualError(b"\x4B\x49\x50\x31", self.magic, self._io, u"/types/kip1_header/seq/0")
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(12), 0, False)).decode(u"ASCII")
            self.program_id = self._io.read_u8le()
            self.version = self._io.read_u4le()
            self.mthread_priority = self._io.read_u1()
            self.mthread_core_num = self._io.read_u1()
            self.reserved0 = self._io.read_u1()
            self.flags = self._io.read_u1()
            self.text_segment = Ini1.Kip1Segment(self._io, self, self._root)
            self.mthread_affinity_mask = self._io.read_u4le()
            self.ro_segment = Ini1.Kip1Segment(self._io, self, self._root)
            self.mthread_stack_size = self._io.read_u4le()
            self.data_segment = Ini1.Kip1Segment(self._io, self, self._root)
            self.reserved1 = self._io.read_u4le()
            self.bss_segment = Ini1.Kip1Segment(self._io, self, self._root)
            self.reserved2 = self._io.read_bytes(36)
            self.kernel_capabilities = self._io.read_bytes(128)


        def _fetch_instances(self):
            pass
            self.text_segment._fetch_instances()
            self.ro_segment._fetch_instances()
            self.data_segment._fetch_instances()
            self.bss_segment._fetch_instances()

        @property
        def total_size(self):
            if hasattr(self, '_m_total_size'):
                return self._m_total_size

            self._m_total_size = ((self.text_segment.compressed_size + self.ro_segment.compressed_size) + self.data_segment.compressed_size) + self.bss_segment.compressed_size
            return getattr(self, '_m_total_size', None)


    class Kip1Program(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Ini1.Kip1Program, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self._raw_header = self._io.read_bytes(256)
            _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
            self.header = Ini1.Kip1Header(_io__raw_header, self, self._root)
            self.body = self._io.read_bytes(self.header.total_size)


        def _fetch_instances(self):
            pass
            self.header._fetch_instances()


    class Kip1Segment(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Ini1.Kip1Segment, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.compressed_size = self._io.read_u4le()


        def _fetch_instances(self):
            pass