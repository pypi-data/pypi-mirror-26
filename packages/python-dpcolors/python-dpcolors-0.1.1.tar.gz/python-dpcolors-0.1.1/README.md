# python-dpcolors

[![Build Status](https://travis-ci.org/nsavch/python-dpcolors.svg?branch=master)](https://travis-ci.org/nsavch/python-dpcolors)

Python library for converting DarkPlaces color strings to various other formats

Supports the following conversions

 * dp -> irc
 * dp -> ansi 8 bit
 * dp -> ansi 24 bit
 * irc -> dp
 * irc -> ansi 8 bit
 * irc -> ansi 24 bit

# Installation

```bash
pip install python-dpcolors
```

# Example usage

```python
from dpcolors import ColorString

cs = ColorString.from_dp('^3hello')
print(cs.to_irc())
print(cs.to_ansi_8bit())
print(cs.to_ansi_24bit())

cs = ColorString.from_irc('\x0305hello')
print(cs.to_dp())
```
