### re模块基本使用
```py
import re
    
phoneNumRegex=re.compile(r'(\d\d\d)-(\d\d\d-\d\d\d\d)')
# search返回Matcher对象或None,
matched=phoneNumRegex.search('444-555-6666')
# Matcher的group方法返回匹配的字符,
print(matched.group())
print(matched.group(1))
print(matched.group(2))
# findall 会返回所有分组的元组列表,
print(phoneNumRegex.findall('444-555-6666'))
```

### 基本语法

|语法|功能|
|:----|:----|
|?|0个或1个|
|*|任意个|
|+|至少1个|
|.|除了换行符以外的任意一个字符|
|{n}|重复n次|
|{n,}|至少重复n次|
|{n,m}|重复n-m次|
|{,m}|至多重复m次|
|^start|以start开头|
|end$|以end结尾|
|\\d \\s \\w \\D \\S \\W|数字、空白字符、字符、大写刚好相反|
|[abc]|a或b或c|
|[^abc]|abc之外的任意字符|

