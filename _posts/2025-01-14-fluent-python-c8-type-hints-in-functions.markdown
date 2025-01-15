---
layout: post
title: "[Fluent python] Chapter 8. Type Hints in Functions"
date: 2025-01-14 12:00:00 +0700
categories: fluent python
---

Type hints trong Python là các chú thích tùy chọn giúp chỉ định kiểu dữ liệu cho biến, đối số hàm và giá trị trả về.  Chúng hỗ trợ các công cụ phát triển như IDE và CI trong việc phát hiện lỗi thông qua phân tích tĩnh, đặc biệt hữu ích cho các kỹ sư phần mềm chuyên nghiệp. Tuy nhiên, với người dùng Python thông thường, lợi ích của type hints có thể không lớn bằng chi phí học tập, đặc biệt khi họ thường làm việc với các dự án nhỏ và kiểu động của Python đã đủ hiệu quả cho nhu cầu của họ.

### Table of contents

1. [About Gradual Typing](#AboutGradualTyping)
2. [Gradual Typing in Practice](#GradualTypinginPractice)
  * 2.1. [Starting with Mypy](#StartingwithMypy)
  * 2.2. [Making Mypy More Strict](#MakingMypyMoreStrict)
  * 2.3. [A Default Parameter Value](#ADefaultParameterValue)
  * 2.4. [Using None as a Default](#UsingNoneasaDefault)
3. [Types Are Defined by Supported Operations](#TypesAreDefinedbySupportedOperations)
4. [Types Usable in Annotations](#TypesUsableinAnnotations)
  * 4.1. [The Any Type](#TheAnyType)
  * 4.2. [Simple Types and Classes](#SimpleTypesandClasses)
  * 4.3. [Optional and Union Types](#OptionalandUnionTypes)
  * 4.4. [Generic Collections](#GenericCollections)
  * 4.5. [Tuple Types](#TupleTypes)
  * 4.6. [Generic Mappings](#GenericMappings)
  * 4.7. [Abstract Base Classes](#AbstractBaseClasses)
  * 4.8. [Iterable](#Iterable)
  * 4.9. [Parameterized Generics and TypeVar](#ParameterizedGenericsandTypeVar)
  * 4.10. [Static Protocols](#StaticProtocols)
  * 4.11. [Callable](#Callable)
  * 4.12. [NoReturn](#NoReturn)
5. [Annotating Positional Only and Variadic Parameters](#AnnotatingPositionalOnlyandVariadicParameters)
6. [Imperfect Typing and Strong Testing](#ImperfectTypingandStrongTesting)

---
###  1. <a name='AboutGradualTyping'></a>About Gradual Typing

Trong Python, **gradual typing** là một hệ thống cho phép bạn thêm thông tin về kiểu dữ liệu vào mã của mình (ví dụ: số nguyên, chuỗi, v.v.). Tuy nhiên, không giống như các ngôn ngữ khác, việc thêm kiểu dữ liệu trong Python là **tùy chọn** (optional). 

Hãy tưởng tượng bạn có một hộp đựng đồ chơi. Bình thường, bạn có thể bỏ bất cứ thứ gì vào hộp, chẳng hạn như xe hơi, búp bê, hoặc thậm chí là sách vở. Đây giống như Python không có **type hints** (gợi ý kiểu).

Nhưng nếu bạn muốn sắp xếp đồ chơi, bạn có thể dán nhãn lên hộp, ví dụ "Hộp đựng xe hơi". Bây giờ, khi bạn nhìn thấy nhãn, bạn biết rằng chỉ nên bỏ xe hơi vào hộp. **Type hints** trong Python cũng tương tự như vậy, chúng giúp bạn "dán nhãn" cho biến và hàm để chỉ ra loại dữ liệu chúng nên chứa.

**Dưới đây là một số điểm quan trọng về gradual typing:**

* **Optional:** Bạn không bắt buộc phải sử dụng type hints. Mã Python của bạn vẫn sẽ chạy bình thường ngay cả khi không có chúng.
* **Không bắt lỗi khi chạy:** Type hints chỉ giúp các công cụ như **type checker** (kiểm tra kiểu) phát hiện lỗi tiềm ẩn trước khi chạy chương trình.
* **Không cải thiện hiệu suất:** Hiện tại, type hints không làm cho mã Python chạy nhanh hơn.

**Ví dụ:**

```python
# Không có type hints
def cộng(a, b):
  return a + b

# Có type hints
def cộng(a: int, b: int) -> int:
  return a + b
```

Cả hai hàm `cộng` đều thực hiện cùng một chức năng. Tuy nhiên, hàm thứ hai sử dụng type hints để chỉ ra rằng `a` và `b` nên là số nguyên (`int`), và hàm sẽ trả về một số nguyên.

**Tóm lại:** Gradual typing trong Python mang đến sự linh hoạt cho người lập trình. Bạn có thể sử dụng type hints để cải thiện khả năng đọc mã và giảm lỗi, nhưng bạn không bắt buộc phải làm vậy.

---
###  2. <a name='GradualTypinginPractice'></a>Gradual Typing in Practice

Để hiểu rõ hơn về **gradual typing**, chúng ta sẽ xem xét một ví dụ thực tế với hàm `show_count`. Hàm này nhận vào một số lượng (`count`) và một từ (`word`), sau đó trả về một chuỗi mô tả số lượng kèm theo từ đó, có tính đến số ít/số nhiều. 

Ví dụ:

```python
>>> show_count(99, 'bird')
'99 birds'
>>> show_count(1, 'bird')
'1 bird'
>>> show_count(0, 'bird')
'no birds'
```

Ban đầu, hàm `show_count` được viết **không có type hints**:

```python
def show_count(count, word):
  if count == 1:
    return f'1 {word}'
  count_str = str(count) if count else 'no'
  return f'{count_str} {word}s'
```

Để kiểm tra kiểu dữ liệu, chúng ta sẽ sử dụng **Mypy**. Mypy là một **type checker** phổ biến cho Python, giúp phát hiện các lỗi tiềm ẩn liên quan đến kiểu dữ liệu.

**Lưu ý:** Có nhiều type checker khác cho Python như **pytype** (Google), **Pyright** (Microsoft), **Pyre** (Facebook),... Mỗi công cụ có những ưu điểm riêng. Ví dụ, pytype có thể xử lý mã không có type hints và đưa ra gợi ý hữu ích.

Bằng cách sử dụng Mypy và thêm **type hints** dần dần, chúng ta có thể cải thiện mã `show_count` và làm cho nó rõ ràng hơn về kiểu dữ liệu được sử dụng.

**Ví dụ với type hints:**

```python
def show_count(count: int, word: str) -> str:
  if count == 1:
    return f'1 {word}'
  count_str = str(count) if count else 'no'
  return f'{count_str} {word}s'
```

Trong ví dụ này, chúng ta đã thêm type hints `int` cho `count`, `str` cho `word` và `str` cho giá trị trả về. Điều này giúp Mypy hiểu rõ hơn về kiểu dữ liệu của hàm và phát hiện ra các lỗi tiềm ẩn.

**Tóm lại:** Việc sử dụng gradual typing và type checker như Mypy giúp chúng ta viết mã Python an toàn và dễ bảo trì hơn.

####  2.1. <a name='StartingwithMypy'></a>Starting with Mypy

Để kiểm tra kiểu dữ liệu trong mã Python, chúng ta sẽ sử dụng **Mypy**. 

Đầu tiên, cần cài đặt Mypy bằng lệnh `pip install mypy`. Sau đó, chạy Mypy trên module `messages.py` (chứa hàm `show_count`) bằng lệnh `mypy messages.py`.

Kết quả trả về là "Success: no issues found in 1 source file". Điều này có nghĩa là Mypy (với cài đặt mặc định) không tìm thấy vấn đề gì với mã hiện tại.

**Lưu ý:**

* Phiên bản Mypy được sử dụng trong ví dụ là 0.910. Mypy vẫn đang trong giai đoạn beta, nên có thể có một số thay đổi không tương thích ngược trong tương lai.
* Nếu hàm không có **type hints**, Mypy sẽ bỏ qua nó theo mặc định.

Ngoài Mypy, chúng ta còn có các **unit tests** (kiểm thử đơn vị) được viết bằng **pytest** trong file `messages_test.py`. Unit tests giúp đảm bảo hàm `show_count` hoạt động đúng như mong đợi với các đầu vào khác nhau.

```python
from pytest import mark
from messages import show_count

@mark.parametrize('qty, expected', [
(1, '1 part'),
(2, '2 parts'),
])
def test_show_count(qty, expected):
  got = show_count(qty, 'part')
  assert got == expected

def test_show_count_zero():
  got = show_count(0, 'part')
  assert got == 'no parts'
```

Bây giờ, chúng ta sẽ bắt đầu thêm **type hints** vào mã `show_count` dựa trên gợi ý của Mypy. Việc này giúp Mypy phân tích mã kỹ hơn và phát hiện ra các lỗi tiềm ẩn liên quan đến kiểu dữ liệu.


####  2.2. <a name='MakingMypyMoreStrict'></a>Making Mypy More Strict


Mặc định, Mypy không yêu cầu bạn phải thêm type hints cho tất cả các hàm. Tuy nhiên, bạn có thể sử dụng các tùy chọn dòng lệnh để làm cho Mypy nghiêm ngặt hơn.

 **`--disallow-untyped-defs`**

Tùy chọn `--disallow-untyped-defs` yêu cầu tất cả các hàm phải có type hints cho tất cả các tham số và giá trị trả về. Nếu chạy Mypy với tùy chọn này trên file `messages_test.py`, bạn sẽ nhận được 3 lỗi:

```
messages.py:14: error: Function is missing a type annotation
messages_test.py:10: error: Function is missing a type annotation
messages_test.py:15: error: Function is missing a return type annotation
messages_test.py:15: note: Use "-> None" if function does not return a value
```

**`--disallow-incomplete-defs`**

Tùy chọn `--disallow-incomplete-defs` chỉ yêu cầu type hints cho các hàm đã được chú thích một phần. Ví dụ, nếu bạn chỉ thêm type hint cho giá trị trả về của hàm `show_count`:

```python
def show_count(count, word) -> str:
  ...
```

thì Mypy sẽ yêu cầu bạn thêm type hints cho các tham số `count` và `word`.

**Thêm type hints dần dần**

Sử dụng `--disallow-incomplete-defs` cho phép bạn thêm type hints dần dần, từng hàm một, mà không bị cảnh báo về các hàm chưa được chú thích.

Sau khi thêm type hints đầy đủ cho `show_count`:

```python
def show_count(count: int, word: str) -> str:
  ...
```

Mypy sẽ không báo lỗi nữa.

**Cấu hình Mypy**

Thay vì gõ các tùy chọn dòng lệnh mỗi lần chạy Mypy, bạn có thể lưu các tùy chọn yêu thích vào file cấu hình `mypy.ini`. Ví dụ:

```ini
[mypy]
python_version = 3.9
warn_unused_configs = True
disallow_incomplete_defs = True
```

File cấu hình này sẽ yêu cầu Mypy sử dụng Python 3.9, cảnh báo về các cấu hình không sử dụng và yêu cầu type hints cho các hàm đã được chú thích một phần.


####  2.3. <a name='ADefaultParameterValue'></a>A Default Parameter Value

Hàm `show_count` ban đầu chỉ hoạt động với các danh từ thông thường (số nhiều tạo bằng cách thêm 's'). Để xử lý các danh từ bất quy tắc, chúng ta cần cho phép người dùng cung cấp dạng số nhiều, ví dụ:

```python
>>> show_count(3, 'mouse', 'mice')
'3 mice'
```

Để bắt đầu, chúng ta sẽ thêm một **unit test** kiểm tra trường hợp này:

```python
def test_irregular() -> None:
  got = show_count(2, 'child', 'children')
  assert got == '2 children'
```

**Lưu ý:**  Cần thêm **type hint** `-> None` cho hàm test, nếu không Mypy sẽ không kiểm tra nó.

Khi chạy Mypy, chúng ta sẽ gặp lỗi "Too many arguments for 'show_count'" vì hàm hiện tại chỉ nhận 2 tham số.

Để sửa lỗi, chúng ta thêm tham số `plural` (tùy chọn) vào hàm `show_count`:

```python
def show_count(count: int, singular: str, plural: str = '') -> str:
  if count == 1:
    return f'1 {singular}'
  count_str = str(count) if count else 'no'
  if not plural:
    plural = singular + 's'
  return f'{count_str} {plural}'
```

Tham số `plural` có giá trị mặc định là chuỗi rỗng (`''`). Nếu người dùng không cung cấp `plural`, hàm sẽ tự động thêm 's' vào `singular`.

**Một lỗi type hint thường gặp**

Một lỗi type hint phổ biến là viết `color=str` thay vì `color: str`. `color=str` sẽ gán giá trị mặc định của `color` là `str` (kiểu dữ liệu chuỗi), trong khi `color: str` mới là cách khai báo type hint chính xác.

**Code Style**

Để đảm bảo code style nhất quán, nên sử dụng các công cụ như **flake8** và **blue**.

* **flake8:** Kiểm tra code style và các vấn đề khác.
* **blue:** Tự động format code theo (hầu hết) các quy tắc của **black**.

**blue** được ưa chuộng hơn **black** vì nó tuân theo style của Python là sử dụng dấu nháy đơn (') làm mặc định. Nếu bạn buộc phải sử dụng **black**, hãy dùng tùy chọn `-S` để giữ nguyên dấu nháy.

####  2.4. <a name='UsingNoneasaDefault'></a>Using None as a Default

Trong ví dụ trước, tham số `plural` có kiểu `str` và giá trị mặc định là `''`. Điều này không gây ra xung đột kiểu dữ liệu.

Tuy nhiên, trong nhiều trường hợp, sử dụng `None` làm giá trị mặc định sẽ tốt hơn, đặc biệt khi tham số là kiểu dữ liệu có thể thay đổi (**mutable type**). 

Để sử dụng `None` làm giá trị mặc định cho `plural`, chúng ta cần khai báo kiểu của nó là `Optional[str]`:

```python
from typing import Optional

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
  ...
```

**Giải thích:**

* `Optional[str]` nghĩa là `plural` có thể là một chuỗi (`str`) hoặc `None`.
* Cần chỉ định rõ ràng giá trị mặc định `= None`.

**Lưu ý:**

* Nếu không gán giá trị mặc định cho `plural`, Python sẽ coi nó là tham số bắt buộc, vì type hints bị bỏ qua khi chạy chương trình.
* Cần import `Optional` từ module `typing`. Nên sử dụng cú pháp `from typing import X` để rút ngắn khai báo kiểu dữ liệu.

**Tên gọi `Optional` có thể gây hiểu nhầm:**

Thực tế, `Optional` không làm cho tham số trở nên tùy chọn. Chính việc gán giá trị mặc định mới làm điều đó. `Optional[str]` chỉ đơn giản có nghĩa là kiểu dữ liệu của tham số có thể là `str` hoặc `NoneType`. Trong các ngôn ngữ như Haskell và Elm, kiểu dữ liệu tương tự được gọi là `Maybe`.

Sau khi tìm hiểu về **gradual typing** trong thực tế, chúng ta sẽ xem xét ý nghĩa của khái niệm "kiểu" trong lập trình.


---
###  3. <a name='TypesAreDefinedbySupportedOperations'></a>Types Are Defined by Supported Operations

Trong Python, **kiểu dữ liệu** (type) không chỉ là tập hợp các giá trị mà còn là tập hợp các **phép toán** (operation) có thể áp dụng lên các giá trị đó.

Ví dụ, xét hàm `double`:

```python
def double(x):
  return x * 2
```

Tham số `x` có thể thuộc nhiều kiểu dữ liệu khác nhau, miễn là nó hỗ trợ phép nhân (`*`) với số nguyên. Ví dụ:

* Các kiểu số: `int`, `float`, `complex`, `Fraction`, `numpy.uint32`,...
* Các kiểu chuỗi: `str`
* Các kiểu danh sách: `list`, `tuple`, `array`,...
* `numpy.array` với nhiều chiều

Tuy nhiên, nếu ta thêm type hint `abc.Sequence` cho `x`:

```python
from collections import abc

def double(x: abc.Sequence):
  return x * 2
```

thì **type checker** (như Mypy) sẽ báo lỗi, vì `abc.Sequence` không hỗ trợ phép nhân.

**Duck typing vs. Nominal typing**

Python sử dụng **duck typing**: một đối tượng thuộc kiểu nào không quan trọng, miễn là nó hỗ trợ các phép toán cần thiết. 

Ngược lại, **nominal typing** (được hỗ trợ bởi type hints) yêu cầu đối tượng phải thuộc đúng kiểu dữ liệu đã khai báo.

Ví dụ:

```python
class Bird:
  pass

class Duck(Bird):
  def quack(self):
    print('Quack!')

def alert_duck(birdie: Duck) -> None:
  birdie.quack()

def alert_bird(birdie: Bird) -> None:
  birdie.quack() 
```

Mypy sẽ báo lỗi ở hàm `alert_bird` vì lớp `Bird` không có phương thức `quack`. Tuy nhiên, khi chạy chương trình, nếu ta gọi `alert_bird` với đối tượng `Duck`, nó vẫn sẽ hoạt động.

**Lợi ích của type hints**

Trong các ví dụ nhỏ, lợi ích của type hints có thể không rõ ràng. Tuy nhiên, trong các dự án lớn, type hints giúp phát hiện lỗi sớm, cải thiện khả năng đọc hiểu mã và bảo trì code dễ dàng hơn.

**Tóm lại:**

* Kiểu dữ liệu được định nghĩa bởi các phép toán được hỗ trợ.
* Python sử dụng duck typing, trong khi type hints hỗ trợ nominal typing.
* Type hints giúp phát hiện lỗi sớm và cải thiện chất lượng mã.

---
###  4. <a name='TypesUsableinAnnotations'></a>Types Usable in Annotations
####  4.1. <a name='TheAnyType'></a>The Any Type

Trong hệ thống kiểu dữ liệu "gradual" của Python, kiểu dữ liệu `Any` đóng vai trò then chốt. Nó còn được gọi là kiểu dữ liệu động.

**`Any` là gì?**

Khi trình kiểm tra kiểu dữ liệu (type checker) gặp một hàm không được khai báo kiểu như sau:

```python
def double(x):
  return x * 2
```

Nó sẽ tự hiểu hàm này như sau:

```python
def double(x: Any) -> Any:
  return x * 2
```

Điều này có nghĩa là tham số `x` và giá trị trả về có thể thuộc **bất kỳ kiểu dữ liệu nào**, kể cả các kiểu khác nhau. `Any` được giả định là hỗ trợ mọi phép toán.

**So sánh `Any` với `object`**

Xét hàm sau:

```python
def double(x: object) -> object:
  return x * 2
```

Hàm này cũng chấp nhận tham số thuộc mọi kiểu dữ liệu, vì mọi kiểu dữ liệu đều là kiểu con của `object`. Tuy nhiên, trình kiểm tra kiểu dữ liệu sẽ báo lỗi với hàm này. Lý do là `object` không hỗ trợ phép nhân (`__mul__`).

**`Any` hoạt động như thế nào?**

`Any` là một kiểu dữ liệu đặc biệt, vừa nằm ở **đỉnh** vừa nằm ở **đáy** của hệ thống phân cấp kiểu dữ liệu. 

* Nó vừa là kiểu **tổng quát nhất** (general type) -  tham số `n: Any` chấp nhận giá trị của mọi kiểu dữ liệu.
* Nó cũng vừa là kiểu **chuyên biệt nhất** (specialized type) - hỗ trợ mọi phép toán.

Tuy nhiên, trên thực tế không có kiểu dữ liệu nào hỗ trợ mọi phép toán. Vì vậy, việc sử dụng `Any` sẽ **ngăn trình kiểm tra kiểu dữ liệu phát hiện các lỗi tiềm ẩn** trước khi chương trình gặp lỗi khi chạy.

**Ví dụ:**

```python
def f3(p: Any) -> None: # p có thể là bất kỳ kiểu dữ liệu nào
  ...
f3("Hello")  # OK
f3(123)     # OK
f3([1, 2, 3]) # OK
```

**`Subtype-of` và `consistent-with`**

* **`Subtype-of`**:  Mối quan hệ kế thừa giữa các kiểu dữ liệu. Ví dụ, `Dog` là subtype-of của `Animal`.
* **`consistent-with`**: Mối quan hệ tương thích giữa các kiểu dữ liệu, bao gồm cả `Any`.

**Quy tắc `consistent-with`:**

1. Nếu `T2` là subtype-of của `T1`, thì `T2` consistent-with `T1`.
2. Mọi kiểu dữ liệu đều consistent-with `Any`.
3. `Any` consistent-with mọi kiểu dữ liệu.

**Tóm lại:**

`Any` là một kiểu dữ liệu đặc biệt trong Python, cho phép bạn bỏ qua việc kiểm tra kiểu dữ liệu. Tuy nhiên, cần sử dụng `Any` một cách cẩn thận để tránh lỗi tiềm ẩn trong chương trình.

####  4.2. <a name='SimpleTypesandClasses'></a>Simple Types and Classes

**Kiểu dữ liệu đơn giản (Simple types)** như `int`, `float`, `str` và `bytes` có thể được sử dụng trực tiếp trong type hints. 

**Lớp cụ thể (Concrete classes)** từ thư viện chuẩn, các gói mở rộng hoặc do người dùng định nghĩa (ví dụ: `FrenchDeck`, `Vector2d`, `Duck`) cũng có thể được sử dụng.

**Lớp trừu tượng (Abstract base classes)** cũng hữu ích, chúng ta sẽ tìm hiểu thêm về chúng khi học về kiểu dữ liệu tập hợp (collection types).

**`consistent-with` trong lớp**

Trong trường hợp của các lớp, `consistent-with` được định nghĩa giống như `subtype-of`: một lớp con (subclass) sẽ `consistent-with` tất cả các lớp cha (superclass) của nó. 

Tuy nhiên, có một ngoại lệ quan trọng:

**`int` là `consistent-with` `complex`**

Mặc dù không có mối quan hệ kế thừa trực tiếp giữa các kiểu dữ liệu `int`, `float` và `complex` (chúng đều là lớp con trực tiếp của `object`), nhưng PEP 484 (tài liệu hướng dẫn về type hints) quy định rằng:

* `int` là `consistent-with` `float`
* `float` là `consistent-with` `complex`

Điều này hợp lý trong thực tế vì `int` hỗ trợ tất cả các phép toán của `float` và còn có thêm các phép toán bit như `&`, `|`, `<<`, v.v. Kết quả cuối cùng là: `int` là `consistent-with` `complex`. 

Ví dụ: với `i = 3`, `i.real` sẽ là 3 và `i.imag` là 0.

**Tóm lại:**

Type hints trong Python cho phép bạn sử dụng cả kiểu dữ liệu đơn giản và lớp. `consistent-with` được sử dụng để xác định tính tương thích giữa các kiểu dữ liệu, với một ngoại lệ đặc biệt là `int` tương thích với `complex`.


####  4.3. <a name='OptionalandUnionTypes'></a>Optional and Union Types

**`Optional`**

Như đã thấy trong phần "Sử dụng `None` làm giá trị mặc định", kiểu dữ liệu đặc biệt `Optional` giải quyết vấn đề khi có `None` làm giá trị mặc định, ví dụ:

```python
from typing import Optional

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
  ...
```

`Optional[str]` thực chất là viết tắt của `Union[str, None]`, nghĩa là kiểu dữ liệu của `plural` có thể là `str` hoặc `None`.

**`Union`**

`Union` cho phép một biến có thể mang một trong nhiều kiểu dữ liệu khác nhau. Ví dụ, hàm `ord()` có thể nhận đầu vào là `str` hoặc `bytes`:

```python
from typing import Union

def ord(c: Union[str, bytes]) -> int: ...
```

**Cú pháp mới trong Python 3.10**

Từ Python 3.10, ta có thể viết `str | bytes` thay vì `Union[str, bytes]`. Ví dụ:

```python
# Trước Python 3.10
plural: Optional[str] = None 

# Từ Python 3.10
plural: str | None = None 
```

**Lưu ý khi sử dụng `Union`**

* Nên tránh tạo các hàm trả về kiểu `Union` nếu có thể, vì nó sẽ buộc người dùng phải kiểm tra kiểu dữ liệu của giá trị trả về khi chạy chương trình.
* `Union[]` yêu cầu ít nhất hai kiểu dữ liệu.
* `Union` hữu ích hơn khi sử dụng với các kiểu dữ liệu không tương thích với nhau. Ví dụ: `Union[int, float]` là thừa vì `int` tương thích với `float`.


**Ví dụ:**

```python
from typing import Union

def parse_token(token: str) -> Union[str, float]:
  try:
    return float(token)  # Chuyển đổi token thành số thực nếu có thể
  except ValueError:
    return token  # Nếu không thể chuyển đổi, trả về token dưới dạng chuỗi

result = parse_token("123.45")  # result sẽ là float
result = parse_token("abc")  # result sẽ là str
```

####  4.4. <a name='GenericCollections'></a>Generic Collections

Hầu hết các tập hợp (collections) trong Python đều là **không đồng nhất (heterogeneous)**. Ví dụ, bạn có thể đặt hỗn hợp các kiểu dữ liệu khác nhau vào một `list`. Tuy nhiên, trong thực tế, điều này không hữu ích lắm: nếu bạn đặt các đối tượng vào một tập hợp, bạn thường muốn thực hiện các thao tác trên chúng sau đó, và điều này thường có nghĩa là chúng phải chia sẻ ít nhất một phương thức chung.

**Kiểu dữ liệu chung chung (Generic types)** có thể được khai báo với các tham số kiểu (type parameters) để chỉ định kiểu dữ liệu của các phần tử mà chúng có thể xử lý.

Ví dụ, một `list` có thể được tham số hóa để ràng buộc kiểu dữ liệu của các phần tử trong đó:

```python
def tokenize(text: str) -> list[str]:
  return text.upper().split()
```

Trong Python 3.9 trở lên, điều này có nghĩa là `tokenize` trả về một `list` mà mọi phần tử đều có kiểu dữ liệu là `str`.

**Các tập hợp hỗ trợ `Generic type hints`**

PEP 585 liệt kê các tập hợp từ thư viện chuẩn chấp nhận `generic type hints`. Dưới đây là một số ví dụ:

* `list`
* `set`
* `frozenset`
* `collections.deque`
* `abc.Container`
* `abc.Collection`
* `abc.Sequence`
* `abc.Set`
* `abc.MutableSequence`
* `abc.MutableSet`

**`tuple`** và các kiểu dữ liệu ánh xạ (mapping types) hỗ trợ các `type hints` phức tạp hơn.

**Hỗ trợ cũ và các kiểu dữ liệu tập hợp không dùng nữa**

Đối với Python 3.7 và 3.8, bạn cần import `__future__` để sử dụng cú pháp `[]` với các tập hợp tích hợp như `list`:

```python
from __future__ import annotations

def tokenize(text: str) -> list[str]:
  return text.upper().split()
```

PEP 585 đã bắt đầu một quá trình cải thiện khả năng sử dụng của `generic type hints`. Quá trình này bao gồm việc giới thiệu cú pháp `list[str]`, loại bỏ dần các kiểu dữ liệu chung chung dư thừa từ module `typing` và cuối cùng là loại bỏ hoàn toàn chúng trong các phiên bản Python tương lai.

####  4.5. <a name='TupleTypes'></a>Tuple Types

Có ba cách để chú thích kiểu dữ liệu cho `tuple`:

**1. Tuples như bản ghi (records)**

Khi sử dụng `tuple` như một bản ghi, sử dụng hàm dựng sẵn `tuple` và khai báo kiểu dữ liệu của các trường trong `[]`. 

Ví dụ, `tuple[str, float, str]` sẽ chấp nhận một `tuple` với tên thành phố, dân số và quốc gia: `('Shanghai', 24.28, 'China')`.

```python
from geolib import geohash as gh  # type: ignore

PRECISION = 9

def geohash(lat_lon: tuple[float, float]) -> str:
  return gh.encode(*lat_lon, PRECISION)
```

Trong ví dụ trên, tham số `lat_lon` được chú thích là một `tuple` với hai trường `float`.

**2. Tuples như bản ghi với trường được đặt tên**

Để chú thích một `tuple` với nhiều trường hoặc các loại `tuple` cụ thể mà mã của bạn sử dụng ở nhiều nơi, nên sử dụng `typing.NamedTuple`.

```python
from typing import NamedTuple
from geolib import geohash as gh  # type: ignore

PRECISION = 9

class Coordinate(NamedTuple):
  lat: float
  lon: float

def geohash(lat_lon: Coordinate) -> str:
  return gh.encode(*lat_lon, PRECISION)
```

`typing.NamedTuple` là một factory cho các lớp con của `tuple`, vì vậy `Coordinate` là `consistent-with` `tuple[float, float]`.

**3. Tuples như chuỗi bất biến (immutable sequences)**

Để chú thích các `tuple` có độ dài không xác định được sử dụng như các danh sách bất biến, bạn phải chỉ định một kiểu dữ liệu duy nhất, theo sau là dấu phẩy và `...` (dấu ba chấm của Python).

Ví dụ, `tuple[int, ...]` là một `tuple` với các phần tử là `int`. Dấu ba chấm cho biết số lượng phần tử >= 1 là chấp nhận được.

```python
from collections.abc import Sequence

def columnize(
  sequence: Sequence[str], num_columns: int = 0
) -> list[tuple[str, ...]]:
  # ... (code to generate list of tuples)
```

Trong ví dụ trên, `columnize` trả về một `list` các `tuple` với các phần tử là `str`.

####  4.6. <a name='GenericMappings'></a>Generic Mappings

Kiểu dữ liệu ánh xạ chung chung được chú thích là `MappingType[KeyType, ValueType]`. `dict` tích hợp và các kiểu dữ liệu ánh xạ trong `collections` và `collections.abc` chấp nhận cú pháp này trong Python 3.9 trở lên. Đối với các phiên bản trước đó, bạn phải sử dụng `typing.Dict` và các kiểu dữ liệu ánh xạ khác từ module `typing`.

**Ví dụ thực tế:**

Ví dụ 8-14 trong sách minh họa việc sử dụng một hàm trả về một chỉ mục đảo ngược (inverted index) để tìm kiếm các ký tự Unicode theo tên. Hàm `name_index` nhận mã ký tự Unicode bắt đầu và kết thúc, trả về một `dict[str, set[str]]`, ánh xạ mỗi từ với một tập hợp các ký tự có từ đó trong tên của chúng.

```python
import sys
import re
import unicodedata
from collections.abc import Iterator

RE_WORD = re.compile(r'\w+')
STOP_CODE = sys.maxunicode + 1

def tokenize(text: str) -> Iterator[str]:
  """return iterable of uppercased words"""
  for match in RE_WORD.finditer(text):
    yield match.group().upper()

def name_index(start: int = 32, end: int = STOP_CODE) -> dict[str, set[str]]:
  index: dict[str, set[str]] = {}
  for char in (chr(i) for i in range(start, end)):
    if name := unicodedata.name(char, ''):
      for word in tokenize(name):
        index.setdefault(word, set()).add(char)
  return index
```

**Giải thích:**

* `tokenize` là một hàm generator.
* Biến cục bộ `index` được chú thích kiểu dữ liệu.
* Toán tử walrus `:=` được sử dụng trong điều kiện `if` để gán kết quả của `unicodedata.name()` cho `name`.

Khi sử dụng `dict` như một bản ghi, thường tất cả các khóa đều có kiểu dữ liệu `str`, với các giá trị có kiểu dữ liệu khác nhau tùy thuộc vào khóa. Trường hợp này sẽ được đề cập trong phần "TypedDict".

####  4.7. <a name='AbstractBaseClasses'></a>Abstract Base Classes

Nguyên tắc chung khi sử dụng ABCs trong type hints:

* **"Be conservative in what you send, be liberal in what you accept"** (Hãy thận trọng trong những gì bạn gửi đi, hãy thoải mái trong những gì bạn chấp nhận) -  **Postel's law**

Nên sử dụng ABCs (ví dụ: `abc.Mapping`, `abc.MutableMapping`) trong chú thích kiểu dữ liệu cho tham số hàm thay vì các kiểu dữ liệu cụ thể (ví dụ: `dict`). Điều này mang lại sự linh hoạt hơn cho người gọi hàm, vì họ có thể truyền vào bất kỳ đối tượng nào là subtype-of của ABC đó.

Ví dụ:

```python
from collections.abc import Mapping

def name2hex(name: str, color_map: Mapping[str, int]) -> str:
  # ...
```

Sử dụng `abc.Mapping` cho phép người gọi truyền vào một instance của `dict`, `defaultdict`, `ChainMap`, một lớp con của `UserDict`, hoặc bất kỳ kiểu dữ liệu nào khác là subtype-of của `Mapping`.

Ngược lại, nếu sử dụng `dict[str, int]`, người gọi sẽ chỉ có thể truyền vào một `dict` hoặc subtype-of của nó.

**Giá trị trả về**

Đối với giá trị trả về của hàm, nên sử dụng kiểu dữ liệu cụ thể. Ví dụ:

```python
def tokenize(text: str) -> list[str]:
  return text.upper().split()
```

**ABCs số học (numeric ABCs)**

Các ABCs số học trong package `numbers` (ví dụ: `Number`, `Complex`, `Real`, `Rational`, `Integral`) không được hỗ trợ cho static type checking. PEP 484 khuyến nghị sử dụng các kiểu dữ liệu tích hợp `complex`, `float` và `int` thay thế.

**Tóm lại:**

Sử dụng ABCs trong type hints giúp tăng tính linh hoạt và khả năng tái sử dụng mã. Tuy nhiên, cần lưu ý rằng các ABCs số học không được hỗ trợ cho static type checking.

####  4.8. <a name='Iterable'></a>Iterable

Tài liệu của `typing.List` khuyến nghị sử dụng `Sequence` và `Iterable` cho type hints của tham số hàm.

`Iterable` là một kiểu dữ liệu trừu tượng (abstract type) đại diện cho bất kỳ đối tượng nào có thể lặp lại (iterable), ví dụ như `list`, `tuple`, `set`, generator, v.v.

**Ví dụ:**

Hàm `math.fsum` trong thư viện chuẩn sử dụng tham số `Iterable`:

```python
from collections.abc import Iterable

def fsum(__seq: Iterable[float]) -> float:
  # ...
```

Hàm `zip_replace` trong ví dụ 8-15 cũng sử dụng tham số `Iterable`:

```python
from collections.abc import Iterable

FromTo = tuple[str, str]  # Type alias

def zip_replace(text: str, changes: Iterable[FromTo]) -> str:
  for from_, to in changes:
    text = text.replace(from_, to)
  return text
```

Trong ví dụ này, `changes` cần là một `Iterable[FromTo]`, tương đương với `Iterable[tuple[str, str]]` nhưng ngắn gọn và dễ đọc hơn.

**`TypeAlias` trong Python 3.10**

Từ Python 3.10, PEP 613 giới thiệu kiểu dữ liệu đặc biệt `TypeAlias` để khai báo type alias rõ ràng hơn:

```python
from typing import TypeAlias

FromTo: TypeAlias = tuple[str, str]
```

**`abc.Iterable` so với `abc.Sequence`**

Cả `math.fsum` và `zip_replace` đều phải lặp qua toàn bộ tham số `Iterable` để trả về kết quả. Nếu truyền vào một iterable vô hạn như generator `itertools.cycle`, các hàm này sẽ tiêu thụ hết bộ nhớ và làm crash chương trình.

Mặt khác, hàm `columnize` trong ví dụ 8-13 cần tham số `Sequence` chứ không phải `Iterable`, vì nó cần lấy `len()` của đầu vào để tính số hàng.

Nên sử dụng `Iterable` làm kiểu dữ liệu cho tham số. Nó quá mơ hồ để làm kiểu dữ liệu trả về.

**`Iterator`**

Kiểu dữ liệu `Iterator` có liên quan chặt chẽ với `Iterable` và được sử dụng làm kiểu dữ liệu trả về trong ví dụ 8-14. Chúng ta sẽ tìm hiểu thêm về `Iterator` trong chương 17, nói về generator và iterator cổ điển.

####  4.9. <a name='ParameterizedGenericsandTypeVar'></a>Parameterized Generics and TypeVar

**Tham số tổng quát (Parameterized Generics)** là một kiểu dữ liệu tổng quát, được viết dưới dạng `list[T]`, trong đó `T` là một **biến kiểu (TypeVar)**. Biến kiểu này sẽ được liên kết với một kiểu dữ liệu cụ thể mỗi khi sử dụng. Điều này cho phép kiểu dữ liệu của tham số được phản ánh trên kiểu dữ liệu của kết quả.

**Ví dụ:**

Hàm `sample` lấy hai tham số: một `Sequence` (chuỗi) các phần tử kiểu `T` và một số nguyên `int`. Nó trả về một `list` (danh sách) các phần tử cùng kiểu `T`, được chọn ngẫu nhiên từ tham số đầu tiên.

```python
from collections.abc import Sequence
from random import shuffle
from typing import TypeVar

T = TypeVar('T')

def sample(population: Sequence[T], size: int) -> list[T]:
  if size < 1:
    raise ValueError('size must be >= 1')
  result = list(population)
  shuffle(result)
  return result[:size]
```

Trong ví dụ này, `T` là một `TypeVar`.

* Nếu gọi hàm với một `tuple` kiểu `tuple[int, ...]`, tương thích với `Sequence[int]`, thì `T` sẽ là `int`, và kiểu dữ liệu trả về là `list[int]`.
* Nếu gọi hàm với một `str`, tương thích với `Sequence[str]`, thì `T` sẽ là `str`, và kiểu dữ liệu trả về là `list[str]`.

**Tại sao cần TypeVar?**

`TypeVar` được sử dụng để khai báo tên của biến kiểu trong Python. Điều này là cần thiết vì Python không tự động nhận biết kiểu dữ liệu như một số ngôn ngữ khác (ví dụ: Java, C#, TypeScript). 

**Ví dụ khác:**

Hàm `statistics.mode` trả về phần tử phổ biến nhất trong một chuỗi. 

```python
>>> mode([1, 1, 2, 3, 3, 3, 3, 4])
3
```

Nếu không sử dụng `TypeVar`, hàm `mode` có thể có chữ ký kiểu như sau:

```python
from collections import Counter
from collections.abc import Iterable

def mode(data: Iterable[float]) -> float:
  pairs = Counter(data).most_common(1)
  if len(pairs) == 0:
    raise ValueError('no mode for empty data')
  return pairs[0][0]
```

Tuy nhiên, việc sử dụng `TypeVar` cho phép hàm `mode` hoạt động với nhiều kiểu dữ liệu số khác nhau, không chỉ `float`.

**Giới hạn TypeVar (Restricted TypeVar)**

`TypeVar` có thể được giới hạn để chỉ chấp nhận một số kiểu dữ liệu cụ thể. Ví dụ:

```python
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar

NumberT = TypeVar('NumberT', float, Decimal, Fraction)

def mode(data: Iterable[NumberT]) -> NumberT:
  # ...
```

Trong ví dụ này, `NumberT` chỉ có thể là `float`, `Decimal` hoặc `Fraction`.

**TypeVar bị ràng buộc (Bounded TypeVar)**

`TypeVar` cũng có thể được ràng buộc với một kiểu dữ liệu "cha". Ví dụ:

```python
from collections import Counter
from collections.abc import Iterable, Hashable
from typing import TypeVar

HashableT = TypeVar('HashableT', bound=Hashable)

def mode(data: Iterable[HashableT]) -> HashableT:
  # ...
```

Trong ví dụ này, `HashableT` có thể là bất kỳ kiểu dữ liệu nào có thể băm (hashable), bao gồm cả các kiểu dữ liệu con của `Hashable`.

**Tóm lại:**

* **Restricted TypeVar:** Giới hạn biến kiểu trong một số kiểu dữ liệu cụ thể.
* **Bounded TypeVar:** Giới hạn biến kiểu là kiểu dữ liệu "cha" hoặc các kiểu dữ liệu con của nó.


**AnyStr**

`AnyStr` là một `TypeVar` được định nghĩa sẵn trong module `typing`, chấp nhận `bytes` hoặc `str`.

####  4.10. <a name='StaticProtocols'></a>Static Protocols

Trong lập trình hướng đối tượng, khái niệm "**protocol**" (giao thức) như một giao diện không chính thức đã có từ lâu đời và là một phần thiết yếu của Python ngay từ đầu. Tuy nhiên, trong ngữ cảnh của gợi ý kiểu, **protocol** là một lớp con của `typing.Protocol` định nghĩa một giao diện mà trình kiểm tra kiểu có thể xác minh.

Kiểu `Protocol`, được giới thiệu trong PEP 544, tương tự như giao diện trong ngôn ngữ Go: một kiểu protocol được định nghĩa bằng cách chỉ định một hoặc nhiều phương thức, và trình kiểm tra kiểu sẽ xác minh rằng các phương thức đó được triển khai ở nơi yêu cầu kiểu protocol đó.

Trong Python, định nghĩa protocol được viết dưới dạng một lớp con của `typing.Protocol`. Tuy nhiên, các lớp triển khai một protocol không cần phải kế thừa, đăng ký hoặc khai báo bất kỳ mối quan hệ nào với lớp định nghĩa protocol. Trình kiểm tra kiểu sẽ tự động tìm các kiểu protocol có sẵn và thực thi việc sử dụng chúng.

**Ví dụ:**

Giả sử bạn muốn tạo một hàm `top(it, n)` trả về `n` phần tử lớn nhất của một `iterable` `it`:

```python
>>> top([4, 1, 5, 2, 6, 7, 3], 3)
[7, 6, 5]
```

Một hàm `top` tổng quát với tham số sẽ trông như thế này:

```python
def top(series: Iterable[T], length: int) -> list[T]:
  ordered = sorted(series, reverse=True)
  return ordered[:length]
```

Vấn đề là làm thế nào để ràng buộc `T`? Nó không thể là `Any` hoặc `object`, vì `series` phải hoạt động với hàm `sorted`. Hàm `sorted` yêu cầu các phần tử trong `series` phải hỗ trợ toán tử `<`.

Để giải quyết vấn đề này, chúng ta có thể tạo một `Protocol` mới:

```python
from typing import Protocol, Any

class SupportsLessThan(Protocol):
  def __lt__(self, other: Any) -> bool: ...
```

Bây giờ, chúng ta có thể định nghĩa hàm `top` sử dụng `TypeVar` với `bound=SupportsLessThan`:

```python
from collections.abc import Iterable
from typing import TypeVar
from comparable import SupportsLessThan

LT = TypeVar('LT', bound=SupportsLessThan)

def top(series: Iterable[LT], length: int) -> list[LT]:
  ordered = sorted(series, reverse=True)
  return ordered[:length]
```

**Static Duck Typing**

`typing.Protocol` cho phép chúng ta thực hiện **static duck typing**. Nghĩa là, kiểu dữ liệu danh nghĩa của `series` không quan trọng, miễn là nó triển khai phương thức `__lt__`. Trình kiểm tra kiểu có thể xác minh điều này mà không cần phải đọc mã nguồn của Python hoặc thực hiện các thử nghiệm.

**Tóm lại:**

* `Static Protocols` cho phép định nghĩa giao diện mà trình kiểm tra kiểu có thể xác minh.
* `typing.Protocol` cho phép thực hiện static duck typing, giúp ràng buộc kiểu dữ liệu dựa trên các phương thức được triển khai.


**Lưu ý:**

Bài viết gốc đề cập đến việc sử dụng `reveal_type()` để kiểm tra kiểu dữ liệu. Đây là một tính năng gỡ lỗi của Mypy và không thể được sử dụng trong thời gian chạy.

####  4.11. <a name='Callable'></a>Callable

`Callable` là một kiểu dữ liệu trong Python được sử dụng để chú thích cho các tham số là hàm callback hoặc các đối tượng có thể gọi được (callable objects) trả về bởi các hàm bậc cao (higher-order functions). 

Kiểu `Callable` được tham số hóa như sau:

```python
Callable[[ParamType1, ParamType2], ReturnType]
```

Trong đó:

* `ParamType1`, `ParamType2`: là các kiểu dữ liệu của tham số của hàm.
* `ReturnType`: là kiểu dữ liệu trả về của hàm.

**Ví dụ:**

```python
def repl(input_fn: Callable[[Any], str] = input) -> None:
  # ...
```

Trong ví dụ này, `input_fn` là một tham số tùy chọn, mặc định là hàm `input` có sẵn trong Python. `Callable[[Any], str]` chỉ ra rằng `input_fn` phải là một hàm nhận một tham số bất kỳ (`Any`) và trả về một chuỗi (`str`).

**Lưu ý:**

* Không có cú pháp để chú thích cho các tham số tùy chọn hoặc tham số từ khóa trong `Callable`.
* Nếu bạn cần một gợi ý kiểu phù hợp với một hàm có chữ ký linh hoạt, hãy thay thế toàn bộ danh sách tham số bằng `...`: `Callable[..., ReturnType]`.

**Phương sai (Variance) trong Callable**

* **Covariant (hiệp biến) trên kiểu trả về:**  Có nghĩa là nếu `A` là kiểu con của `B`, thì `Callable[[], A]` là kiểu con của `Callable[[], B]`.
* **Contravariant (phản biến) trên kiểu tham số:** Có nghĩa là nếu `A` là kiểu con của `B`, thì `Callable[[B], None]` là kiểu con của `Callable[[A], None]`.

**Ví dụ:**

```python
from collections.abc import Callable

def update(
  probe: Callable[[], float],
  display: Callable[[float], None]
) -> None:
  temperature = probe()
  # ...
  display(temperature)

def probe_ok() -> int:
  return 42

def display_wrong(temperature: int) -> None:
  print(hex(temperature))

update(probe_ok, display_wrong)  # Lỗi kiểu

def display_ok(temperature: complex) -> None:
  print(temperature)

update(probe_ok, display_ok)  # Hợp lệ
```

Trong ví dụ này:

* `probe_ok` hợp lệ vì trả về `int` (kiểu con của `float`).
* `display_wrong` không hợp lệ vì nhận tham số `int` mà không thể xử lý `float`.
* `display_ok` hợp lệ vì nhận tham số `complex` (có thể xử lý `float`).

**Tóm lại:**

* `Callable` được sử dụng để chú thích cho các hàm callback hoặc các đối tượng có thể gọi được.
* `Callable` là covariant trên kiểu trả về và contravariant trên kiểu tham số.
* Hầu hết các kiểu dữ liệu tổng quát với tham số là **invariant (bất biến)**, nghĩa là kiểu tham số phải khớp chính xác.


####  4.12. <a name='NoReturn'></a>NoReturn

`NoReturn` là một kiểu đặc biệt trong Python, chỉ được sử dụng để chú thích cho kiểu trả về của các hàm không bao giờ trả về giá trị. Thông thường, các hàm này tồn tại để tạo ra các ngoại lệ (exceptions). Có rất nhiều hàm như vậy trong thư viện chuẩn của Python.

**Ví dụ:**

Hàm `sys.exit()` tạo ra ngoại lệ `SystemExit` để kết thúc chương trình Python. Chữ ký kiểu của hàm này trong typeshed là:

```python
def exit(__status: object = ...) -> NoReturn: ...
```

Trong đó:

* `__status`: là một tham số chỉ định trạng thái thoát, có thể là bất kỳ đối tượng nào (`object`), mặc định là `None`.
* `NoReturn`: chỉ ra rằng hàm này không bao giờ trả về giá trị.

**Ví dụ khác:**

Trong chương 24 của cuốn sách, ví dụ 24-6 sử dụng `NoReturn` để chú thích cho phương thức `__flag_unknown_attrs`. Phương thức này được thiết kế để tạo ra một thông báo lỗi thân thiện với người dùng và toàn diện, sau đó tạo ra ngoại lệ `AttributeError`.

**Tóm lại:**

* `NoReturn` là một kiểu đặc biệt để chú thích cho các hàm không bao giờ trả về giá trị.
* Các hàm được chú thích `NoReturn` thường được sử dụng để tạo ra các ngoại lệ.
* `sys.exit()` là một ví dụ về hàm sử dụng `NoReturn`.

---
###  5. <a name='AnnotatingPositionalOnlyandVariadicParameters'></a>Annotating Positional Only and Variadic Parameters

Trong Python, bạn có thể sử dụng gợi ý kiểu để chú thích cho các tham số chỉ định vị trí (positional-only parameters) và tham số biến đổi (variadic parameters).

**Tham số chỉ định vị trí:**

* **Python ≥ 3.8:** Sử dụng ký hiệu `/` để phân tách các tham số chỉ định vị trí với các tham số khác.
* **Python 3.7 hoặc cũ hơn:** Sử dụng tiền tố `__` (hai dấu gạch dưới) cho tên của các tham số chỉ định vị trí.

**Ví dụ:**

```python
from typing import Optional

# Python ≥ 3.8
def tag(
  name: str,
  /,
  *content: str,
  class_: Optional[str] = None,
  **attrs: str,
) -> str:
  # ...

# Python 3.7 hoặc cũ hơn
def tag(
  __name: str,
  *content: str,
  class_: Optional[str] = None,
  **attrs: str,
) -> str:
  # ...
```

Trong ví dụ này:

* `name`: là tham số chỉ định vị trí, chỉ có thể được truyền bằng vị trí.
* `content`: là tham số biến đổi, có thể nhận một số lượng bất kỳ các tham số vị trí. Kiểu dữ liệu của `content` bên trong hàm sẽ là `tuple[str, ...]`.
* `class_`: là tham số từ khóa tùy chọn, có kiểu dữ liệu là `Optional[str]`.
* `attrs`: là tham số từ khóa biến đổi, có thể nhận một số lượng bất kỳ các tham số từ khóa. Kiểu dữ liệu của `attrs` bên trong hàm sẽ là `dict[str, str]`.

**Lưu ý:**

* Mypy hiểu và thực thi cả hai cách khai báo tham số chỉ định vị trí.
* Nếu tham số `attrs` cần chấp nhận các giá trị thuộc nhiều kiểu dữ liệu khác nhau, bạn cần sử dụng `Union[]` hoặc `Any`: `**attrs: Any`.

**Tóm lại:**

* Gợi ý kiểu có thể được sử dụng để chú thích cho các tham số chỉ định vị trí và tham số biến đổi.
* Python cung cấp hai cách để khai báo tham số chỉ định vị trí: sử dụng ký hiệu `/` (Python ≥ 3.8) hoặc tiền tố `__` (Python 3.7 hoặc cũ hơn).
* Kiểu dữ liệu của tham số biến đổi `content` là `tuple`, và kiểu dữ liệu của tham số từ khóa biến đổi `attrs` là `dict`.

---
###  6. <a name='ImperfectTypingandStrongTesting'></a>Imperfect Typing and Strong Testing

Mặc dù kiểm tra kiểu tĩnh (static type checking) có thể giúp phát hiện nhiều lỗi trong mã nguồn, nhưng nó không phải là giải pháp hoàn hảo. Vẫn tồn tại những hạn chế nhất định khi sử dụng kiểm tra kiểu tĩnh trong Python.

**Những hạn chế của kiểm tra kiểu tĩnh:**

* **Dương tính giả (False positives):** Công cụ báo cáo lỗi kiểu trên mã nguồn chính xác.
* **Âm tính giả (False negatives):** Công cụ không báo cáo lỗi kiểu trên mã nguồn không chính xác.
* **Mất tính linh hoạt:** Một số tính năng hữu ích của Python không thể được kiểm tra kiểu tĩnh, ví dụ như giải nén tham số (`config(**settings)`).
* **Hỗ trợ hạn chế:** Các tính năng nâng cao như thuộc tính (properties), bộ mô tả (descriptors), lớp meta (metaclasses) và lập trình meta (metaprogramming) nói chung được hỗ trợ kém hoặc vượt quá khả năng hiểu biết của trình kiểm tra kiểu.
* **Chậm cập nhật:** Trình kiểm tra kiểu thường chậm hơn so với các bản phát hành Python mới, dẫn đến việc từ chối hoặc thậm chí gặp sự cố khi phân tích mã nguồn sử dụng các tính năng ngôn ngữ mới.
* **Không thể hiện được tất cả các ràng buộc dữ liệu:** Gợi ý kiểu không thể đảm bảo các ràng buộc dữ liệu phức tạp, ví dụ như "số lượng phải là số nguyên > 0" hoặc "nhãn phải là chuỗi có từ 6 đến 12 chữ cái ASCII".

**Kiểm tra mạnh mẽ (Strong Testing)**

Kiểm tra tự động (automated testing) là một phương pháp quan trọng để đảm bảo chất lượng phần mềm. Kiểm tra tự động có thể phát hiện nhiều lỗi mà kiểm tra kiểu tĩnh không thể phát hiện được. Bất kỳ mã nào bạn có thể viết bằng Python, bạn đều có thể kiểm tra bằng Python, dù có sử dụng gợi ý kiểu hay không.

**Kết luận**

Kiểm tra kiểu tĩnh là một công cụ hữu ích, nhưng không nên coi đó là giải pháp duy nhất để đảm bảo chất lượng phần mềm. Kiểm tra tự động vẫn đóng vai trò quan trọng trong việc phát hiện và sửa lỗi.

**Tóm lại:**

* Kiểm tra kiểu tĩnh có những hạn chế nhất định.
* Kiểm tra tự động vẫn là một phương pháp quan trọng để đảm bảo chất lượng phần mềm.
* Nên kết hợp kiểm tra kiểu tĩnh và kiểm tra tự động để đạt hiệu quả tốt nhất.
