# PyGSM (Python Grade Student Manager)

> **作者: Ash**  
> **GitHub: [https://github.com/Ash-Cpp/PyGSM](https://github.com/Ash-Cpp/PyGSM)**  
> **个人主页: [https://www.ashlab.site/](https://www.ashlab.site/)**

PyGSM 是一个基于 Python 的学生成绩管理系统，同时提供 **CLI（命令行界面）** 和 **GUI（图形界面）** 两种交互方式。支持学生信息的增删改查、成绩排序、数据持久化等功能。

---

## 目录

- [PyGSM (Python Grade Student Manager)](#pygsm-python-grade-student-manager)
  - [目录](#目录)
  - [项目架构](#项目架构)
  - [依赖](#依赖)
    - [PyQt6](#pyqt6)
    - [tabulate](#tabulate)
    - [wcwidth](#wcwidth)
  - [快速开始](#快速开始)
  - [核心模块详解 (core)](#核心模块详解-core)
    - [models.py — 数据模型层](#modelspy--数据模型层)
    - [manager.py — 数据管理器（含懒更新）](#managerpy--数据管理器含懒更新)
      - [懒更新（Lazy Update）](#懒更新lazy-update)
    - [storage.py — 数据持久化层](#storagepy--数据持久化层)
    - [stream.py — IO 流处理](#streampy--io-流处理)
    - [util.py — 工具模块](#utilpy--工具模块)
    - [mainwindow.py — 图形主窗口](#mainwindowpy--图形主窗口)
  - [CLI 模块 (csys.py)](#cli-模块-csyspy)
    - [期望调用设计模式 (expectCall)](#期望调用设计模式-expectcall)
      - [动态绑定示例](#动态绑定示例)
      - [与传统方案的对比](#与传统方案的对比)
  - [GUI 模块 (gsys.pyw)](#gui-模块-gsyspyw)
  - [启动方式](#启动方式)

---

## 项目架构

```
PyGSM/
├── main.py              # 程序入口，根据配置选择启动模式
├── config.json          # 配置文件（默认模式、上次使用的模式）
├── requirements.txt     # Python 依赖
├── README.md
├── cli/
│   └── csys.py          # CLI 主逻辑（命令行界面）
├── gui/
│   └── gsys.pyw         # GUI 主逻辑（图形界面）
├── core/
│   ├── models.py        # 数据模型层（Student 类）
│   ├── manager.py       # 数据管理器（GradeManager，含懒更新）
│   ├── storage.py       # 数据持久化层（文件读写）
│   ├── stream.py        # IO 流处理（控制台表格输出）
│   ├── util.py          # 工具模块（子进程启动等）
│   └── mainwindow.py    # 图形主窗口（PyQt6 实现）
└── data/
    └── studentsInfo.json # 学生数据存储文件
```

---

## 依赖

### PyQt6

> 版本: 6.11.0

Qt 是由英国 Riverbank Computing 公司开发的跨平台图形用户界面（GUI）应用程序开发框架。PyQt6 是为 C++ 领域的行业标准级 GUI 框架——Qt——所提供的 Python 官方第三方绑定（Bindings）。本项目中用于实现图形界面（GUI）部分。

### tabulate

> 版本: 0.10.0

tabulate 是一个用于将二维数据（如列表、字典等）快速转化为漂亮文本表格的 Python 库。本项目中用于 CLI 模式下学生信息的表格化展示。

### wcwidth

> 版本: 0.8.0

wcwidth 是一个底层工具库，它的前身是 C 语言中的 wcwidth() 函数（POSIX 标准）。它的唯一任务是：测量一个 Unicode 字符在终端（Terminal）中实际占用了几个"光标位置"（列宽）。作为 tabulate 的间接依赖引入。

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 直接启动（默认根据上次使用的模式启动）
python main.py

# 3. 或直接启动 CLI 模式
python cli/csys.py

# 4. 或直接启动 GUI 模式
python gui/gsys.pyw
```

---

## 核心模块详解 (core)

### models.py — 数据模型层

`Student` 类是系统的核心数据模型，封装了学生的基本信息与成绩数据。

**关键设计：**

- **属性封装**：`sum`（总分）和 `average`（平均分）通过 `@property` 只读暴露，在构造函数中一次性计算，后续通过 `update()` 方法增量更新，避免重复遍历成绩表。
- **增量更新**：`update()` 方法在修改单科成绩时，通过计算差值 `delta` 来更新总分和平均分，时间复杂度 O(1)。
- **下标访问**：实现了 `__getitem__` 和 `__setitem__` 魔法方法，支持 `student["语文"]` 这样的字典式访问语法。
- **序列化**：提供 `toDict()` 和 `toJson()` 方法，方便数据持久化。

```python
# 增量更新示例
def update(self, subject: str, newVal: any) -> None:
    oldVal = self.__grades[subject]
    delta = newVal - oldVal          # 计算差值
    self.__grades[subject] = newVal
    self.__sum += delta              # 总分增量更新
    self.__average += delta / self.__subCnt  # 平均分增量更新
```

### manager.py — 数据管理器（含懒更新）

`GradeManager` 是系统的数据管理核心，负责学生的增删改查与排序。

**核心数据结构：**

- `__studentsBySid`：以学号为键的字典，支持 O(1) 学号查找
- `__studentsByName`：以姓名为键的嵌套字典，支持 O(1) 姓名查找（同名可共存）
- `__sortedList`：排序后的学生列表缓存
- `__sortFlag`：脏标记，标识缓存是否有效

#### 懒更新（Lazy Update）

排序操作采用 **懒更新（Lazy Update）** 策略，这是本系统的一个关键设计亮点：

1. **脏标记机制**：当学生数据发生任何变更（增/删/改）时，仅将 `__sortFlag` 置为 `True`，并不立即重新排序。
2. **按需排序**：只有在真正需要获取排序结果时（调用 `getSortedList()`），才会检查 `__sortFlag` 并执行实际排序。
3. **性能优化**：避免在连续多次修改数据时反复排序，将多次排序合并为一次。

```python
def __sortList(self) -> None:
    """排序学生列表，懒更新"""
    if self.__sortFlag:  # 仅当脏标记为 True 时才排序
        students = self.__studentsBySid.values()
        self.__sortedList = sorted(students, key=lambda stu: (-stu.sum, stu.sid))
        self.__sortFlag = False  # 重置脏标记
```

**排序规则**：按总分从高到低排序，总分相同时按学号升序排列。

### storage.py — 数据持久化层

负责数据的文件读写与持久化，包含两个类：

- **`FileHandler`**：管理学生数据的 JSON 文件读写。初始化时从文件加载数据并构建 `GradeManager` 对象；通过 `saveToFile()` 方法将内存数据写回磁盘。利用 `atexit` 注册安全退出回调，确保程序退出时数据不丢失。
- **`ConfigHanlde`**：管理配置文件（config.json），记录默认启动模式和上次使用的界面模式。

**写入优化**：`saveToFile()` 内部通过 `cnt` 计数器和 `FLUSH_CNT` 阈值控制实际写入频率，避免频繁 I/O 操作。

### stream.py — IO 流处理

负责 CLI 模式下的控制台输出，使用 `tabulate` 库将学生数据渲染为美观的表格。

- `printOptions()`：打印操作菜单
- `printStudent()`：打印单个学生信息
- `printStudentsTable()`：打印带排名的学生总表
- `clearConsole()`：清空控制台

### util.py — 工具模块

提供跨平台子进程启动工具 `launchIndependent()`，支持在 CLI 和 GUI 之间切换时以独立进程启动对方，互不阻塞。

### mainwindow.py — 图形主窗口

基于 PyQt6 实现的图形界面主窗口，提供与 CLI 相同的增删改查功能，并支持表格内直接编辑成绩。

---

## CLI 模块 (csys.py)

`csys.py` 是命令行界面的主逻辑文件，采用 **路由表 + 循环** 的架构模式。

**核心设计：**

- **路由表（Router）**：使用字典将用户的操作编号映射到对应的处理函数，实现"表驱动编程"，代码结构清晰、易于扩展。
- **子菜单嵌套**：主菜单下嵌套"增删改查"子菜单，每个子功能独立封装为 `subXxx()` 函数。
- **异常安全**：所有用户输入均包裹在 `try-except` 中，支持 `Ctrl+C` 安全退出当前操作。

```python
# 路由表示例
mainRouter = {
    1: lambda: expectCall(subShowAll, False),
    2: lambda: expectCall(subCURD),
    3: lambda: expectCall(lambda: subClearHistory(mainOptions), False),
    4: lambda: expectCall(subToggleGUI),
    5: lambda: expectCall(subExit)
}
```

### 期望调用设计模式 (expectCall)

> **原创声明**：`expectCall` 是本人在开发 PyGSM 过程中原创设计的一个轻量级编程模式，旨在解决 CLI 路由表中"函数执行"与"返回值控制"之间的耦合问题。

`expectCall` 是一个自定义的轻量级设计模式，用于统一处理菜单路由的返回值逻辑。

**设计动机**：在 CLI 的路由循环中，每个操作执行后需要返回一个布尔值来控制是否刷新菜单。`expectCall` 将"执行函数"和"返回期望值"这两个逻辑封装在一起，使路由表更加简洁统一。


```python
def expectCall(func: callable, expectVal: bool = True) -> bool:
    """
    期望调用设计模式
    
    封装一个函数调用并返回期望的布尔值，用于统一路由表的返回值逻辑。
    
    Args:
        func (callable): 需要执行的回调函数
        expectVal (bool): 期望返回的布尔值，默认为 True
    
    Returns:
        bool: 返回 expectVal 指定的值
    
    使用场景:
        在 CLI 路由表中，每个操作执行后需要返回一个布尔值，
        用于控制主循环是否刷新菜单。expectCall 让路由表更加简洁统一。
    """
    func()           # 执行实际功能
    return expectVal # 返回期望值
```

**工作流程**：

```
用户输入操作编号
       ↓
  路由表查找 → 调用 expectCall(func, expectVal)
       ↓
  执行 func()  →  返回 expectVal
       ↓
  主循环判断返回值:
    - True  → 刷新菜单（清屏 + 重新打印选项）
    - False → 保持当前界面不变
```

**设计优势**：

1. **关注点分离**：将"函数执行"和"返回值控制"解耦，每个子函数只需关注自身业务逻辑，无需关心路由控制。
2. **代码复用**：所有路由项统一使用 `expectCall` 包装，避免在每个子函数中重复编写 `return True/False`。
3. **灵活性**：通过 `expectVal` 参数灵活控制是否刷新菜单。例如 `subShowAll` 展示总表后不需要刷新菜单（`expectVal=False`），而 `subCURD` 进入子菜单后需要刷新（`expectVal=True`）。

#### 动态绑定示例

`expectCall` 的核心思想是：**同一个函数，在不同的路由表中可以绑定不同的 `expectVal`，实现行为的动态切换**，而非将返回值写死在函数内部。

以 `subClearHistory` 为例，它在主菜单和子菜单中都被使用，但行为不同：

```python
# subClearHistory 本身只负责"清屏 + 打印选项"
# 它不需要知道调用者是谁，也不需要关心后续是否刷新菜单
def subClearHistory(options: list[str] = []):
    stream.clearConsole()
    stream.printOptions(options)

# 在主菜单中：清屏后保持主菜单界面，不需要额外刷新
mainRouter = {
    3: lambda: expectCall(lambda: subClearHistory(mainOptions), False),
    # ...
}

# 在子菜单中：清屏后进入子菜单，同样不需要额外刷新
curdRouter = {
    6: lambda: expectCall(lambda: subClearHistory(curdOptions), False),
    # ...
}
```

再看 `subShowAll` 的例子——它在主菜单和子菜单中都可以被调用，但刷新行为不同：

```python
# subShowAll 只负责展示数据，不关心路由控制
def subShowAll():
    stream.printStudentsTable(Manager.getSortedList())

# 在主菜单中：展示总表后保持菜单，不刷新
mainRouter = {
    1: lambda: expectCall(subShowAll, False),
    # ...
}

# 在子菜单中：展示总表后同样保持菜单，不刷新
curdRouter = {
    5: lambda: expectCall(subShowAll, False),
    # ...
}
```

而 `subCURD` 进入子菜单后需要刷新界面，`subToggleGUI` 切换界面后不需要刷新——这些差异全部通过路由表中的 `expectVal` 参数动态指定，子函数本身零感知：

```python
mainRouter = {
    2: lambda: expectCall(subCURD),          # expectVal=True  (默认)，进入子菜单后刷新
    4: lambda: expectCall(subToggleGUI, False),  # expectVal=False，切换后不刷新
}
```

这种设计将"做什么"（函数逻辑）与"做完后怎么办"（路由控制）彻底分离，实现了 **行为的路由表级动态绑定**。

#### 与传统方案的对比


假设没有 `expectCall`，每个子函数都需要在末尾显式 `return` 一个布尔值来控制菜单刷新：

**传统方案（无 expectCall）**：

```python
def subShowAll():
    stream.printStudentsTable(Manager.getSortedList())
    return False  # 展示总表后不刷新菜单

def subCURD():
    subClearHistory(curdOptions)
    return True   # 进入子菜单后刷新菜单

def subExit():
    sys.exit(0)
    return True   # ❌ 死代码，sys.exit 后永远不会执行到

mainRouter = {
    1: subShowAll,
    2: subCURD,
    3: subExit
}
```

**使用 expectCall 后**：

```python
def subShowAll():
    stream.printStudentsTable(Manager.getSortedList())
    # 无需 return，专注业务逻辑

def subCURD():
    subClearHistory(curdOptions)
    # 无需 return，专注业务逻辑

def subExit():
    sys.exit(0)
    # 无需 return，专注业务逻辑

mainRouter = {
    1: lambda: expectCall(subShowAll, False),
    2: lambda: expectCall(subCURD),
    3: lambda: expectCall(subExit)
}
```

| 对比维度 | 传统方案 | 使用 expectCall |
|:---|:---|:---|
| 职责清晰度 | 子函数既要执行业务逻辑，又要负责路由控制 | 子函数只关注业务逻辑，路由控制由 expectCall 统一管理 |
| 代码冗余 | 每个子函数末尾都需要 `return True/False` | 路由表中通过 `expectVal` 参数统一指定，零冗余 |
| 死代码风险 | `sys.exit()` 等终止性操作后的 `return` 永远不会执行 | 不存在死代码，`expectVal` 在路由表中直接指定 |
| 扩展性 | 新增功能时容易忘记写 `return` 导致路由异常 | 新增功能只需在路由表中添加一行 `lambda`，不易出错 |
| 可读性 | 路由控制逻辑分散在各个子函数中 | 路由控制逻辑集中在路由表中，一目了然 |

---


## GUI 模块 (gsys.pyw)

`gsys.pyw` 是图形界面的入口，基于 PyQt6 框架构建。使用 `.pyw` 扩展名确保在 Windows 下运行时不会弹出控制台窗口。

**功能特点：**

- 表格化展示学生信息（带排名）
- 支持添加、删除、查找学生
- 表格内直接双击编辑成绩，实时保存
- 一键切换至 CLI 界面

---

## 启动方式

| 方式 | 命令 | 说明 |
|:---:|:---|:---|
| 自动模式 | `python main.py` | 根据配置文件决定启动 CLI 或 GUI |
| CLI 模式 | `python cli/csys.py` | 直接启动命令行界面 |
| GUI 模式 | `python gui/gsys.pyw` | 直接启动图形界面 |

**配置文件 (config.json)**：

```json
{"defaultMode": "auto", "lastMode": "cli"}
```

- `defaultMode`：默认启动模式（`auto` / `cli` / `gui`）
- `lastMode`：上次使用的模式，当 `defaultMode` 为 `auto` 时生效
