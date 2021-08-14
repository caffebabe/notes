## 结构体定义和初始化

### 定义结构体

```rs
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}
```

### 实例化

```rs
fn main() {
    let user1 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };

    let username=user1.username;

    println!("{}", username);
}
```

字段初始化简写(field init shorthand syntax)：

```rs
fn build_user(email: String, username: String) -> User {
    User {
        email,
        username,
        active: true,
        sign_in_count: 1,
    }
}
```

结构体更新语法（Struct Update Syntax）：

```rs
fn main() {
    let user1 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };

    let user2 = User {
        email: String::from("another@example.com"),
        username: String::from("anotherusername567"),
        ..user1
    };
}
```

### 空结构体

Rust允许我们创建没有任何字段的结构体！当你想要在某些类型上实现一个trait，却不需要在该类型中存储任何数据时，空结构体就可以发挥相应的作用。

## 方法

方法与函数依然是两个不同的概念，方法定义在某个结构体的上下文中，并且第一个参数永远都是self，用于指代调用该方法的结构体实例。

```rs
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!(
        "The area of the rectangle is {} square pixels.",
        rect1.area()
    );
}
```

### 关联函数(Associated Functions)

impl块还可以定义不接收self作为参数的函数。由于这类函数与结构体相互关联，所以称为关联函数（associatedfunction）。关联函数不会作用于某个具体的结构体实例，所以称为函数而不是方法。关联函数常用于构造器来返回一个结构体的新实例。

```rs
impl Rectangle {
    fn square(size: u32) -> Rectangle {
        Rectangle {
            width: size,
            height: size,
        }
    }
}
```
