# Python 代码压缩工具

### 主要功能
压缩 Python 代码，使这份代码占的存储空间变小，主要适合在发布应用程序之前使用

这份代码会：
+ 去掉多余的注释
+ 把行首的 4 个空格换成 Tab
+ 去掉中间某些不必要的空格

### 使用方法
可以直接修改 main.py 使用，也可以通过 import 使用。  
使用示例一：
```py
file = open('code.py', 'r', encoding='utf-8')
code = file.read()
file.close()

ans = main(code)

file = open('ans.py', 'w', encoding='utf-8')
file.write(ans)
file.close()
```
在 `main.py` 的最后添加这段内容，然后把自己的代码赋值到同级目录下的 `code.py` 中，运行程序，`ans.py` 就是压缩后的内容。

使用示例二：
```py
import main

file = open('code.py', 'r', encoding='utf-8')
code = file.read()
file.close()

ans = main.main(code)

file = open('ans.py', 'w', encoding='utf-8')
file.write(ans)
file.close()
```
在 `main.py` 的同级目录下创建这个程序（避免命名为 `ans.py` 或者 `code.py`），然后把自己的代码赋值到同级目录下的 `code.py` 中，运行刚刚创建的程序，`ans.py` 就是压缩后的内容。

### 函数参数

+ `main` 函数的参数列表：
  
  | 参数名称 | 默认值（其它可能值） | 说明 |
  | :-- | :-- | :-- |
  | remove_comments | True (False) | 删除代码中的注释 |

### 写在最后
+ ~~确实没人看~~
+ 如果犯低级错误请大家多多谅解
