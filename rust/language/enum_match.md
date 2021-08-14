## 枚举

```rs
enum IpAddrKind {
    V4,
    V6,
}

fn main() {
    let four = IpAddrKind::V4;
    let six = IpAddrKind::V6;

    route(IpAddrKind::V4);
    route(IpAddrKind::V6);
}

fn route(ip_kind: IpAddrKind) {}

```

可以直接将其关联的数据嵌入枚举变体内:

```rs
fn main() {
    enum IpAddr {
        V4(String),
        V6(String),
    }

    let home = IpAddr::V4(String::from("127.0.0.1"));

    let loopback = IpAddr::V6(String::from("::1"));
}
```

并且每个变体可以拥有不同类型和数量的关联数据。

```rs
fn main() {
    enum IpAddr {
        V4(u8, u8, u8, u8),
        V6(String),
    }

    let home = IpAddr::V4(127, 0, 0, 1);

    let loopback = IpAddr::V6(String::from("::1"));
}
```

## Option枚举与空值处理

Option的定义：

```rs
pub enum Option<T> {
    None,
    Some(T),
}
```

### Option空值处理的好处

在编写代码的过程中，不必再去考虑一个值是否为空可以极大地增强我们对自己代码的信心。为了持有一个可能为空的值，我们总是需要将它显式地放入对应类型的Option&lt;T&gt;值中。当我们随后使用这个值的时候，也必须显式地处理它可能为空的情况。无论在什么地方，只要一个值的类型不是Option&lt;T&gt;的，我们就可以安全地假设这个值不是非空的。这是Rust为了限制空值泛滥以增加Rust代码安全性而做出的一个有意为之的设计决策。

## match

```rs
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}
```

匹配必须穷举所有的可能.

_通配符
