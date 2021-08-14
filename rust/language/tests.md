## 测试函数的构成

测试函数最简单的形式是给一个函数加上 test 属性。

我们可以使用cargo test命令来运行测试。这个命令会构建并执行一个用于测试的可执行文件，该文件在执行的过程中会逐一调用所有标注了 test 属性的函数，并生成统计测试运行成功或失败的相关报告。

使用 cargo new tests --lib 生成的模板代码如下：

```rs
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
```

在Rust中，一旦测试函数触发panic，该测试就被视作执行失败。每个测试在运行时都处于独立的线程中，主线程在监视测试线程时，一旦发现测试线程意外终止，就会将对应的测试标记为失败。

```rs
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    fn another() {
        panic!("Make this test fail");
    }
}
```

## 常用的检查工具

- assert!：断言某个值为true
- assert_eq!：断言两个值相等
- assert_ne!：断言两个值不相等
- #[should_panic]：断言会触发panic
- 返回Result<T,E>

## 控制测试运行方式

- Running Tests in Parallel or Consecutively
- Showing Function Output
- Running a Subset of Tests by Name
- Ignoring Some Tests Unless Specifically Request

## 单元测试

单元测试的目的在于将一小段代码单独隔离出来，从而迅速地确定这段代码的功能是否符合预期。

我们一般将单元测试与需要测试的代码存放在src目录下的同一文件中。同时也约定俗成地在每个源代码文件中都新建一个tests模块来存放测试函数，并使用cfg(test)对该模块进行标注。

在tests模块上标注#[cfg(test)]可以让Rust只在执行cargo test命令时编译和运行该部分测试代码，而在执行cargo build时剔除它们。

## 集成测试

集成测试的目的在于验证库的不同部分能否协同起来正常工作。能够独立正常工作的单元代码在集成运行时也会发生各种问题，所以集成测试的覆盖率同样是非常重要的。

为了创建集成测试，你首先需要建立一个tests目录。Cargo会自动在这个目录下寻找集成测试文件。我们可以在这个目录下创建任意多个测试文件，Cargo在编译时会将每个文件都处理为一个独立的包。
