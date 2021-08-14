### 文件读写

```python
import os

helloFilepath = os.path.join(os.getcwd(), "hello.txt")

helloFile = open(helloFilepath, "w")
helloFile.writelines("Hello,world!\n")
helloFile.close()

helloFile = open(helloFilepath)
helloContent = helloFile.readlines()
print(helloContent)
helloFile.close()

helloFile = open(helloFilepath, "a")
helloFile.writelines("Hello again,world!\n")
helloFile.close()

helloFile = open(helloFilepath)
helloContent = helloFile.readlines()
print(helloContent)
helloFile.close()

```
### 持久化
```python
import shelve

catShelf = shelve.open("cat_data")
cats = ["Zophie", "Pooka", "Simon"]
catShelf["cats"] = cats
catShelf.close()

catShelf = shelve.open("cat_data")
cats = catShelf["cats"]
print(cats)

```
### shuit(shell utilities)

### zipfile