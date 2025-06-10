# Problem (unicode1): Understanding Unicode (1 point)

## What Unicode character does chr(0) return?

The `chr(0)` function returns the Unicode character with code point 0, which is the **null character** (often represented as `'\0'`). It is a control character used to signify the end of a string in many programming languages and systems. In Unicode, it is referred to as "NULL" and has no visual representation.

## How does this character’s string representation (__repr__()) differ from its printed representa-
tion?

The string representation of a character using __repr__() provides a detailed and unambiguous representation of the object, often including escape sequences for non-printable characters. For the null character (chr(0)), __repr__() would return '\x00', showing its hexadecimal escape code.

In contrast, the printed representation (print()) attempts to display the character as-is. Since the null character has no visual representation, printing it results in no visible output.