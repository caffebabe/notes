## 闭包（Closures）

Rust中的闭包是一种可以存入变量或作为参数传递给其他函数的匿名函数。

和一般的函数不同，闭包可以从定义它的作用域中捕获值。

运用闭包的特性可以实现代码复用和行为自定义。

使用闭包存储代码来进行重构：

```rs
use std::thread;
use std::time::Duration;

fn generate_workout(intensity: u32, random_number: u32) {
    let expensive_closure = |num| {
        println!("calculating slowly...");
        thread::sleep(Duration::from_secs(2));
        num
    };

    if intensity < 25 {
        println!("Today, do {} pushups!", expensive_closure(intensity));
        println!("Next, do {} situps!", expensive_closure(intensity));
    } else {
        if random_number == 3 {
            println!("Take a break today! Remember to stay hydrated!");
        } else {
            println!("Today, run for {} minutes!", expensive_closure(intensity));
        }
    }
}

fn main() {
    let simulated_user_specified_value = 10;
    let simulated_random_number = 7;

    generate_workout(simulated_user_specified_value, simulated_random_number);
}
```

### 类型推断（Closure Type Inference）

编译器能够可靠地推断出闭包参数的类型及返回值的类型。但不能使用两种不同的类型调用同一个需要类型推导的闭包。

```rs
fn main() {
    let example_closure = |x| x;

    let s = example_closure(String::from("hello"));
    let n = example_closure(5);
}

//mismatched types
//expected struct `std::string::String`, found integer
```

### 存储闭包

创建一个同时存放闭包及闭包返回值的结构体。这个结构体只会在我们需要获得结果值时运行闭包，并将首次运行闭包时的结果缓存起来，这样余下的代码就不必再负责存储结果，
而可以直接复用该结果。这种模式一般被称作 记忆化（memoization）或 惰性求值（lazy evaluation）。

```rs
use std::thread;
use std::time::Duration;

struct Cacher<T>
where
    T: Fn(u32) -> u32,
{
    calculation: T,
    value: Option<u32>,
}

impl<T> Cacher<T>
where
    T: Fn(u32) -> u32,
{
    fn new(calculation: T) -> Cacher<T> {
        Cacher {
            calculation,
            value: None,
        }
    }

    fn value(&mut self, arg: u32) -> u32 {
        match self.value {
            Some(v) => v,
            None => {
                let v = (self.calculation)(arg);
                self.value = Some(v);
                v
            }
        }
    }
}

fn generate_workout(intensity: u32, random_number: u32) {
    let mut expensive_result = Cacher::new(|num| {
        println!("calculating slowly...");
        thread::sleep(Duration::from_secs(2));
        num
    });

    if intensity < 25 {
        println!("Today, do {} pushups!", expensive_result.value(intensity));
        println!("Next, do {} situps!", expensive_result.value(intensity));
    } else {
        if random_number == 3 {
            println!("Take a break today! Remember to stay hydrated!");
        } else {
            println!(
                "Today, run for {} minutes!",
                expensive_result.value(intensity)
            );
        }
    }
}

fn main() {
    let simulated_user_specified_value = 10;
    let simulated_random_number = 7;

    generate_workout(simulated_user_specified_value, simulated_random_number);
}
```

### 捕获上下文

闭包可以捕获作用域下的上下文：

```rs
fn main() {
    let x = 4;
    let equal_to_x = |z| z == x;
    let y = 4;
    assert!(equal_to_x(y));
}
```

闭包可以通过3种方式从它们的环境中捕获值，这和函数接收参数的3种方式是完全一致的：获取所有权、可变借用及不可变借用。

这3种方式被分别编码在3种 Fn 系列的 trait中：

- FnOnce 意味着闭包可以从它的封闭作用域中，消耗捕获的变量。为了实现这一功能，闭包必须在定义时取得这些变量的所有权并将它们移动至闭包中。
- FnMut 可以从环境中可变地借用值并对它们进行修改。
- Fn 可以从环境中不可变地借用值。

所有闭包都自动实现了FnOnce，因为它们至少都可以被调用一次。

假如你希望强制闭包获取环境中值的所有权，那么你可以在参数列表前添加 ***move*** 关键字。这个特性在把闭包传入新线程时相当有用，它可以将捕获的变量一并移动到新线程中去。

### 迭代器（Iterators）

迭代器模式允许你依次为序列中的每一个元素执行某些任务。迭代器会在这个过程中负责遍历每一个元素并决定序列何时结束。

在Rust中，迭代器是惰性的（layzy）。这也就意味着创建迭代器后，除非你主动调用方法来消耗并使用迭代器，否则它们不会产生任何的实际效果。

```rs
fn main() {
    let v1 = vec![1, 2, 3];
    let v1_iter = v1.iter();
    for val in v1_iter {
        println!("Got: {}", val);
    }
}
```

### Iterator trait

```rs
#[must_use = "iterators are lazy and do nothing unless consumed"]
pub trait Iterator {
    type Item;
    
    fn next(&mut self) -> Option<Self::Item>;
}
```

注意，这个定义使用了两种新语法：type Item 和 Self::Item，它们定义了 trait 的关联类型（associated type）。

为了实现 Iterator trait，我们必须要定义一个具体的Item类型，而这个Item类型会被用作next方法的返回值类型。

Iterator trait 只要求实现者手动定义一个方法：next 方法，它会在每次被调用时返回一个包裹在 Some 中的迭代器元素，并在迭代结束时返回 None。

```rs
#[cfg(test)]
mod tests {
    #[test]
    fn iterator_demonstration() {
        let v1 = vec![1, 2, 3];

        let mut v1_iter = v1.iter();

        assert_eq!(v1_iter.next(), Some(&1));
        assert_eq!(v1_iter.next(), Some(&2));
        assert_eq!(v1_iter.next(), Some(&3));
        assert_eq!(v1_iter.next(), None);
    }
}
fn main(){}
```

注意：v1_iter 必须是可变的，因为调用 next() 方法改变了迭代器内部用来记录序列位置的状态。

动态数组提供三种方法来生成不同的迭代器：

- iter()： 生成不可变引用的迭代器，通过 next() 取得的值实际上是指向动态数组中各个元素的不可变引用。
- into_iter()：生成取得所有权的迭代器。
- iter_mut（）：生成可变引用的迭代器。

### 消耗迭代器的方法（consuming adaptor）

标准库为Iterator trait 提供了多种包含默认实现的方法，这些方法中的一部分会在它们的定义中调用 next 方法。

这些调用 next 的方法也被称为消耗适配器（consuming adaptor），因为它们同样消耗了迭代器本身。例如 collect 方法会消耗迭代器并将结果值收集到某种集合数据类型中。

### 生成其他迭代器的方法（iterator adaptor）

Iterator trait 还定义了另外一些被称为迭代器适配器（iterator adaptor）的方法，这些方法可以使你将已有的迭代器转换成其他不同类型的迭代器。

你可以链式地调用多个迭代器适配器完成一些复杂的操作，同时保持代码易于阅读。但因为所有的迭代器都是惰性的，所以你必须调用一个消耗适配器的方法才能从迭代器适配器中获得结果。

```rs
fn main() {
    let v1: Vec<i32> = vec![1, 2, 3];
    let v2: Vec<_> = v1.iter().map(|x| x + 1).collect();
    assert_eq!(v2, vec![2, 3, 4]);
}
```

### 实现 Iterator trait

```rs
struct Counter {
    count: u32,
}

impl Counter {
    fn new() -> Counter {
        Counter { count: 0 }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < 5 {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn calling_next_directly() {
        let mut counter = Counter::new();

        assert_eq!(counter.next(), Some(1));
        assert_eq!(counter.next(), Some(2));
        assert_eq!(counter.next(), Some(3));
        assert_eq!(counter.next(), Some(4));
        assert_eq!(counter.next(), Some(5));
        assert_eq!(counter.next(), None);
    }
    #[test]
    fn using_other_iterator_trait_methods() {
        let sum: u32 = Counter::new()
            .zip(Counter::new().skip(1))
            .map(|(a, b)| a * b)
            .filter(|x| x % 3 == 0)
            .sum();
        assert_eq!(18, sum);
    }
}

fn main() {}
```
