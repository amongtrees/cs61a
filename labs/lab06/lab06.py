from __future__ import annotations


class Transaction:
    def __init__(self, id: int, before: int, after: int):
        self.id = id
        self.before = before
        self.after = after

    def changed(self) -> bool:
        """Return whether the transaction resulted in a changed balance."""
        "*** YOUR CODE HERE ***"
        return self.before != self.after

    def report(self) -> str:
        """Return a string describing the transaction.

        >>> Transaction(3, 20, 10).report()
        '3: decreased 20->10'
        >>> Transaction(4, 20, 50).report()
        '4: increased 20->50'
        >>> Transaction(5, 50, 50).report()
        '5: no change'
        """
        msg: str = 'no change'
        if self.changed():
            "*** YOUR CODE HERE ***"
            if self.before < self.after:
                msg = 'increased ' + str(self.before) + '->' + str(self.after)
            else:
                msg = 'decreased ' + str(self.before) + '->' + str(self.after)
        return str(self.id) + ': ' + msg

class BankAccount:
    """A bank account that tracks its transaction history.

    >>> a = BankAccount('Eric')
    >>> a.deposit(100)    # Transaction 0 for a
    100
    >>> b = BankAccount('Erica')
    >>> a.withdraw(30)    # Transaction 1 for a
    70
    >>> a.deposit(10)     # Transaction 2 for a
    80
    >>> b.deposit(50)     # Transaction 0 for b
    50
    >>> b.withdraw(10)    # Transaction 1 for b
    40
    >>> a.withdraw(100)   # Transaction 3 for a
    'Insufficient funds'
    >>> len(a.transactions)
    4
    >>> len([t for t in a.transactions if t.changed()])
    3
    >>> for t in a.transactions:
    ...     print(t.report())
    0: increased 0->100
    1: decreased 100->70
    2: increased 70->80
    3: no change
    >>> b.withdraw(100)   # Transaction 2 for b
    'Insufficient funds'
    >>> b.withdraw(30)    # Transaction 3 for b
    10
    >>> for t in b.transactions:
    ...     print(t.report())
    0: increased 0->50
    1: decreased 50->40
    2: no change
    3: decreased 40->10
    """

    # *** YOU NEED TO MAKE CHANGES IN SEVERAL PLACES IN THIS CLASS ***
    
    
    def __init__(self, account_holder: str):
        self.balance: int = 0
        self.holder = account_holder
        self.transactions: list = []
        self.trans_id = 0

    def deposit(self, amount: int) -> int:
        """Increase the account balance by amount, add the deposit
        to the transaction history, and return the new balance.
        """
        self.new_transaction(self.balance, self.balance + amount)
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount: int) -> int | str:
        """Decrease the account balance by amount, add the withdraw
        to the transaction history, and return the new balance.
        """
        if amount > self.balance:
            self.new_transaction(self.balance, self.balance)
            return 'Insufficient funds'
        self.new_transaction(self.balance, self.balance - amount)
        self.balance = self.balance - amount
        return self.balance
    
    def new_transaction(self, before: int, after: int):
        self.transactions.append(Transaction(self.trans_id, before, after))
        self.trans_id += 1


class Email:
    """An email has the following instance attributes:

        msg (str): the contents of the message
        sender (Client): the client that sent the email
        recipient_name (str): the name of the recipient (another client)
    """
    def __init__(self, msg: str, sender, recipient_name: str):
        self.msg = msg
        self.sender = sender
        self.recipient_name = recipient_name

class Server:
    """Each Server has one instance attribute called clients that is a
    dictionary from client names to client objects.

    >>> s = Server()
    >>> # Dummy client class implementation for testing only
    >>> class Client:
    ...     def __init__(self, server, name):
    ...         self.inbox = []
    ...         self.server = server
    ...         self.name = name
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> s.register_client(a) 
    >>> s.register_client(b)
    >>> len(s.clients)  # we have registered 2 clients
    2
    >>> all([type(c) == str for c in s.clients.keys()])  # The keys in self.clients should be strings
    True
    >>> all([type(c) == Client for c in s.clients.values()])  # The values in self.clients should be Client instances
    True
    >>> new_a = Client(s, 'Alice')  # a new client with the same name as an existing client
    >>> s.register_client(new_a)
    >>> len(s.clients)  # the key of a dictionary must be unique
    2
    >>> s.clients['Alice'] is new_a  # the value for key 'Alice' should now be updated to the new client new_a
    True
    >>> e = Email("I love 61A", b, 'Alice')
    >>> s.send(e)
    >>> len(new_a.inbox)  # one email has been sent to new Alice
    1
    >>> type(new_a.inbox[0]) == Email  # a Client's inbox is a list of Email instances
    True
    """
    def __init__(self):
        self.clients = {}

    def send(self, email: Email):
        """Append the email to the inbox of the client it is addressed to.
            email is an instance of the Email class.
        """
        self.clients[email.recipient_name].inbox.append(email)

    def register_client(self, client):
        """Add a client to the clients mapping (which is a 
        dictionary from client names to client instances).
            client is an instance of the Client class.
        """
        self.clients[client.name] = client

class Client:
    """A client has a server, a name (str), and an inbox (list).

    >>> s = Server()
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> a.compose('Hello, World!', 'Bob')
    >>> b.inbox[0].msg
    'Hello, World!'
    >>> a.compose('CS 61A Rocks!', 'Bob')
    >>> len(b.inbox)
    2
    >>> b.inbox[1].msg
    'CS 61A Rocks!'
    >>> b.inbox[1].sender.name
    'Alice'
    """
    def __init__(self, server: Server, name: str):
        self.inbox: list = []
        self.server = server
        self.name = name
        server.register_client(self)

    def compose(self, message: str, recipient_name: str):
        """Send an email with the given message to the recipient."""
        email = Email(message, self, recipient_name)
        self.server.send(email)


class Mint:
    """A mint creates coins by stamping on years.

    The update method sets the mint's stamp to Mint.present_year.

    >>> mint = Mint()
    >>> mint.year
    2025
    >>> dime = mint.create(Dime)
    >>> dime.year
    2025
    >>> Mint.present_year = 2105  # Time passes
    >>> nickel = mint.create(Nickel)
    >>> nickel.year     # The mint has not updated its stamp yet
    2025
    >>> nickel.worth()  # 5 cents + (80 - 50 years)
    35
    >>> mint.update()   # The mint's year is updated to 2105
    >>> Mint.present_year = 2180     # More time passes
    >>> mint.create(Dime).worth()    # 10 cents + (75 - 50 years)
    35
    >>> Mint().create(Dime).worth()  # A new mint has the current year
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)
    115
    >>> Dime.cents = 20  # Upgrade all dimes!
    >>> dime.worth()     # 20 cents + (155 - 50 years)
    125
    """
    present_year = 2025

    def __init__(self):
        self.year: int
        self.update()

    def create(self, coin):
        "*** YOUR CODE HERE ***"
        return coin(self.year)

    def update(self) -> None:
        "*** YOUR CODE HERE ***"
        self.year = self.present_year

class Coin:
    cents = None # will be provided by subclasses, but not by Coin itself

    def __init__(self, year: int):
        self.year = year

    def worth(self) -> int:
        "*** YOUR CODE HERE ***"
        return self.cents + max(0, Mint.present_year - self.year - 50) if self.cents else 0

class Nickel(Coin):
    cents = 5

class Dime(Coin):
    cents = 10


class VirFib():
    """A Virahanka Fibonacci number.

    >>> start = VirFib()
    >>> start
    VirFib object, value 0
    >>> start.next()
    VirFib object, value 1
    >>> start.next().next()
    VirFib object, value 1
    >>> start.next().next().next()
    VirFib object, value 2
    >>> start.next().next().next().next()
    VirFib object, value 3
    >>> start.next().next().next().next().next()
    VirFib object, value 5
    >>> start.next().next().next().next().next().next()
    VirFib object, value 8
    >>> start.next().next().next().next().next().next() # Ensure start isn't changed
    VirFib object, value 8
    """

    def __init__(self, value: int = 0):
        self.value = value

    def next(self):
        "*** YOUR CODE HERE ***"
        if self.value == 0:
            result = VirFib(1)
        else:
            result = VirFib(self.value + self.previous)
        result.previous = self.value
        return result

    def __repr__(self) -> str:
        return "VirFib object, value " + str(self.value)
    
""" 
贴一下Gemini关于最后一个问题的看法（当然我是抄的答案）：

这是一种**完全可行**且思路非常独特的写法。

它与我们之前提到的“在 `__init__` 里预存 `next_value`”的思路正好相反：这一版代码的核心思想是**“回溯历史”**（Back-looking），即把**上一个数**硬塞给新的对象，让新对象自己去算。

我们来详细解析一下这种写法的逻辑和优缺点。

### 1. 代码逻辑解析

假设你的 `__init__` 是最简单的写法：
```python
def __init__(self, value=0):
    self.value = value
    # 注意：这里没有定义 self.previous，也没有 self.next_value
```

代码执行流程如下：

#### 第一步：`start = VirFib()`
*   `start.value` 是 `0`。
*   `start` 对象**没有** `previous` 属性。

#### 第二步：`obj1 = start.next()`
*   进入 `next` 方法。
*   `if self.value == 0:` 成立。
*   `result = VirFib(1)` -> 创建了一个新对象 `obj1`，值为 1。
*   **关键点**：`result.previous = self.value` -> 强行给 `obj1` 绑定了一个属性 `previous`，值为 `0`。
*   返回 `obj1`。
*   **状态**：`obj1` (value=1, previous=0)。

#### 第三步：`obj2 = obj1.next()`
*   进入 `next` 方法。
*   `obj1.value` 是 1，不等于 0。进入 `else`。
*   **计算**：`self.value (1) + self.previous (0)` = 1。
*   `result = VirFib(1)` -> 创建新对象 `obj2`，值为 1。
*   `result.previous = self.value` -> 给 `obj2` 绑定 `previous`，值为 `1`。
*   返回 `obj2`。
*   **状态**：`obj2` (value=1, previous=1)。

#### 第四步：`obj3 = obj2.next()`
*   进入 `else`。
*   **计算**：`self.value (1) + self.previous (1)` = 2。
*   `result = VirFib(2)` -> 创建新对象 `obj3`，值为 2。
*   `result.previous = 1`。
*   **状态**：`obj3` (value=2, previous=1)。

---

### 2. 这种写法的特点

#### 优点：
1.  **满足 Immutability（不可变性）**：每次都 `result = VirFib(...)` 创建新对象，没有修改 `self`，所以完美符合 doctest 中 `start` 不变的要求。
2.  **`__init__` 很干净**：初始化函数不需要去预测未来（不需要 `next_value`），只需要存当前的值。

#### 缺点/风险：
1.  **动态属性注入 (Attribute Injection)**：
    你在 `__init__` 之外的地方（`next` 方法里）强行给对象添加了一个 `previous` 属性。
    *   在 Python 中这是允许的，但在严格的面向对象编程（OOP）规范中，这通常被视为“代码异味”（Code Smell）。因为一个对象的结构应该在 `__init__` 中确定，而不是在运行过程中突然长出一个新肢体。
2.  **依赖特定路径**：
    如果我手动创建一个对象 `a = VirFib(5)`，然后直接调用 `a.next()`，程序会**直接报错**（AttributeError）。
    因为手动创建的 `a` 没有 `previous` 属性，而你的代码 `else` 分支必须依赖 `previous`。这使得这个类的健壮性变差了，它只能通过 `start.next()` 链式调用产生，不能半路出家。

### 3. 总结

这种写法是**正确**的，能通过测试。

*   **它的策略**：我不知道下一个数是几，但我把“我”存到下一个对象里（作为它的 `previous`）。下一个对象想要算它的下下个数时，它拿它自己的值加上我传给它的 `previous` 就行了。
*   **对比之前的写法**：
    *   **之前写法**：向前看。我出生时就知道下一代是谁（`next_value`）。
    *   **这种写法**：向后看。我出生时带着上一代的记忆（`previous`）。

在 Python 面试或作业中，这种写法通常会被接受，但面试官可能会问你如果手动初始化一个非 0 的 `VirFib` 会发生什么，以此考察你对 `AttributeError` 的理解。

"""