from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdl.operatorDefs import AllOps


# keep in mind that there is no such a thing in vhdl itself
opPrecedence = {AllOps.NOT: 2,
                AllOps.RISING_EDGE: 1,
                AllOps.NEG: 2,
                AllOps.DIV: 3,
                AllOps.ADD: 3,
                AllOps.SUB: 3,
                AllOps.MUL: 3,
                AllOps.XOR: 2,
                AllOps.EQ: 2,
                AllOps.NEQ: 2,
                AllOps.AND: 2,
                AllOps.OR: 2,
                AllOps.DOWNTO: 2,
                AllOps.GT: 2,
                AllOps.LT: 2,
                AllOps.GE: 2,
                AllOps.LE: 2,
                AllOps.CONCAT: 2,
                AllOps.INDEX: 1,
                AllOps.TERNARY: 1,
                AllOps.CALL: 1,
                }


def isResultOfTypeConversion(sig):
    try:
        sig.drivers[0]
    except IndexError:
        return False

    if sig.hidden:
        return True
    return False


class VhdlSerializer_ops():

    @classmethod
    def Operator(cls, op, ctx):
        def p(operand):
            s = cls.asHdl(operand, ctx)
            if isinstance(operand, RtlSignalBase):
                try:
                    o = operand.singleDriver()
                    if o.operator != op.operator and\
                            opPrecedence[o.operator] <= opPrecedence[op.operator]:
                        return "(%s)" % s
                except Exception:
                    pass
            return s
        # [TODO] no nested ternary in expressions like
        # ( '1'  WHEN r = f ELSE  '0' ) & "0"
        ops = op.operands
        o = op.operator

        def _bin(name):
            return name.join(map(p, ops))

        if o == AllOps.AND:
            return _bin(' AND ')
        elif o == AllOps.OR:
            return _bin(' OR ')
        elif o == AllOps.XOR:
            return _bin(' XOR ')
        elif o == AllOps.NOT:
            assert len(ops) == 1
            return "NOT " + p(ops[0])
        elif o == AllOps.CALL:
            return "%s(%s)" % (cls.FunctionContainer(ops[0]),
                               ", ".join(map(p, ops[1:])))
        elif o == AllOps.CONCAT:
            return _bin(' & ')
        elif o == AllOps.DIV:
            return _bin(' / ')
        elif o == AllOps.DOWNTO:
            return _bin('-1 DOWNTO ')
        elif o == AllOps.TO:
            return _bin('-1 TO ')
        elif o == AllOps.EQ:
            return _bin(' = ')
        elif o == AllOps.GT:
            return _bin(' > ')
        elif o == AllOps.GE:
            return _bin(' >= ')
        elif o == AllOps.LE:
            return _bin(' <= ')
        elif o == AllOps.INDEX:
            assert len(ops) == 2
            o1 = ops[0]
            if isinstance(o1, RtlSignalBase) and isResultOfTypeConversion(o1):
                o1 = ctx.createTmpVarFn("tmpTypeConv", o1._dtype)
                o1.defaultVal = ops[0]

            return "%s(%s)" % (cls.asHdl(o1, ctx).strip(), p(ops[1]))
        elif o == AllOps.LT:
            return _bin(' < ')
        elif o == AllOps.SUB:
            return _bin(' - ')
        elif o == AllOps.MUL:
            return _bin(' * ')
        elif o == AllOps.NEQ:
            return _bin(' /= ')
        elif o == AllOps.ADD:
            return _bin(' + ')
        elif o == AllOps.NEG:
            return "-(%s)" % (p(ops[0]))
        elif o == AllOps.TERNARY:
            return " ".join([p(ops[1]), "WHEN",
                             cls.condAsHdl([ops[0]], True, ctx),
                             "ELSE",
                             p(ops[2])])
        elif o == AllOps.RISING_EDGE:
            assert len(ops) == 1
            return "RISING_EDGE(" + p(ops[0]) + ")"
        elif o == AllOps.FALLIGN_EDGE:
            assert len(ops) == 1
            return "FALLING_EDGE(" + p(ops[0]) + ")"
        elif o == AllOps.BitsAsSigned:
            assert len(ops) == 1
            return "SIGNED(" + p(ops[0]) + ")"
        elif o == AllOps.BitsAsUnsigned:
            assert len(ops) == 1
            return "UNSIGNED(" + p(ops[0]) + ")"
        elif o == AllOps.BitsAsVec:
            assert len(ops) == 1
            return "STD_LOGIC_VECTOR(" + p(ops[0]) + ")"
        elif o == AllOps.BitsToInt:
            assert len(ops) == 1
            op = cls.asHdl(ops[0], ctx)
            if ops[0]._dtype.signed is None:
                op = "UNSIGNED(%s)" % op
            return "TO_INTEGER(%s)" % op
        elif o == AllOps.IntToBits:
            assert len(ops) == 1
            resT = op.result._dtype
            op_str = cls.asHdl(ops[0], ctx)
            w = resT.bit_length()

            if resT.signed is None:
                return "STD_LOGIC_VECTOR(TO_UNSIGNED(" + op_str + ", %d))" % (w)
            elif resT.signed:
                return "TO_UNSIGNED(" + op_str + ", %d)" % (w)
            else:
                return "TO_UNSIGNED(" + op_str + ", %d)" % (w)

        elif o == AllOps.POW:
            assert len(ops) == 2
            return _bin(' ** ')
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to vhdl" % (o))
