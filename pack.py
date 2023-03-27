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

    def _pack_int(self, obj):
        pass

    def _pack_positive_fix_int(self, obj):
        pass

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

    def _pack_bool(self, obj):
        if obj is True:
            self._buffer.write(b"\xc3")
        else:
            self._buffer.write(b"\xc2")

    def _pack_none(self, obj):
        self._buffer.write(b"\xc0")
