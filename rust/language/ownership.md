## 所有权（Ownership）

Rust 没有GC，也不用手动管理内存，而是采用了另一种方式进行内存管理：所有权规则：

1. 每个值都有一个变量作为它的所有者（owner）
2. 一次只能有一个所有者
3. 一旦所有者变量超出作用域，值就会被销毁（dropped）

例1：下面代码无法编译通过

```rs
let x=5;
let z=y=x;
```

### 移动

例2：下面代码无法编译通过

```rs
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;
    println!("{}, world!", s1);
    println!("{}, world!", s2);
}

// borrow of moved value：`s1`

// move occurs because `s1` has type `std::string::String`, 
// which does not implement the `Copy` trait
```

为了确保内存安全，同时也避免复制分配的内存，Rust在这种场景下会简单地将s1废弃，不再视其为一个有效的变量。这种方式有个术语叫做 “move”。

### 克隆

例3：下面代码可以通过编译：

```rs
fn main() {
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("{}, world!", s1);
    println!("{}, world!", s2);
}
```

### 复制（Copy）

例4：下面代码可以编译通过

```rs
fn main() {
    let x = 1;
    let y = x;
    println!("x = {}, y = {}", x, y);
}
```

Rust提供了一个名为 Copy 的 trait。一旦某种类型拥有了 Copy 这种trait，那么它的变量就可以在赋值给其他变量之后保持可用性。

如果一种类型本身或这种类型的任意成员实现了 Drop 这种 trait，那么Rust就不允许其实现 Copy 这种 trait。

所有的标量类型以及元组都实现了这一trait。

## 引用与借用

引用不持有所有权。通过引用传递参数给函数的方法称为借用（borrowing）。例如：

```rs
fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);
    println!("The length of '{}' is {}.", s1, len);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}
```

引用是默认不可变的，不能修改引用指向的值：

```rs
fn main() {
    let s = String::from("hello");
    change(&s);
}

fn change(some_string: &String) {
    some_string.push_str(", world");
}

//`some_string` is a `&` reference, 
// so the data it refers to cannot be borrowed as mutable
```

如果要修改引用指向的值，就要使用可变引用。只能同时拥有一个可变引用，但可以有多个不可变引用。

```rs
fn main() {
    let mut s = String::from("hello");
    change(&mut s);
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

### 切片

切片也不持有所有权。一个字符串切片示例：

```rs
fn main() {
    let s = String::from("hello world");
    let hello = &s[0..5];
    let another_hello=&s[..5];
    let world = &s[6..11];
    let another_word=&s[6..];
    let hello_world=&s[..];

    println!("{}",hello);
    println!("{}",another_hello);
    println!("{}",world);
    println!("{}",another_word);
    println!("{}",hello_world);
}
```

字符串切片作为函数参数：

```rs
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}

fn main() {
    let my_string = String::from("hello world");

    // first_word works on slices of `String`s
    let word = first_word(&my_string[..]);

    let my_string_literal = "hello world";

    // first_word works on slices of string literals
    let word = first_word(&my_string_literal[..]);

    // Because string literals *are* string slices already,
    // this works too, without the slice syntax!
    let word = first_word(my_string_literal);
}
```
