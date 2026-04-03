## Проблема 1 – код проверяет несуществующую глобальную переменную `_price` вместо устанавливаемой цены `p` в `set_prices()`
1) Код до исправления

```py
    def set_prices(self, p: int):
        if self._mode == VendingMachine.Mode.OPERATION:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if _price <= 0:
            return VendingMachine.Response.INVALID_PARAM
        self._price = p
        return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `ADMINISTERING` (после `enter_admin_mode(117345294655382)`), `set_prices(p = 7)` (можно любое другое `p`)

3) Полученное значение, ожидаемое значение

Получено:
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/vasilisagolikova/PycharmProjects/OKIT_HW2/VendingMachine.py", line 92, in set_prices
    if _price <= 0:
       ^^^^^^
NameError: name '_price' is not defined. Did you mean: 'self._price'?
```

Ожидалось: `VendingMachine.Response.OK`, если `p > 0`, иначе `VendingMachine.Response.INVALID_PARAM`

4) Код после исправления

```py
    def set_prices(self, p: int):
        if self._mode == VendingMachine.Mode.OPERATION:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if p <= 0:
            return VendingMachine.Response.INVALID_PARAM
        self._price = p
        return VendingMachine.Response.OK
```

## Проблема 2 – `get_coins2()` возвращает неправильное значение
1) Код до исправления

```py
def get_coins2(self):
    if self._mode == VendingMachine.Mode.OPERATION:
        return self._coins1
    return self._coins2
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `OPERATION`, `_coins1 = 5`, `_coins2 = 7` (или другие ненулевые значения)

3) Полученное значение, ожидаемое значение

Получено: `get_coins2()` возвращает 5 (`=_coins1`)

Ожидалось: 0

4) Код после исправления

```py
def get_coins2(self):
    if self._mode == VendingMachine.Mode.OPERATION:
        return 0
    return self._coins2
```

## Проблема 3 – `fill_products()` игнорирует используемый режим
1) Код до исправления

```py
def fill_products(self):
    self._num = self._max
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `OPERATION`

3) Полученное значение, ожидаемое значение

Получено: `VendingMachine.Response.OK`, `_num == vm._max`

Ожидалось: `VendingMachine.Response.ILLEGAL_OPERATION`, `_num` не изменилось (например, осталось 0, если было 0)

4) Код после исправления

```py
def fill_products(self):
    if self._mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    self._num = self._max
    return VendingMachine.Response.OK
```

## Проблема 4 – `fill_coins()` проверяет `c2 > self._maxc1` вместо `c1 > self._maxc1` и не проверяет `c2 <= 0`
1) Код до исправления

```py
def fill_coins(self, c1: int, c2: int):
    if self._mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c2 > self._maxc1:
        return VendingMachine.Response.INVALID_PARAM
    if c1 <= 0 or c2 > self._maxc2:
        return VendingMachine.Response.INVALID_PARAM
    self._coins1 = c1
    self._coins2 = c2
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `ADMINISTERING`, `_maxc1 = 5`, `_maxc2 = 50`, `c1 = 6`, `c2 = 0` (либо другая комбинация, при которой `c1 > _maxc1` или `c2 <= 0`)

3) Полученное значение, ожидаемое значение

Получено: `VendingMachine.Response.OK`

Ожидалось: `VendingMachine.Response.INVALID_PARAM`

4) Код после исправления

```py
def fill_coins(self, c1: int, c2: int):
    if self._mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c1 > self._maxc1:
        return VendingMachine.Response.INVALID_PARAM
    if c2 <= 0 or c2 > self._maxc2:
        return VendingMachine.Response.INVALID_PARAM
    self._coins1 = c1
    self._coins2 = c2
    return VendingMachine.Response.OK
```

## Проблема 5 – `enter_admin_mode()` должен возвращать `VendingMachine.Response.CANNOT_PERFORM` при наличии внесенных покупателем средств, вместо этого возвращает `VendingMachine.Response.UNSUITABLE_CHANGE` 
1) Код до исправления

```py
def enter_admin_mode(self, code: int):
    if self._balance != 0:
        return VendingMachine.Response.UNSUITABLE_CHANGE
    if code != self._id:
        return VendingMachine.Response.INVALID_PARAM
    self._mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: любой из возможных, `vm._balance != 0`, `code = 117345294655382`

3) Полученное значение, ожидаемое значение

Получено: `VendingMachine.Response.UNSUITABLE_CHANGE`

Ожидалось: `VendingMachine.Response.CANNOT_PERFORM`

4) Код после исправления

```py
def enter_admin_mode(self, code: int):
    if self._balance != 0:
        return VendingMachine.Response.CANNOT_PERFORM
    if code != self._id:
        return VendingMachine.Response.INVALID_PARAM
    self._mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```

## Проблема 6 – `put_coin1()` добавляет монету в `_coins2` вместо `_coins1` и добавляет монету вида 2 на баланс пользователя вместо монеты вида 1, а также проверяет `self._coins2 == self._maxc2` вместо `self._coins1 == self._maxc1`
1) Код до исправления

```py
def put_coin1(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins2 == self._maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval2
    self._coins2 += 1
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `OPERATION`, (`_maxc1 = 50`, `_maxc2 = 50`, `_coins1 = 0`, `_coins2 = 0`), или (`_maxc1 = 50`, `_maxc2 = 50`, 
`_coins1 = maxc1`, `_coins2 = 0`) (или другие данные, при которых `_coins1 < _maxc1` или `_coins1 == _maxc1`, 
при этом `_coins2 < _maxc2` (если `_coins2 == _maxc2`, будет `VendingMachine.Response.CANNOT_PERFORM` при любых 
`_coins1`))

3) Полученное значение, ожидаемое значение

При `_coins1 < _maxc1`:

    Получено: `VendingMachine.Response.OK`, `_coins1` не изменилось, `_coins2` изменилось на +1, `_balance` изменился на +`_coinval2`
    
    Ожидалось: `VendingMachine.Response.OK`, `_coins1` изменилось на +1, `_coins2` не изменилось, `_balance` изменился на +`_coinval1`

При `_coins1 == _maxc1`

    Получено: `VendingMachine.Response.OK`, `_coins1` не изменилось, `_coins2` изменилось на +1, `_balance` изменился на +`_coinval2`
    
    Ожидалось: `VendingMachine.Response.CANNOT_PERFORM`

4) Код после исправления

```py
def put_coin1(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins1 == self._maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval1
    self._coins1 += 1
    return VendingMachine.Response.OK
```

## Проблема 7 – `put_coin2()` добавляет монету в `_coins1` вместо `_coins2` и добавляет монету вида 1 на баланс пользователя вместо монеты вида 2, а также проверяет `self._coins1 == self._maxc1` вместо `self._coins2 == self._maxc2`
1) Код до исправления

```py
def put_coin2(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins1 == self._maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval1
    self._coins1 += 1
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `OPERATION`, (`_maxc1 = 50`, `_maxc2 = 50`, `_coins1 = 0`, `_coins2 = 0`), или (`_maxc1 = 50`, `_maxc2 = 50`, 
`_coins1 = 0`, `_coins2 = _maxc2`) (или другие данные, при которых `_coins2 < _maxc2` или `_coins2 == _maxc2`, при этом `_coins1 < _maxc1` (если `_coins1 == _maxc1`, будет 
`VendingMachine.Response.CANNOT_PERFORM` при любых `_coins2`)

3) Полученное значение, ожидаемое значение

При `_coins2 < _maxc2`:

    Получено: `VendingMachine.Response.OK`, `_coins2` не изменилось, `_coins1` изменилось на +1, `_balance` изменился на +`_coinval1`
    
    Ожидалось: `VendingMachine.Response.OK`, `_coins2` изменилось на +1, `_coins1` не изменилось, `_balance` изменился на +`_coinval2`

При `_coins2 == _maxc2`:

    Получено: `VendingMachine.Response.OK`, `_coins2` не изменилось, `_coins1` изменилось на +1, `_balance` изменился на +`_coinval1`
    
    Ожидалось: `VendingMachine.Response.CANNOT_PERFORM`

4) Код после исправления

```py
def put_coin2(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._coins2 == self._maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self._balance += self._coinval2
    self._coins2 += 1
    return VendingMachine.Response.OK
```

## Проблема 8 – `give_product(int number)` возвращает при недостатке средств для сдачи `INSUFFICIENT_MONEY` вместо `TOO_BIG_CHANGE` 
1) Код до исправления
```py
def give_product(self, number: int):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if number <= 0 or number > self._max:
        return VendingMachine.Response.INVALID_PARAM
    if number > self._num:
        return VendingMachine.Response.INSUFFICIENT_PRODUCT
    res = self._balance - number * self._price
    if res < 0:
        return VendingMachine.Response.INSUFFICIENT_MONEY
    if res > self._coins1 * self._coinval1 + self._coins2 * self._coinval2:
        return VendingMachine.Response.INSUFFICIENT_MONEY
    if res > self._coins2 * self._coinval2:
        # using coinval1 == 1
        self._coins1 -= res - self._coins2 * self._coinval2
        self._coins2 = 0
        self._balance = 0
        self._num -= number
        return VendingMachine.Response.OK
    if res % self._coinval2 == 0:
        self._coins2 -= res // self._coinval2
        self._balance = 0
        self._num -= number
        return VendingMachine.Response.OK
    if self._coins1 == 0:
        return VendingMachine.Response.UNSUITABLE_CHANGE
    self._coins1 -= res // self._coinval2
    self._coins2 -= 1
    self._balance = 0
    self._num -= number
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `OPERATION`, `_num = 10`, `_balance = 10`, `_coins1 = 0`, `_coins2 = 0`, `number = 1`, `_price = 5` (или другие данные, при 
которых нет проблем с количеством продукции и баланса достаточно для покупки)

3) Полученное значение, ожидаемое значение

Получено: `VendingMachine.Response.INSUFFICIENT_MONEY`

Ожидалось: `VendingMachine.Response.TOO_BIG_CHANGE`

4) Код после исправления

```py
def give_product(self, number: int):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if number <= 0 or number > self._max:
        return VendingMachine.Response.INVALID_PARAM
    if number > self._num:
        return VendingMachine.Response.INSUFFICIENT_PRODUCT
    res = self._balance - number * self._price
    if res < 0:
        return VendingMachine.Response.INSUFFICIENT_MONEY
    if res > self._coins1 * self._coinval1 + self._coins2 * self._coinval2:
        return VendingMachine.Response.TOO_BIG_CHANGE
    if res > self._coins2 * self._coinval2:
        # using coinval1 == 1
        self._coins1 -= res - self._coins2 * self._coinval2
        self._coins2 = 0
        self._balance = 0
        self._num -= number
        return VendingMachine.Response.OK
    if res % self._coinval2 == 0:
        self._coins2 -= res // self._coinval2
        self._balance = 0
        self._num -= number
        return VendingMachine.Response.OK
    if self._coins1 == 0:
        return VendingMachine.Response.UNSUITABLE_CHANGE
    self._coins1 -= res // self._coinval2
    self._coins2 -= 1
    self._balance = 0
    self._num -= number
    return VendingMachine.Response.OK
```

## Проблема 9 – `return_money()` при нечетном балансе, `_coins2 >= _balance // 2` и `_coins1 >= 1` отнимает `_balance // _coinval2` от `_coins1` и 1 от `_coins2`, хотя должен отнимать `_balance // _coinval2` от `_coins2` и 1 от `_coins1`
1) Код до исправления
```py
def return_money(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._balance == 0:
        return VendingMachine.Response.OK
    if self._balance > self._coins1 * self._coinval1 + self._coins2 * self._coinval2:
        return VendingMachine.Response.TOO_BIG_CHANGE
    if self._balance > self._coins2 * self._coinval2:
        # using coinval1 == 1
        self._coins1 -= self._balance - self._coins2 * self._coinval2
        self._coins2 = 0
        self._balance = 0
        return VendingMachine.Response.OK
    if self._balance % self._coinval2 == 0:
        self._coins2 -= self._balance // self._coinval2
        self._balance = 0
        return VendingMachine.Response.OK
    if self._coins1 == 0:
        # using coinval1 == 1
        return VendingMachine.Response.UNSUITABLE_CHANGE
    # using coinval1 == 1
    self._coins1 -= self._balance // self._coinval2
    self._coins2 -= 1
    self._balance = 0
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `OPERATION`, `_coins2 = 10`, `_coins1 = 5`, `vm._balance = 7` (можно другие данные, главное, чтобы `_balance` был
нечетным и соблюдалось `_coins2 >= _balance // 2` и `_coins1 >= 1`. Также количество `_coins1` и `_coins2` будет 
корректироваться на правильные значения, если отнимается только одна монета вида 2, поэтому чтобы вычлось неверное 
значение нужно, чтобы `_balance >= 5`)

3) Полученное значение, ожидаемое значение

Получено: `VendingMachine.Response.OK`, `_coins2 == 9`, `_coins1 == 2`, `_balance == 0`

Ожидалось: `VendingMachine.Response.OK`, `_coins2 == 7`, `_coins1 == 4`, `_balance == 0`


4) Код после исправления

```py
def return_money(self):
    if self._mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self._balance == 0:
        return VendingMachine.Response.OK
    if self._balance > self._coins1 * self._coinval1 + self._coins2 * self._coinval2:
        return VendingMachine.Response.TOO_BIG_CHANGE
    if self._balance > self._coins2 * self._coinval2:
        # using coinval1 == 1
        self._coins1 -= self._balance - self._coins2 * self._coinval2
        self._coins2 = 0
        self._balance = 0
        return VendingMachine.Response.OK
    if self._balance % self._coinval2 == 0:
        self._coins2 -= self._balance // self._coinval2
        self._balance = 0
        return VendingMachine.Response.OK
    if self._coins1 == 0:
        # using coinval1 == 1
        return VendingMachine.Response.UNSUITABLE_CHANGE
    # using coinval1 == 1
    self._coins2 -= self._balance // self._coinval2
    self._coins1 -= 1
    self._balance = 0
    return VendingMachine.Response.OK
```

## Проблема 10 – `give_product()` при нечетной сдаче, `_coins2 >= res // 2` (res – сдача) и `_coins1 >= 1` отнимает `res // _coinval2` от `_coins1` и 1 от `_coins2`, хотя должен отнимать `res // _coinval2` от `_coins2` и 1 от `_coins1`
1) Код до исправления
```py
def give_product(self, number: int):
    ...
    self._coins1 -= res // self._coinval2
    self._coins2 -= 1
    self._balance = 0
    self._num -= number
    return VendingMachine.Response.OK
```

2) Данные, на которых наблюдается некорректное поведение

Режим: `OPERATION`, `_num = 10`, `vm._price = 3`, `_coins2 = 10`, `_coins1 = 5`, `vm._balance = 8`, `number = 1` 
(можно другие данные, главное, чтобы соблюдалось `number <= num` (чтобы не было проблем с количеством продукции), 
`res = _balance - number * _price` было нечетным, `_coins2 >= res // 2` и `_coins1 >= 1`. Также количество `_coins1` и 
`_coins2` будет корректироваться на правильные значения, если отнимается только одна монета вида 2, поэтому чтобы 
вычлось неверное значение нужно, чтобы `res >= 5`)

3) Полученное значение, ожидаемое значение

Получено: `VendingMachine.Response.OK`, `_coins2 == 9`, `_coins1 == 3`, `_balance == 0`, `_num == 9`

Ожидалось: `VendingMachine.Response.OK`, `_coins2 == 8`, `_coins1 == 4`, `_balance == 0`, `_num == 9`


4) Код после исправления

```py
def give_product(self, number: int):
    ...
    self._coins2 -= res // self._coinval2
    self._coins1 -= 1
    self._balance = 0
    self._num -= number
    return VendingMachine.Response.OK
```