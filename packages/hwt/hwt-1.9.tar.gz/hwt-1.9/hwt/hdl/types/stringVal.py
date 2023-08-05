from hwt.hdl.value import Value
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.typeCast import toHVal


class StringVal(Value):
    """
    Value class for hdl String type
    """

    @classmethod
    def fromPy(cls, val, typeObj):
        assert isinstance(val, str) or val is None
        vld = 0 if val is None else 1
        if not vld:
            val = ""
        return cls(val, typeObj, vld)

    def _eq__val(self, other):
        eq = self.val == other.val
        vld = int(self.vldMask and other.vldMask)
        updateTime = max(self.updateTime, other.updateTime)

        return BOOL.getValueCls()(eq, BOOL, vld, updateTime)

    def _eq(self, other):
        other = toHVal(other)
        if isinstance(other, Value):
            return self._eq__val(other)
        else:
            raise NotImplementedError()
