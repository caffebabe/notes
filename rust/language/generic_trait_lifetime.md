## Trait

Trait 类似于 Java 中的接口，用于定义实现某些目标的行为(即方法)集合。

trait Summary 定义了 summarize 行为，用于生成摘要信息：

```rs
pub trait Summary {
    fn summarize(&self) -> String;
}
```

实现 Summary：

```rs
pub trait Summary {
    fn summarize(&self) -> String;
}

pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct Tweet {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}

fn main() {
    let tweet = Tweet {
        username: String::from("horse_ebooks"),
        content: String::from("of course, as you probably already know, people"),
        reply: false,
        retweet: false,
    };

    println!("1 new tweet: {}", tweet.summarize());
}
```

### 默认实现

```rs
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
```

### Trait Bound Syntax

trait实现时的 impl Summary 只是语法糖，其真正的语法应该是：

```rs
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

impl Summary 形式的语法更简洁，但它隐含了一个限制：对象的类型必须相同。如果允许不同的对象，就需要使用 Trait Bound Syntax

```rs
// item1 和 item2 必须是同一类型
pub fn notify(item1: &impl Summary, item2: &impl Summary) {

// item1 和 item2 可以是不同类型
pub fn notify<T: Summary>(item1: &T, item2: &T) {

```

### 多实现

```rs
pub fn notify(item: &(impl Summary + Display)) {

pub fn notify<T: Summary + Display>(item: &T) {
```

### where 条件

```rs
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {

fn some_function<T, U>(t: &T, u: &U) -> i32
    where T: Display + Clone,
          U: Clone + Debug
{
```

### 返回 trait

```rs
fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        retweet: false,
    }
}
```

### 选择性实现

```rs
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
}

impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("The largest member is x = {}", self.x);
        } else {
            println!("The largest member is y = {}", self.y);
        }
    }
}
```

```rs
impl<T: Display> ToString for T {
    // --snip--
}
```

## Generic Data Types

```rs
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];

    for &item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest(&number_list);
    println!("The largest number is {}", result);

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest(&char_list);
    println!("The largest char is {}", result);
}
```

### 用于 struct

```rs
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let integer = Point { x: 5, y: 10 };
    let float = Point { x: 1.0, y: 4.0 };
}
```

### 用于枚举

```rs
enum Option<T> {
    Some(T),
    None,
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

### 用于方法

```rs
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

方法中的泛型参数不一定要和结构体中的泛型参数一致：

```rs
struct Point<T, U> {
    x: T,
    y: U,
}

impl<T, U> Point<T, U> {
    fn mixup<V, W>(self, other: Point<V, W>) -> Point<T, W> {
        Point {
            x: self.x,
            y: other.y,
        }
    }
}
```

### 泛型的开销

Rust会在编译时执行泛型代码的单态化（monomorphization），在编译期将所有使用过的具体类型填入泛型参数从而得到有具体类型的代码。

例如，对于 Option&lt;T&gt; 的使用：

```rs
let integer = Some(5);
let float = Some(5.0);
```

编译后的结果为：

```rs
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

## Lifetime

Rust 中的引用都是有效的。当引用的生命周期可能以不同的方式相互关联时，我们就必须手动标注生命周期，来确保运行时实际使用的引用一定是有效的。

Rust 编译器使用借用检查器（borrow checker）比较不同的作用域并确定所有借用的合法性。

```rs
fn main() {
    {
        let r;
        {
            let x = 5;
            r = &x;//borrowed value does not live long enough
        }
        println!("r: {}", r);
    }
}
```

### 生命周期标注语法

下面代码编译不通过：

```rs
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
//missing lifetime specifier
//expected named lifetime parameter

//help: this function's return type contains a borrowed value, 
//but the signature does not say whether it is borrowed from `x` or `y`
```

生命周期的标注并不会改变任何引用的生命周期，只是用来描述多个引用生命周期之间的关系。

对于上面的例子，一种可行的修改方式是：告诉编译器，所有参数和返回值的引用都必须拥有相同的生命周期。

```rs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

当我们将具体的引用传入 longest 时，被用于替代'a的具体生命周期就是作用域x与作用域y重叠的那一部分。因为我们将返回的引用也标记为了生命周期参数'a，所以返回的引用在具化后的生命周期范围内都是有效的。

### 结构体定义中的生命周期标注

下面的生命周期标注表明：ImportantExcerpt 实例的生命周期不能超过 part 字段引用的生命周期

```rs
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn main() {

    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().expect("Could not find a '.'");
    let i = ImportantExcerpt {
        part: first_sentence,
    };
    println!("{}",i.part);
}
```

### 生命周期省略规则

没有显示标注生命周期时，编译器会使用生命周期省略规则：

1. 每一个引用参数都会拥有自己的生命周期参数。
2. 当只存在一个输入生命周期参数时，这个生命周期会被赋予给所有输出生命周期参数。
3. 当拥有多个输入生命周期参数，而其中一个是 &self 或 &mut self 时，self 的生命周期会被赋予给所有的输出生命周期参数。

例如：

```rs
fn first_word(s: &str) -> &str {

//使用规则一之后：
fn first_word<'a>(s: &'a str) -> &str {

//使用规则二之后：
fn first_word<'a>(s: &'a str) -> &'a str {

//没有多个输入参数，所以不需要规则三，最终结果就是返回值和输入参数有相同的生命周期，可以编译通过
```

再如：

```rs
fn longest(x: &str, y: &str) -> &str {

//使用规则一之后：
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {

//编译器无法使用规则二，所以编译不通过
```

### 方法定义中的生命周期标注

```rs
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
}

impl<'a> ImportantExcerpt<'a> {
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention please: {}", announcement);
        self.part
    }
}
```

### 静态生命周期

静态生命周期在程序运行期间都有效，字符串字面量的生命周期就是静态的。

```rs
#![allow(unused)]
fn main() {
    let s: &'static str = "I have a static lifetime.";
}
```
