## 二叉查找树(BST)

BST 是一棵空树或者具有下列性质的二叉树：

- 若任意节点的左子树不空，则左子树上所有节点的值均 **小于** 它的根节点的值;
- 若任意节点的右子树不空，则右子树上所有节点的值均 **大于** 它的根节点的值;
- 任意节点的左、右子树也分别为二叉查找树。

示例：

```java
                  50
                 /  \
                30   70
               / \   / \
              20 40 60 80 
```

### 数据结构定义

```java
public class BinarySearchTree {

    private static class Node {
        int key;
        Node left, right;

        public Node(int item) {
            key = item;
            left = right = null;
        }
    }

    private Node root;

    public BinarySearchTree() {
        root = null;
    }

    public void insert(int key) {
        // TODO：插入节点
    }

    public void inorder() {
        // TODO：中序遍历。BST的中序遍历是有序的
    }

    public void deleteKey(int key) { 
        // TODO: 删除元素key
     }
}
```

## 插入

递归实现：

```java
/**
 * 插入：递归实现
 *
 * @param root 根节点
 * @param key  值
 * @return 新的根节点
 */
private Node insertRec(Node root, int key) {
    if (root == null) {
        root = new Node(key);
        return root;
    }

    if (key < root.key)
        root.left = insertRec(root.left, key);
    else if (key > root.key)
        root.right = insertRec(root.right, key);

    return root;
}
```

循环实现：

```java
/**
 * 插入：循环实现
 *
 * @param key 值
 */
public void insertItr(int key) {
    Node node = new Node(key);
    if (root == null) {
        root = node;
        return;
    }

    Node prev = null;
    Node temp = root;
    while (temp != null) {
        if (temp.key > key) {
            prev = temp;
            temp = temp.left;
        } else if (temp.key < key) {
            prev = temp;
            temp = temp.right;
        }
    }

    if (prev.key > key) {
        prev.left = node;
    } else {
        prev.right = node;
    }
}
```

## 中序遍历

递归实现：

```java
/**
 * 中序遍历：递归实现
 *
 * @param root 根节点
 */
private void inorderRec(Node root) {
    if (root != null) {
        inorderRec(root.left);
        System.out.println(root.key);
        inorderRec(root.right);
    }
}
```

循环实现：

```java
/**
 * 中序遍历：循环实现，需要辅助栈
 */
public void inorderItr() {
    Node temp = root;
    Stack<Node> stack = new Stack<>();
    while (temp != null || !stack.isEmpty()) {
        if (temp != null) {
            stack.add(temp);
            temp = temp.left;
        } else {
            temp = stack.pop();
            System.out.print(temp.key + " ");
            temp = temp.right;
        }
    }
}
```

## 删除

删除key可能有三种情况：

1）如果待删除的是叶子节点，直接删除：

```java
              50                            50
           /     \         delete(20)      /   \
          30      70       --------->    30     70 
         /  \    /  \                     \    /  \ 
       20   40  60   80                   40  60   80
```

2）如果待删除的节点只有一个子节点，把子节点的值复制给待删除节点，然后删除子节点：

```java
              50                            50
           /     \         delete(30)      /   \
          30      70       --------->    40     70 
            \    /  \                          /  \ 
            40  60   80                       60   80
```

3）如果待删除节点有两个子节点: 找到该节点的中序前缀节点 N（右子树中最小的节点），把N的值复制给该节点，并删除N :

```java
              50                            60
           /     \         delete(50)      /   \
          40      70       --------->    40    70 
                 /  \                            \ 
                60   80                           80
```

代码如下：

```java
public void deleteKey(int key) {
    root = deleteRec(root, key);
}

private Node deleteRec(Node root, int key) {
    // base case
    if (root == null)
        return root;

    if (key < root.key) {
        root.left = deleteRec(root.left, key);
    } else if (key > root.key) {
        root.right = deleteRec(root.right, key);
    } else {
        // node with only one child or no child
        if (root.left == null) {
            return root.right;
        } else if (root.right == null) {
            return root.left;
        }

        // node with two children: Get the inorder
        // successor (smallest in the right subtree)
        root.key = minValue(root.right);

        // Delete the inorder successor
        root.right = deleteRec(root.right, root.key);
    }

    return root;
}

int minValue(Node root) {
    int minv = root.key;
    while (root.left != null) {
        minv = root.left.key;
        root = root.left;
    }
    return minv;
}
```

## 完整代码

```java
package com.example.demo.tree;

import java.util.Stack;

public class BinarySearchTree {

    private static class Node {
        int key;
        Node left, right;

        public Node(int item) {
            key = item;
            left = right = null;
        }
    }

    private Node root;

    public BinarySearchTree() {
        root = null;
    }

    public void insert(int key) {
        // root = insertRec(root, key);
        insertItr(key);
    }

    /**
     * 插入：递归实现
     *
     * @param root 根节点
     * @param key  值
     * @return 新的根节点
     */
    private Node insertRec(Node root, int key) {
        if (root == null) {
            root = new Node(key);
            return root;
        }

        if (key < root.key)
            root.left = insertRec(root.left, key);
        else if (key > root.key)
            root.right = insertRec(root.right, key);

        return root;
    }

    /**
     * 插入：循环实现
     *
     * @param key 值
     */
    public void insertItr(int key) {
        Node node = new Node(key);
        if (root == null) {
            root = node;
            return;
        }

        Node prev = null;
        Node temp = root;
        while (temp != null) {
            if (temp.key > key) {
                prev = temp;
                temp = temp.left;
            } else if (temp.key < key) {
                prev = temp;
                temp = temp.right;
            }
        }
        if (prev.key > key) {
            prev.left = node;
        } else {
            prev.right = node;
        }
    }

    public void inorder() {
        inorderRec(root);
        // inorderItr();
    }

    public void deleteKey(int key) {
        root = deleteRec(root, key);
    }

    private Node deleteRec(Node root, int key) {
        // base case
        if (root == null)
            return root;

        if (key < root.key) {
            root.left = deleteRec(root.left, key);
        } else if (key > root.key) {
            root.right = deleteRec(root.right, key);
        } else {
            // node with only one child or no child
            if (root.left == null) {
                return root.right;
            } else if (root.right == null) {
                return root.left;
            }

            // node with two children: Get the inorder
            // successor (smallest in the right subtree)
            root.key = minValue(root.right);

            // Delete the inorder successor
            root.right = deleteRec(root.right, root.key);
        }

        return root;
    }

    int minValue(Node root) {
        int minv = root.key;
        while (root.left != null) {
            minv = root.left.key;
            root = root.left;
        }
        return minv;
    }


    /**
     * 中序遍历：递归实现
     *
     * @param root 根节点
     */
    private void inorderRec(Node root) {
        if (root != null) {
            inorderRec(root.left);
            System.out.println(root.key);
            inorderRec(root.right);
        }
    }

    /**
     * 中序遍历：循环实现
     */
    public void inorderItr() {
        Node temp = root;
        Stack<Node> stack = new Stack<>();
        while (temp != null || !stack.isEmpty()) {
            if (temp != null) {
                stack.add(temp);
                temp = temp.left;
            } else {
                temp = stack.pop();
                System.out.print(temp.key + " ");
                temp = temp.right;
            }
        }
    }

    public static void main(String[] args) {
        BinarySearchTree tree = new BinarySearchTree();

  /*  create following BST
    50
  /  \
    30  70
    / \   / \
   20 40 60 80 */
        tree.insert(50);
        tree.insert(30);
        tree.insert(20);
        tree.insert(40);
        tree.insert(70);
        tree.insert(60);
        tree.insert(80);

        tree.deleteKey(20);
        tree.inorder();
    }
}
```

原文链接：
<https://www.geeksforgeeks.org/binary-search-tree-set-2-delete/>
