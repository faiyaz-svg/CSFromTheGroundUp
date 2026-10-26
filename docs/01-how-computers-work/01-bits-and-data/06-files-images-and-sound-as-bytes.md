# Files, images and sound as bytes

After this you can say what is actually inside a file, work out how big an uncompressed image or sound is, and identify a file by its first bytes.

Before this: [text, ASCII and Unicode](05-text-ascii-and-unicode.md).

## The idea

A user uploads `report.pdf` to your app, and it is really a renamed `.exe`. A designer sends a "photo" that is 40 MB. A one-minute voice recording takes 5 MB as a WAV file and under 1 MB as an MP3. In every case the file is a sequence of bytes, and the only questions are what the bytes mean and how much space they need.

A file has no built-in type. The name and the extension (`.png`) are labels that people and programs agree to trust. The meaning comes from the format, a documented layout for the bytes. Most formats start with a few fixed bytes that announce what follows.

## Key terms

A **file** is a named sequence of bytes on storage. A **text file** is a file whose bytes are valid in some text encoding. A **binary file** is any other file; the term only means that a text editor cannot show it sensibly.

A **file format** is the documented layout of the bytes: what comes first, what each field means and how long it is.

A **file signature**, or **magic number**, is the fixed byte sequence at the start of a file that identifies its format. A **header** is the block at the start of a file that describes the data after it (width, height, sample rate).

A **pixel** is one dot of an image. In **RGB**, each pixel has three values (red, green, blue), usually one byte each, so 24 bits per pixel. The **resolution** is the number of pixels across and down.

A **sample** is one measurement of a sound wave. The **sample rate** is how many samples there are per second (44,100 for CD audio), and the **bit depth** is how many bits each sample takes (16 for CD audio). A **channel** is one stream of samples; stereo has two.

**Compression** shrinks data. **Lossless** compression (PNG, ZIP, FLAC) can restore every byte. **Lossy** compression (JPEG, MP3) throws away detail people are unlikely to notice, and cannot restore it.

## How it works

Uncompressed data is a header followed by values laid out in order: pixels row by row, or samples one after another. In the diagram, each pixel is 3 bytes and each CD-audio sample is 2 bytes.

```text
image:  header | ff 00 00 | 00 ff 00 | 00 00 ff | ...   3 bytes per pixel (R G B), row by row
                  red        green      blue

sound:  header | 12 34 | 56 78 | 9a bc | ...             2 bytes per sample, 1/44100 s apart
                  s0      s1      s2
```

Sizes are then plain multiplication:

$$\text{image bytes} = \text{width} \times \text{height} \times \text{bytes per pixel}$$

$$\text{sound bytes} = \text{sample rate} \times \text{bytes per sample} \times \text{channels} \times \text{seconds}$$

Real files are smaller when compressed and a little larger for headers. The same signature can sit behind several extensions: a `.zip`, a `.docx`, a `.xlsx` and a `.jar` all start with the ZIP signature, because they are ZIP archives with specific contents.

| Format | First bytes (hex) | As text |
|---|---|---|
| PNG | `89 50 4e 47 0d 0a 1a 0a` | `.PNG....` |
| JPEG | `ff d8 ff` | (not printable) |
| GIF | `47 49 46 38` | `GIF8` |
| PDF | `25 50 44 46 2d` | `%PDF-` |
| ZIP | `50 4b 03 04` | `PK..` |
| gzip | `1f 8b` | (not printable) |
| ELF (Linux program) | `7f 45 4c 46` | `.ELF` |
| WAV | `52 49 46 46`, 4 size bytes, `57 41 56 45` | `RIFF....WAVE` |

These come from the [list of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures). The PNG, JPEG and GIF rows were also checked on files written by ffmpeg, and the gzip row on Python's `gzip` module.

To identify a file, read its first bytes in binary mode and compare. The Linux and macOS command `file name` does the same with a large built-in table. Here are the first 16 bytes of the PNG the lab writes.

```text
89 50 4e 47 0d 0a 1a 0a | 00 00 00 0d | 49 48 44 52 | ...
signature (PNG)         | length: 13  | chunk type: "IHDR" (header), then width, height, ...
```

## Worked examples

<div class="example" markdown>

### Example 1: how big is it before compression

1. A full-HD image is $1920 \times 1080$ pixels with 3 bytes each: $1920 \times 1080 \times 3 = 6{,}220{,}800$ bytes, which is 5.93 MiB. A 40 MB photo is therefore either very high resolution or stored with little compression.
2. One second of CD-quality mono sound is $44{,}100 \times 2 \times 1 \times 1 = 88{,}200$ bytes. A minute is 5,292,000 bytes, about 5 MB.
3. A WAV file adds a 44-byte header, so one second is 88,244 bytes.

<details class="code" markdown>
<summary>In code</summary>

```python
print(1920 * 1080 * 3, 1920 * 1080 * 3 / 2**20)
print(44100 * 2 * 1 * 1, 44100 * 2 * 60, 44100 * 2 + 44)
```

```text
6220800 5.9326171875
88200 5292000 88244
```

</details>

Check: the lab writes a real one-second WAV file, and its size is exactly 88,244 bytes.

</div>

<div class="example" markdown>

### Example 2: a PNG named `photo.jpg`

Rename `red.png` to `photo.jpg`. Programs that trust the extension now treat it as a JPEG, and some will fail to open it. The bytes did not change: the first eight are still `89 50 4e 47 0d 0a 1a 0a`, the PNG signature. A check on the content, not the name, catches the mismatch, and the lab does this.

A signature shows the format, not that the file is safe. A file can start with valid PNG bytes and contain something else after them.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: trusting file extensions or the `Content-Type` that came with an upload. The sender chooses both. Check the signature, and still treat the file as untrusted.

Watch out: opening a binary file in text mode. In Python, `open("a.png")` decodes the bytes as text and can translate line endings, which corrupts the data. Use `open("a.png", "rb")`.

Watch out: expecting a lossy file to survive repeated saving. Each JPEG re-save loses a little more detail. Keep the original, or use a lossless format for edited images.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: file signature, magic bytes, header, binary mode, lossless, lossy, sample rate, bit depth.

Prompts to try:

- "Write a Python function that reads the first 12 bytes of an uploaded file and returns its type for PNG, JPEG, GIF, PDF and ZIP. Say what it cannot tell me about the rest of the file."
- "An uploaded PNG is 6000 by 4000 pixels and 24 MB. Estimate its uncompressed size and say whether 24 MB is plausible."

What to check:

- Signature bytes written from memory. Compare them with the table above or with real files.
- Code that opens files in text mode, or reads a whole upload into memory with no size limit.
- Validation based only on the extension or the declared MIME type.

</div>

## Quiz

1\. How many bytes is an uncompressed 800 by 600 RGB image with one byte per channel?

<details class="solution" markdown>
<summary>Answer</summary>

$800 \times 600 \times 3 = 1{,}440{,}000$ bytes.

</details>

2\. Predict the output: `print(open("photo.jpg", "rb").read(4))` for a PNG that was renamed to `photo.jpg`.

<details class="solution" markdown>
<summary>Answer</summary>

`b'\x89PNG'`. The extension changed; the bytes did not.

</details>

3\. Why does a `.docx` file look like a ZIP archive by its first bytes?

<details class="solution" markdown>
<summary>Answer</summary>

A `.docx` is a ZIP archive that holds XML files, so it starts with `50 4b 03 04`. Telling it from other ZIP-based formats means looking inside the archive.

</details>

4\. Stereo music at 44,100 samples per second and 16 bits per sample lasts 3 minutes. How big is it uncompressed?

<details class="solution" markdown>
<summary>Answer</summary>

$44{,}100 \times 2 \times 2 \times 180 = 31{,}752{,}000$ bytes, about 30 MiB. An MP3 of it is much smaller because MP3 is lossy.

</details>

## Lab

<div class="lab" markdown>

### Lab: build files and identify them by content

Goal: write a PNG and a WAV with the standard library, then identify four files by their first bytes. Time: about 15 minutes. Runs in: any terminal with Python 3.

1. Save the script below as `sniff.py` and run it. It creates a folder `lab6` with a 100 by 100 red PNG named `photo.jpg`, a one-second 440 Hz WAV, a ZIP archive and a text file.
2. Read the output. Which name lies? Compare each size with the formulas in this lesson.
3. Add a path to any image you already have, and run `sniff` on it.
4. Cleanup: delete the `lab6` folder and `sniff.py`.

Expected result: the PNG is found even under a `.jpg` name, and the WAV size is exact (88,244). The PNG and ZIP sizes can differ by a few bytes between Python versions. The text file is 6 bytes because the script writes bytes, so Windows adds no carriage return.

```text
photo.jpg      335 bytes  PNG image
tone.wav     88244 bytes  WAV audio
notes.zip      113 bytes  ZIP archive (also .docx, .xlsx, .jar)
hello.txt        6 bytes  unknown (maybe text)
89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52
```

<details class="solution" markdown>
<summary>Solution</summary>

```python
import math, struct, wave, zipfile, zlib
from pathlib import Path

SIGNATURES = [
    (b"\x89PNG\r\n\x1a\n", "PNG image"),
    (b"\xff\xd8\xff", "JPEG image"),
    (b"GIF8", "GIF image"),
    (b"%PDF-", "PDF document"),
    (b"PK\x03\x04", "ZIP archive (also .docx, .xlsx, .jar)"),
    (b"\x1f\x8b", "gzip data"),
    (b"\x7fELF", "ELF executable"),
    (b"MZ", "Windows executable"),
]

def sniff(path):
    head = Path(path).read_bytes()[:12]
    if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
        return "WAV audio"
    for magic, name in SIGNATURES:
        if head.startswith(magic):
            return name
    return "unknown (maybe text)"

def chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

def write_png(path, width, height, pixel):
    rows = b"".join(b"\x00" + bytes(pixel) * width for _ in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")
    Path(path).write_bytes(png)

def write_wav(path, hz=440, seconds=1, rate=44100):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        samples = (int(20000 * math.sin(2 * math.pi * hz * i / rate)) for i in range(rate * seconds))
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))

Path("lab6").mkdir(exist_ok=True)
write_png("lab6/photo.jpg", 100, 100, (255, 0, 0))
write_wav("lab6/tone.wav")
with zipfile.ZipFile("lab6/notes.zip", "w") as z:
    z.writestr("a.txt", "hello")
Path("lab6/hello.txt").write_bytes(b"hello\n")
for name in ["photo.jpg", "tone.wav", "notes.zip", "hello.txt"]:
    p = Path("lab6") / name
    print(f"{name:10} {p.stat().st_size:>7} bytes  {sniff(p)}")
print(Path("lab6/photo.jpg").read_bytes()[:16].hex(" "))
```

The PNG has a header chunk (`IHDR`: width, height, bit depth 8, colour type 2 for RGB), one compressed data chunk (`IDAT`: each row is a filter byte `00` plus the pixels) and an end chunk (`IEND`), each followed by a checksum. The 30,000 raw pixel bytes compress to a few hundred because every pixel is the same.

</details>

</div>

## Where this shows up

- [File systems](../../02-operating-systems-and-linux/01-os-concepts/04-file-systems.md) store files as bytes plus a name and metadata, and [file formats and columnar storage](../../11-data-engineering-and-data-science/01-data-engineering/08-file-formats-and-columnar-storage.md) covers CSV, JSON and Parquet.
- Upload handling in [injection and input validation](../../12-security/01-web-security/03-injection-and-input-validation.md), and image and audio data sent to AI models.
