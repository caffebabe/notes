# Rust介绍

- [Rust官网](https://www.rust-lang.org/)
- [Rust中文社区](https://rustcc.cn/)
- [一篇爽文，看了就想学Rust了](https://mp.weixin.qq.com/s/9rjeVgVzmrC0wWhV4wA9FA)

## 开发环境

### 安装Rust

参考官方网站，使用rustup安装。安装过程中如提示没有VC++环境，按提示去vs官方下载并安装，成功后继续运行rustup-init.exe。

### VS Code 支持

安装Rust插件

### 设置代理

字节跳动维护的Crate.io镜像和Rustup 镜像：<https://rsproxy.cn/>

~/.cargo/config:

```toml
[source.crates-io]
replace-with = 'rsproxy'

[source.rsproxy]
registry = "https://rsproxy.cn/crates.io-index"
```

~/.zshrc or ~/.bashrc：

```toml
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
```

## 第一个Rust程序

### 创建项目guessing_game

```shell
cargo new guessing_game
```

### 使用vscode打开 guessing_game

由于第一次使用rust，vscode会提示安装一些rust工具，那就安装吧。最终的项目结构如下：

```txt
guessing_game       --项目目录
  src               源代码目录
    main.rs
  target            构建结果
    rls
    CACHEDIR.TAG
  Cargo.toml        Cargo项目配置文件
  Cargo.lock        
  .gitignore
```

cargo 添加 rand 依赖：

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2018"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
rand = "0.8.4"
```

写代码了：

```rust
use rand::Rng;
use std::cmp::Ordering;
use std::io;

fn main() {
    println!("Guess the number!");
    let secret_number = rand::thread_rng().gen_range(1..100);
    loop {
        println!("Please input your guess.");
        let mut guess = String::new();
        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {}", guess);

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

## 初体验

1. 工具链很强大
2. main 函数没有参数
3. 变量默认不可变
4. match 表达式与枚举
5. 异常处理的艺术
6. 宏
7. 表达式与语句的区别（表达式有返回值）
8. 语句分号结束，go不要分号

## TODO

1. vs code rust 不太方便。继续摸索，达到 idea 写 java 那般丝滑就完美
2. 继续学习rust基本语法
