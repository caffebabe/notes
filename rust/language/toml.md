## TOML

>Tom's Obvious Minimal Language  
A config file format for humans.

支持的数据类型：

- Key/Value Pairs
- Arrays
- Tables
- Inline tables
- Arrays of tables
- Integers & Floats
- Booleans
- Dates & Times, with optional offsets

## 速览

注释：

```toml
# This is a TOML comment

# This is a multiline
# TOML comment
```

数值：

```toml
# 整型
int1 = +99
int2 = 42
int3 = 0
int4 = -17

# 16进制
hex1 = 0xDEADBEEF
hex2 = 0xdeadbeef
hex3 = 0xdead_beef

# 8进制
oct1 = 0o01234567
oct2 = 0o755

# 二进制
bin1 = 0b11010110

# 小数
float1 = +1.0
float2 = 3.1415
float3 = -0.01

# 科学计数
float4 = 5e+22
float5 = 1e06
float6 = -2E-2

# both
float7 = 6.626e-34

# 千位分割符
float8 = 224_617.445_991_228

# 无穷
infinite1 = inf # positive infinity
infinite2 = +inf # positive infinity
infinite3 = -inf # negative infinity

# NaN
not1 = nan
not2 = +nan
not3 = -nan 
```

字符串：

```toml
# Basic strings 
str1 = "I'm a string."
str2 = "You can \"quote\" me."
str3 = "Name\tJos\u00E9\nLoc\tSF."

# Multi-line basic strings
str1 = """
Roses are red
Violets are blue"""

# The quick brown fox jumps over the lazy dog.
str2 = """\
  The quick brown \
  fox jumps over \
  the lazy dog.\
  """
# Literal strings
path = 'C:\Users\nodejs\templates'
path2 = '\\User\admin$\system32'
quoted = 'Tom "Dubs" Preston-Werner'
regex = '<\i\c*\s*>'

# multi-line literal strings
re = '''\d{2} apps is t[wo]o many'''
lines = '''
The first newline is
trimmed in raw strings.
All other whitespace
is preserved.
'''

```
