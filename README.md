# Encoding Identifier
This program identifies likely encodings which a text string represents. The tested-for encodings are:

- Binary
- Hex
- Octal
- Base64
- Base32
- Base45
- Base58
- Base62
- ROT13
- ROT47

It not only checks whether the text strings technically can be decoded as the above formats, but in many cases whether they are likely to be (such as using frequency analysis on ROT13 and ROT47).
