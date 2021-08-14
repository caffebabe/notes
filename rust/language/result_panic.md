## 错误处理

在大部分情形下，Rust会迫使你意识到可能出现错误的地方，并在编译阶段确保它们得到妥善的处理。这些特性使你能够在将代码最终部署到生产环境之前，发现并合理地处理错误，从而使程序更加健壮！

在Rust中，我们将错误分为两大类：可恢复错误与不可恢复错误。对于可恢复错误，比如文件未找到等，一般需要将它们报告给用户并再次尝试进行操作。而不可恢复错误往往就是bug的另一种说法，比如尝试访问超出数组结尾的位置等。

Rust提供了用于可恢复错误的类型 Result&lt;T, E&gt;，以及在程序出现不可恢复错误时中止运行的 panic! 宏。

## 不可恢复错误与panic

Rust提供了一个特殊的 panic! 宏。程序会在 panic! 宏执行时打印出一段错误提示信息，展开并清理当前的调用栈，然后退出程序。

查看回溯栈：

```shell
# powershell
$env:RUST_BACKTRACE=1 ; cargo run
# linux shell
RUST_BACKTRACE=1 cargo run
```

## 可恢复错误与Result

大部分的错误其实都没有严重到需要整个程序停止运行的地步。函数常常会由于一些可以简单解释并做出响应的原因而运行失败。例如，尝试打开文件的操作会因为文件不存在而失败。你也许会在这种情形下考虑创建该文件而不是终止进程。

## Result定义

```rs
enum Result<T, E> {
   Ok(T),
   Err(E),
}
```

匹配不同的错误：

```rs
use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let f = File::open("hello.txt");

    let f = match f {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,
                Err(e) => panic!("Problem creating the file: {:?}", e),
            },
            other_error => {
                panic!("Problem opening the file: {:?}", other_error)
            }
        },
    };
}
```

Result内部通过match封装了一系列接收闭包的方法，更优雅的处理结果：

```rs
use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let f = File::open("hello.txt").unwrap_or_else(|error| {
        if error.kind() == ErrorKind::NotFound {
            File::create("hello.txt").unwrap_or_else(|error| {
                panic!("Problem creating the file: {:?}", error);
            })
        } else {
            panic!("Problem opening the file: {:?}", error);
        }
    });
}
```

失败时触发panic！的简写方式：

```rs
use std::fs::File;

fn main() {
    let f = File::open("hello.txt").unwrap();
}
```

```rs
use std::fs::File;

fn main() {
    let f = File::open("hello.txt").expect("Failed to open hello.txt");
}
```

### 传播错误（propagating）

我们没有足够的上下文信息去知晓调用者会如何处理返回值，所以我们将成功信息和错误信息都向上传播，让调用者自行决定自己的处理方式。

使用？操作符向上传播错误：

```rs
#![allow(unused)]
fn main() {
    use std::fs::File;
    use std::io;
    use std::io::Read;

    fn read_username_from_file() -> Result<String, io::Error> {
        let mut f = File::open("hello.txt")?;
        let mut s = String::new();
        f.read_to_string(&mut s)?;
        Ok(s)
    }
}
```

还可以在链式调用中使用？操作符：

```rs
#![allow(unused)]
fn main() {
    use std::fs::File;
    use std::io;
    use std::io::Read;

    fn read_username_from_file() -> Result<String, io::Error> {
        let mut s = String::new();

        File::open("hello.txt")?.read_to_string(&mut s)?;

        Ok(s)
    }
}
```
