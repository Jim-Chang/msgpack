import struct
from io import BytesIO


def pack(obj, using_single_float=False):
    packer = Packer(using_single_float=using_single_float)
    return packer.pack(obj)


class Packer:
    def __init__(self, using_single_float=False):
        self._buffer = BytesIO()
        self._using_single_float = using_single_float

    def pack(self, obj) -> bytes:
        self._buffer = BytesIO()
        self._pack(obj)
        return self._buffer.getvalue()

    def _pack(self, obj):
        if obj is None:
            self._pack_none(obj)
        elif isinstance(obj, bool):
            self._pack_bool(obj)
        elif isinstance(obj, int):
            self._pack_int(obj)
        elif isinstance(obj, float):
            self._pack_float(obj)
        elif isinstance(obj, str):
            self._pack_str(obj)
        elif isinstance(obj, (bytes, bytearray)):
            self._pack_bytes(obj)
        elif isinstance(obj, (list, tuple)):
            self._pack_array(obj)
        elif isinstance(obj, dict):
            self._pack_dict(obj)
        else:
            raise TypeError("Cannot pack object of type %s" % type(obj))

    def _pack_int(self, obj: int):
        if 0 <= obj < 0x80:
            self._pack_positive_fix_int(obj)
        elif 0x80 <= obj <= 0xFF:
            self._pack_uint8(obj)
        elif 0xFF < obj <= 0xFFFF:
            self._pack_uint16(obj)
        elif 0xFF < obj <= 0xFFFFFFFF:
            self._pack_uint32(obj)
        elif 0xFFFFFFFF < obj <= 0xFFFFFFFFFFFFFFFF:
            self._pack_uint64(obj)
        elif -0x20 <= obj < 0:
            self._pack_negative_fix_int(obj)
        elif -0x80 <= obj < -0x20:
            self._pack_int8(obj)
        elif -0x8000 <= obj < -0x80:
            self._pack_int16(obj)
        elif -0x80000000 <= obj < 0x8000:
            self._pack_uint32(obj)
        elif -0x8000000000000000 <= obj < -0x80000000:
            self._pack_uint64(obj)

    def _pack_positive_fix_int(self, obj: int):
        self._buffer.write(bytes([obj]))

    def _pack_uint8(self, obj: int):
        self._buffer.write(b"\xcc")
        self._buffer.write(obj.to_bytes(1, byteorder="big"))

    def _pack_uint16(self, obj: int):
        self._buffer.write(b"\xcd")
        self._buffer.write(obj.to_bytes(2, byteorder="big"))

    def _pack_uint32(self, obj: int):
        self._buffer.write(b"\xce")
        self._buffer.write(obj.to_bytes(4, byteorder="big"))

    def _pack_uint64(self, obj: int):
        self._buffer.write(b"\xcf")
        self._buffer.write(obj.to_bytes(8, byteorder="big"))

    def _pack_negative_fix_int(self, obj: int):
        # 224 = 0xe0
        # -32 => 0x00000 => 0
        # -1 => 0x11111 => 31
        self._buffer.write((224 + obj + 32).to_bytes(1, byteorder="big"))

    def _pack_int8(self, obj: int):
        self._buffer.write(b"\xd0")
        self._buffer.write(obj.to_bytes(1, byteorder="big", signed=True))

    def _pack_int16(self, obj: int):
        self._buffer.write(b"\xd1")
        self._buffer.write(obj.to_bytes(2, byteorder="big", signed=True))

    def _pack_int32(self, obj: int):
        self._buffer.write(b"\xd2")
        self._buffer.write(obj.to_bytes(4, byteorder="big", signed=True))

    def _pack_int64(self, obj: int):
        self._buffer.write(b"\xd3")
        self._buffer.write(obj.to_bytes(8, byteorder="big", signed=True))

    def _pack_float(self, obj: float):
        if self._using_single_float:
            self._pack_single_float(obj)
        else:
            self._pack_double_float(obj)

    def _pack_single_float(self, obj: float):
        self._buffer.write(b"\xca")
        self._buffer.write(struct.pack(">f", obj))

    def _pack_double_float(self, obj: float):
        self._buffer.write(b"\xcb")
        self._buffer.write(struct.pack(">d", obj))

    def _pack_str(self, obj: str):
        byte_str = obj.encode("utf-8")
        byte_len = len(byte_str)
        if byte_len > 0xFFFFFFFF:
            raise Exception("String is too long to pack")
        if byte_len <= 0x1F:
            self._pack_fix_str(byte_str)
        elif byte_len <= 0xFF:
            self._pack_str8(byte_str)
        elif byte_len <= 0xFFFF:
            self._pack_str16(byte_str)
        elif byte_len <= 0xFFFFFFFF:
            self._pack_str32(byte_str)

    def _pack_fix_str(self, byte_str: bytes):
        self._buffer.write((0xA0 + len(byte_str)).to_bytes(1, byteorder="big"))
        self._buffer.write(byte_str)

    def _pack_str8(self, byte_str: bytes):
        self._buffer.write(b"\xd9")
        self._buffer.write(len(byte_str).to_bytes(1, byteorder="big"))
        self._buffer.write(byte_str)

    def _pack_str16(self, byte_str: bytes):
        self._buffer.write(b"\xda")
        self._buffer.write(len(byte_str).to_bytes(2, byteorder="big"))
        self._buffer.write(byte_str)

    def _pack_str32(self, byte_str: bytes):
        self._buffer.write(b"\xdb")
        self._buffer.write(len(byte_str).to_bytes(4, byteorder="big"))
        self._buffer.write(byte_str)

    def _pack_bytes(self, obj: bytes | bytearray):
        byte_len = len(obj)
        if byte_len > 0xFFFFFFFF:
            raise Exception("Bytes is too long to pack")
        if byte_len <= 0xFF:
            self._pack_bin8(obj)
        elif byte_len <= 0xFFFF:
            self._pack_bin16(obj)
        elif byte_len <= 0xFFFFFFFF:
            self._pack_bin32(obj)

    def _pack_bin8(self, obj):
        self._buffer.write(b"\xc4")
        self._buffer.write(len(obj).to_bytes(1, byteorder="big"))
        self._buffer.write(obj)

    def _pack_bin16(self, obj):
        self._buffer.write(b"\xc5")
        self._buffer.write(len(obj).to_bytes(2, byteorder="big"))
        self._buffer.write(obj)

    def _pack_bin32(self, obj):
        self._buffer.write(b"\xc6")
        self._buffer.write(len(obj).to_bytes(4, byteorder="big"))
        self._buffer.write(obj)

    def _pack_array(self, obj):
        list_len = len(obj)
        if list_len > 0xFFFFFFFF:
            raise Exception("List is too long to pack")
        if list_len <= 0xF:
            self._pack_fix_array(obj)
        elif list_len <= 0xFFFF:
            self._pack_array16(obj)
        elif list_len <= 0xFFFFFFFF:
            self._pack_array32(obj)

    def _pack_fix_array(self, obj):
        self._buffer.write((0x90 + len(obj)).to_bytes(1, byteorder="big"))
        for item in obj:
            self._pack(item)

    def _pack_array16(self, obj):
        self._buffer.write(b"\xdc")
        self._buffer.write(len(obj).to_bytes(2, byteorder="big"))
        for item in obj:
            self._pack(item)

    def _pack_array32(self, obj):
        self._buffer.write(b"\xdd")
        self._buffer.write(len(obj).to_bytes(4, byteorder="big"))
        for item in obj:
            self._pack(item)

    def _pack_dict(self, obj):
        pass

    def _pack_bool(self, obj: bool):
        if obj is True:
            self._buffer.write(b"\xc3")
        else:
            self._buffer.write(b"\xc2")

    def _pack_none(self, obj):
        self._buffer.write(b"\xc0")
