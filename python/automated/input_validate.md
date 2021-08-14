### 基本input校验
不断循环提示，直到校验成功！
```python
while True:
    print("Enter your age:")
    age = input()
    try:
        age = int(age)
    except (Exception):
        print("Please use numeric digits.")
        continue
    if age < 1:
        print("Please enter a positive number.")
        continue
    break
print(f"Your age is {age}.")

```

### 使用PyInputPlus模块
基本方法：
- inputStr() 
- inputNum()
- inputChoice()
- inputMenu() 
- inputDatetime() 
- inputYesNo() 
- inputBool() 
- inputEmail() 
- inputFilepath() 
- inputPassword() 
- inputCustom()

```python
import pyinputplus as pyip
from pathlib import Path

help(pyip.inputFilepath)
filePath = pyip.inputFilepath(
    prompt="Enter the path(current work dir): ", blank=True, default=Path.cwd
)
age = pyip.inputInt(prompt="Enter your age: ", min=18, max=100)
password = pyip.inputPassword(prompt="Enter your Password: ", limit=3)
str = pyip.inputStr(allowRegexes=[r"caterpillar", "category"], blockRegexes=[r"cat"])

```
自定义,输入字符加起来等于10：
```python
import pyinputplus as pyip


def addsUpToTen(numbers):
    numList = list(numbers)
    for i, digit in enumerate(numList):
        numList[i] = int(digit)
    if sum(numList) != 10:
        raise Exception("The digits must add up to 10, not %s." % (sum(numList)))
    return int(numbers)  # Return an int form of numbers.


response = pyip.inputCustom(addsUpToTen, "Enter nums add up to ten:")

```