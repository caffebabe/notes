### 基本结构

ArrayList 基于数组实现，其内部是一个 Object 数组

```java
transient Object[] elementData; 
private int size;
```

### 构造函数

```java
public ArrayList(int initialCapacity) {
    if (initialCapacity > 0) {
        this.elementData = new Object[initialCapacity];
    } else if (initialCapacity == 0) {
        this.elementData = EMPTY_ELEMENTDATA;
    } else {
        throw new IllegalArgumentException("Illegal Capacity: "+
                                           initialCapacity);
    }
}

public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}
```

### add方法

```java
public boolean add(E e) {
    modCount++;
    add(e, elementData, size);
    return true;
}

private void add(E e, Object[] elementData, int s) {
    if (s == elementData.length)
        //满了需要扩容
        elementData = grow();

    elementData[s] = e;
    size = s + 1;
}
```

核心是扩容方法 grow

```java
private Object[] grow() {
    return grow(size + 1);
}

private Object[] grow(int minCapacity) {
    return elementData = Arrays.copyOf(elementData, newCapacity(minCapacity));
}
```

***扩容策略***

```java
private int newCapacity(int minCapacity) {
    // overflow-conscious code
    int oldCapacity = elementData.length;
    // 新容量是旧容量的1.5倍
    int newCapacity = oldCapacity + (oldCapacity >> 1);

    if (newCapacity - minCapacity <= 0) {
        if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA)
            return Math.max(DEFAULT_CAPACITY, minCapacity);
        if (minCapacity < 0) // overflow
            throw new OutOfMemoryError();
        return minCapacity;
    }

    return (newCapacity - MAX_ARRAY_SIZE <= 0)
        ? newCapacity
        : hugeCapacity(minCapacity);
}
```

### remove 方法

```java
public E remove(int index) {
    // jdk9 提供，如果 index 不满足条件会抛出异常
    Objects.checkIndex(index, size);
    
    final Object[] es = elementData;
    E oldValue = (E) es[index];
    fastRemove(es, index);

    return oldValue;
}

private void fastRemove(Object[] es, int i) {
    modCount++;
    final int newSize;
    if ((newSize = size - 1) > i)
        // 如果不是最后一个元素，删除后需要移动
        System.arraycopy(es, i + 1, es, i, newSize - i);
    es[size = newSize] = null;
}

// System.arraycopy 方法：
// 将 src 数组中从 srcPos 位置开始的 length 个元素
// 复制到 dest 数组中 despPos 开始的元素
@HotSpotIntrinsicCandidate
public static native void arraycopy(
    Object src, int  srcPos, Object dest, int destPos, int length)
```

### ensureCapacity

 如果容量没有设置很大，在插入大量元素之前，可以先调用该方法。

```java
public void ensureCapacity(int minCapacity) {
    if (minCapacity > elementData.length
        && !(elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA
             && minCapacity <= DEFAULT_CAPACITY)) {
        modCount++;
        grow(minCapacity);
    }
}
```

## 总结

1. ArrayList 内部基于数组实现，具有动态扩容的特点，扩容机制是加一半。
2. 建议构造函数传入恰当的初始容量避免扩容。
3. 如果初始容器不确定，在插入大量元素之前，先调用ensureCapacity方法避免扩容。
