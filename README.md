## Simple code for Arithmetic (Range) Coding
- Both encoder and decoder are in the same class.
- Encoder encodes to a float number.
- Decoder uses this float number and decodes (independently) given also the message length.
- Checkout test for usage.

### Simple usage:
```
test_symbol_prob: dict[str, Decimal] = {
"a": Decimal("0.2"),
"b": Decimal("0.5"),
"c": Decimal("0.3")
}
acoder = ArithmeticCoder(test_symbol_prob)

```

#### TODOS:
- use bitstream libray to finish encoding to a bitstream
e.g.
```
f1 = bitstring.BitArray(float=Decimal("1.1"), length=32)
f2 = bitstring.Bits(bin=f1.bin, length=32)
```
