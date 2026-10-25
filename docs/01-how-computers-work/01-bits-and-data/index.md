# Bits and data

A compact reference for the chapter. Each section links the lesson that teaches it.

## Lessons

1. [Binary and hexadecimal](01-binary-and-hexadecimal.md)
2. [Bits, bytes and units](02-bits-bytes-and-units.md)
3. [Integers and two's complement](03-integers-and-twos-complement.md)
4. [Floating point](04-floating-point.md)
5. [Text, ASCII and Unicode](05-text-ascii-and-unicode.md)
6. [Files, images and sound as bytes](06-files-images-and-sound-as-bytes.md)

## Bases and Python syntax

| Base | Prefix | Digits | Python to text | Python from text |
|---|---|---|---|---|
| 2 | `0b` | 0, 1 | `bin(n)`, `f"{n:08b}"` | `int(s, 2)` |
| 8 | `0o` | 0 to 7 | `oct(n)` | `int(s, 8)` |
| 16 | `0x` | 0 to 9, a to f | `hex(n)`, `f"{n:02x}"` | `int(s, 16)` |

One hex digit is 4 bits (a nibble); two make a byte. Operators: `&` AND, `|` OR, `^` XOR, `~` NOT, `<<` and `>>` shifts. Parenthesize masks: `(x & 0xF) == 0`. See [binary and hexadecimal](01-binary-and-hexadecimal.md).

## Units

| Quantity | Value |
|---|---|
| 1 byte | 8 bits, 256 values |
| $n$ bits | $2^n$ values |
| 1 kB, 1 MB, 1 GB | $10^3$, $10^6$, $10^9$ bytes |
| 1 KiB, 1 MiB, 1 GiB | $2^{10}$, $2^{20}$, $2^{30}$ bytes |
| 1 TB drive in GiB | 931.32 |
| Mbps to MB/s | divide by 8 |

Lowercase `b` is bits, uppercase `B` is bytes. Download time is size in bits divided by speed in bits per second. See [bits, bytes and units](02-bits-bytes-and-units.md).

## Integer ranges

| Width | Signed | Unsigned |
|---|---|---|
| 8 bits | $-128$ to 127 | 0 to 255 |
| 16 bits | $-32{,}768$ to 32,767 | 0 to 65,535 |
| 32 bits | $-2{,}147{,}483{,}648$ to 2,147,483,647 | 0 to 4,294,967,295 |
| 64 bits | about $\pm 9.2 \times 10^{18}$ | 0 to about $1.8 \times 10^{19}$ |

Two's complement: flip every bit and add 1 to negate. The top bit has place value $-2^{n-1}$. Overflow wraps modulo $2^n$ in Java and Go, is undefined behaviour for signed integers in C, and panics in Rust debug builds. A signed 32-bit time ends on 19 January 2038, 03:14:07 UTC. See [integers and two's complement](03-integers-and-twos-complement.md).

## Floating point

A double (binary64) has 1 sign bit, 11 exponent bits and 52 significand bits, about 15 to 17 decimal digits. Integers are exact only up to $2^{53}$.

| Rule | Why |
|---|---|
| Compare with `math.isclose(a, b)`, not `==` | `0.1 + 0.2` is `0.30000000000000004` |
| Test NaN with `math.isnan(x)` | NaN is not equal to itself |
| Store money as integer cents or `Decimal` | Floats cannot hold 0.1 exactly |
| Write `Decimal("0.1")`, not `Decimal(0.1)` | The float's error is copied |

See [floating point](04-floating-point.md).

## Text

| Character | Code point | UTF-8 bytes |
|---|---|---|
| `A` | U+0041 | 1 (`41`) |
| `é` | U+00E9 | 2 (`c3 a9`) |
| `€` | U+20AC | 3 (`e2 82 ac`) |
| emoji such as U+1F600 | U+1F600 | 4 (`f0 9f 98 80`) |

`len(s)` counts code points; `len(s.encode("utf-8"))` counts bytes. Always pass `encoding="utf-8"` to `open()`. Mojibake such as `cafÃ©` is UTF-8 read as Latin-1 or cp1252; repair with `s.encode("latin-1").decode("utf-8")`. Normalize with `unicodedata.normalize("NFC", s)` before comparing. See [text, ASCII and Unicode](05-text-ascii-and-unicode.md).

## Files, images and sound

| Format | Signature (hex) |
|---|---|
| PNG | `89 50 4e 47 0d 0a 1a 0a` |
| JPEG | `ff d8 ff` |
| GIF | `47 49 46 38` |
| PDF | `25 50 44 46 2d` |
| ZIP, DOCX, XLSX, JAR | `50 4b 03 04` |
| gzip | `1f 8b` |
| ELF | `7f 45 4c 46` |

Image bytes: width $\times$ height $\times$ bytes per pixel. Sound bytes: sample rate $\times$ bytes per sample $\times$ channels $\times$ seconds. CD audio is 44,100 samples per second at 16 bits. Open binary files with `"rb"`. See [files, images and sound as bytes](06-files-images-and-sound-as-bytes.md).
