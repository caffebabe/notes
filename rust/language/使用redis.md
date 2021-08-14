## redis-rs

Redis-rs is a high level redis library for Rust.

It provides convenient access to all Redis functionality through a very flexible but low-level API.

It uses a customizable type conversion trait so that any operation can return results in just the type you are expecting.

The crate is called redis and you can depend on it via cargo:

```rs
[dependencies]
redis = "0.20.2"
```

There are a few features defined that can enable additional functionality if so desired.

- acl: enables acl support (enabled by default)
- aio: enables async IO support (enabled by default)
- geospatial: enables geospatial support (enabled by default)
- script: enables script support (enabled by default)
- r2d2: enables r2d2 connection pool support (optional)
- cluster: enables redis cluster support (optional)
- tokio-comp: enables support for tokio (optional)
- connection-manager: enables support for automatic reconnection (optional)

## 基本操作

To open a connection you need to create a client and then to fetch a connection from it.

**In the future there will be a connection pool for those, currently each connection is separate and not pooled.**

Many commands are implemented through the Commands trait but manual command creation is also possible.

```rs
extern crate redis;

use redis::Commands;

// low level
fn get_mykey(con: &mut redis::Connection) -> redis::RedisResult<usize> {
    redis::cmd("GET").arg("my_key").query(con)
}

// high level
fn set_mykey(con: &mut redis::Connection) -> redis::RedisResult<()> {
    let _: () = con.set("my_key", 42)?;
    Ok(())
}

fn main() {
    let client = redis::Client::open("redis://:123@10.20.44.193:6379/0").unwrap();
    let mut con = client.get_connection().unwrap();
    set_mykey(&mut con).unwrap();
    let val = get_mykey(&mut con).expect("something wrong");
    println!("{}", val);
}
```

## 类型转换

```rs
let count : i32 = con.get("my_counter")?;
let count = con.get("my_counter").unwrap_or(0i32);
let k : Option<String> = con.get("missing_key")?;
let name : String = con.get("my_name")?;
let bin : Vec<u8> = con.get("my_binary")?;
let map : HashMap<String, i32> = con.hgetall("my_hash")?;
let keys : Vec<String> = con.hkeys("my_hash")?;
let mems : HashSet<i32> = con.smembers("my_set")?;
let (k1, k2) : (String, String) = con.get(&["k1", "k2"])?;
```

## pipeline

```rs
extern crate redis;

fn main() {
    let client = redis::Client::open("redis://:123@10.20.44.193:6379/0").unwrap();
    let mut con = client.get_connection().unwrap();

    let (k1, k2): (i32, i32) = redis::pipe()
        .atomic()
        .set("key_1", 42)
        .ignore()
        .set("key_2", 43)
        .ignore()
        .get("key_1")
        .get("key_2")
        .query(&mut con)
        .unwrap();

    println!("{:?}", (k1, k2));
}
```

## transaction

```rs
extern crate redis;
use redis::Commands;

fn main() {
    let client = redis::Client::open("redis://:123@10.20.44.193:6379/0").unwrap();
    let mut con = client.get_connection().unwrap();

    let key = "the_key";
    let (new_val,): (isize,) = redis::transaction(&mut con, &[key], |con, pipe| {
        let old_val: isize = con.get(key)?;
        pipe.set(key, old_val + 1).ignore().get(key).query(con)
    })
    .expect("something wrong");
    println!("The incremented number is: {}", new_val);
}
```

## Script

```rs
extern crate redis;

fn main() {
    let client = redis::Client::open("redis://:123@10.20.44.193:6379/0").unwrap();
    let mut con = client.get_connection().unwrap();

    let script = redis::Script::new(r"return tonumber(ARGV[1]) + tonumber(ARGV[2]);");
    let result: isize = script.arg(1).arg(2).invoke(&mut con).unwrap();
    assert_eq!(result, 3);
}
```
