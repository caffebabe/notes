## Vec

Vec 是动态数组，内存连续，大小可变。

### 创建 Vec

```rs
let v: Vec<i32> = Vec::new();
let v = vec![1,2,3];
```

### 更新 Vec

```rs
fn main() {
    let mut v= vec![1,2,3];
    v.push(4);
    v.insert(0, 0);
    assert_eq!(v.pop(), Some(4));
}
```

### 读取 Vec

```rs
&v[0] 返回位置0上的元素的引用，若不存在会触发panic
v.get(0) 返回Option<&I>
```

一旦程序获得了一个有效的引用，借用检查器就会执行所有权规则和借用规则，来保证这个引用及其他任何指向这个动态数组的引用始终有效。

下面代码编译不通过：

```rs
fn main() {
    let mut v = vec![1, 2, 3, 4, 5];
    let first = &v[0]; //不可变借用
    v.push(6); //可变借用
    println!("The first element is: {}", first);//再次使用不可变借用
}

//cannot borrow `v` as mutable because it is also borrowed as immutable
```

为什么对第一个元素的引用需要关心动态数组结尾处的变化呢？此处的错误是由动态数组的工作原理导致的：动态数组中的元素是连续存储的，插入新的元素后也许会没有足够多的空间将所有元素依次相邻地放下，这就需要分配新的内存空间，并将旧的元素移动到新的空间上。第一个元素的引用可能会因为插入行为而指向被释放的内存。借用规则可以帮助我们规避这类问题。

### 遍历 Vec

只读遍历：

```rs
fn main() {
    let v = vec![100, 32, 57];
    for i in &v {
        println!("{}", i);
    }
}
```

可变遍历：

```rs
fn main() {
    let mut v = vec![100, 32, 57];
    for i in &mut v {
        *i+=1; //这里使用了 解引用操作符
        println!("{}", *i);
    }
}
```

## String

> The String type is a growable, mutable, owned, UTF-8 encoded string type.

### 创建 String

```rs
let mut s = String::new();
let s = String::from("initial contents");
```

### 更新 String：push_str and push

```rs
fn main() {
    let mut s = String::from("foo");
    s.push_str("bar");
    s.push('l');
}
```

### 拼接 String：+ 操作符

```rs
fn main() {
    let s1 = String::from("Hello, ");
    let s2 = String::from("world!");
    let s3 = s1 + &s2; 
    
    println!("{}",s3);
    println!("{}",s1);//borrow of moved value: `s1`
}
```

“+” 操作符会取得所有权，其本质是：

```rs
fn add(self, s: &str) -> String 
```

String 没有实现 Copy，add函数取得s1的所有权并返回给了s3，所以s1被移动了。

add函数第二个参数接收一个字符串切片，不需要所有权，所以s2没有移动。

这里将 &String 传给 &str，实际rust使用了解引用强制转换（deref coercion）。

format! 会将结果包含在一个String中返回。这段使用format! 的代码要更加易读，并且不会夺取任何参数的所有权。

### 拼接 String：format! 宏

```rs
fn main() {
    let s1 = String::from("tic");
    let s2 = String::from("tac");
    let s3 = String::from("toe");

    let s = format!("{}-{}-{}", s1, s2, s3);
}
```

### Rust中String不支持索引

下面代码无法编译通过：

```rs
fn main() {
    let s1 = String::from("hello");
    let h = s1[0];
}
```

为什么Rust不允许使用字符串索引：

1. 字符串是Unicode字符串，按索引访问可能会返回一个无效的字符，所以Rust直接不允许按索引访问字符串
2. 按索引访问字符串

### 字符串切片

如果要使用索引来创建字符串切片，必须通过索引范围来明确指定所需的字节内容。

```rs

#![allow(unused)]
fn main() {
let hello = "Здравствуйте";

let s = &hello[0..4];//前4个字节的内容正好是“Зд”
println!("{}",s);
}
```

### 遍历字符串

得到每一个Unicode标量值：

```rs
#![allow(unused)]
fn main() {
    for c in "नमस्ते".chars() {
        println!("{}", c);
    }
}
```

得到每一个字节：

```rs
#![allow(unused)]
fn main() {
    for b in "नमस्ते".bytes() {
        println!("{}", b);
    }
}
```

## HashMap

### 创建 Hash Map

```rs
fn main() {
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
}
```

两一种方法：一直key集合和value集合

```rs
fn main() {
    use std::collections::HashMap;

    let teams = vec![String::from("Blue"), String::from("Yellow")];
    let initial_scores = vec![10, 50];

    let mut scores: HashMap<_, _> = teams.into_iter().zip(initial_scores.into_iter()).collect();

    let timber_resources: HashMap<&str, i32> = 
    [("Norway", 100), ("Denmark", 50), ("Iceland", 10)]
    .iter().cloned().collect();
}
```

### 哈希映射与所有权

对于那些实现了Copy trait的类型，例如i32，它们的值会被简单地复制到哈希映射中。而对于String这种持有所有权的值，其值将会转移且所有权会转移给哈希映射。

### get方法

```rs
fn main() {
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    let team_name = String::from("Blue");
    let score = scores.get(&team_name);
}
```

### 遍历方法

```rs
fn main() {
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    for (key, value) in &scores {
        println!("{}: {}", key, value);
    }
}
```

### 更新方法

- insert：覆盖旧值
- Entry.or_insert：不存在才插入
- 基于旧值更新

```rs
fn main() {
    use std::collections::HashMap;

    let text = "hello world wonderful world";

    let mut map = HashMap::new();

    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1;
    }

    println!("{:?}", map);
}
```
