from io import BytesIO


def pack(obj):
    packer = Packer()
    return packer.pack(obj)


class Packer:
    def __init__(self):
        self._buffer = BytesIO()

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
            self._pack_string(obj)
        elif isinstance(obj, bytes):
            self._pack_bytes(obj)
        elif isinstance(obj, (list, tuple)):
            self._pack_list(obj)
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

    def _pack_float(self, obj):
        pass

    def _pack_string(self, obj):
        pass

    def _pack_bytes(self, obj):
        pass

    def _pack_list(self, obj):
        pass

    def _pack_dict(self, obj):
        pass

    def _pack_bool(self, obj: bool):
        if obj is True:
            self._buffer.write(b"\xc3")
        else:
            self._buffer.write(b"\xc2")

    def _pack_none(self, obj):
        self._buffer.write(b"\xc0")
