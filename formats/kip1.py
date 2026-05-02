# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Kip1(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        super(Kip1, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self._raw_header = self._io.read_bytes(256)
        _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
        self.header = Kip1.Kip1Header(_io__raw_header, self, self._root)
        self.body = Kip1.BlzBody(self._io, self, self._root)


    def _fetch_instances(self):
        pass
        self.header._fetch_instances()
        self.body._fetch_instances()

    class BlzBody(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Kip1.BlzBody, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self._raw_text = self._io.read_bytes(self._root.header.text_segment.compressed_size)
            _io__raw_text = KaitaiStream(BytesIO(self._raw_text))
            self.text = Kip1.BlzSection(_io__raw_text, self, self._root)
            self._raw_ro = self._io.read_bytes(self._root.header.ro_segment.compressed_size)
            _io__raw_ro = KaitaiStream(BytesIO(self._raw_ro))
            self.ro = Kip1.BlzSection(_io__raw_ro, self, self._root)
            self._raw_data = self._io.read_bytes(self._root.header.data_segment.compressed_size)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = Kip1.BlzSection(_io__raw_data, self, self._root)


        def _fetch_instances(self):
            pass
            self.text._fetch_instances()
            self.ro._fetch_instances()
            self.data._fetch_instances()


    class BlzFooter(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Kip1.BlzFooter, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.compressed_size = self._io.read_u4le()
            self.footer_size = self._io.read_u4le()
            self.additional_size = self._io.read_u4le()


        def _fetch_instances(self):
            pass


    class BlzSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Kip1.BlzSection, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.body = self._io.read_bytes(self._io.size() - 12)
            self._raw_footer = self._io.read_bytes(12)
            _io__raw_footer = KaitaiStream(BytesIO(self._raw_footer))
            self.footer = Kip1.BlzFooter(_io__raw_footer, self, self._root)


        def _fetch_instances(self):
            pass
            self.footer._fetch_instances()


    class Kip1Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Kip1.Kip1Header, self).__init__(_io)
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
            self.text_segment = Kip1.Kip1Segment(self._io, self, self._root)
            self.mthread_affinity_mask = self._io.read_u4le()
            self.ro_segment = Kip1.Kip1Segment(self._io, self, self._root)
            self.mthread_stack_size = self._io.read_u4le()
            self.data_segment = Kip1.Kip1Segment(self._io, self, self._root)
            self.reserved1 = self._io.read_u4le()
            self.bss_segment = Kip1.Kip1Segment(self._io, self, self._root)
            self.reserved2 = self._io.read_bytes(36)
            self.kernel_capabilities = self._io.read_bytes(128)


        def _fetch_instances(self):
            pass
            self.text_segment._fetch_instances()
            self.ro_segment._fetch_instances()
            self.data_segment._fetch_instances()
            self.bss_segment._fetch_instances()


    class Kip1Segment(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            super(Kip1.Kip1Segment, self).__init__(_io)
            self._parent = _parent
            self._root = _root
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.compressed_size = self._io.read_u4le()


        def _fetch_instances(self):
            pass



