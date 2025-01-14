---
layout: post
title: "[Fluent python] Chapter 5. Data class Builders"
date: 2025-01-13 09:00:00 +0700
categories: fluent python
---

Python cung cấp một số cách để xây dựng một `class` đơn giản chỉ là tập hợp các trường dữ liệu (`fields`), với ít hoặc không có chức năng bổ sung. Mô hình đó được gọi là " `data class` " - và `data classes` là một trong những package hỗ trợ mô hình này. Chương này đề cập đến ba trình xây dựng `class` khác nhau mà bạn có thể sử dụng làm lối tắt để viết `data class`:

`collections.namedtuple`
Cách đơn giản nhất - có sẵn từ Python 2.6.

`typing.NamedTuple`
Một lựa chọn thay thế yêu cầu `type hints` trên các trường - kể từ Python 3.5, với cú pháp `class` được thêm vào trong 3.6.

`@dataclasses.dataclass`
Một `class decorator` cho phép tùy chỉnh nhiều hơn so với các lựa chọn thay thế trước đó, thêm nhiều tùy chọn và khả năng phức tạp - kể từ Python 3.7.

Sau khi đề cập đến các trình xây dựng `class` đó, chúng ta sẽ thảo luận về lý do tại sao `Data Class` cũng là tên của một `code smell`: một mô hình mã hóa có thể là triệu chứng của thiết kế hướng đối tượng kém.

> `typing.TypedDict` có vẻ giống như một trình xây dựng `data class` khác. Nó sử dụng cú pháp tương tự và được mô tả ngay sau `typing.NamedTuple` trong tài liệu mô-đun `typing` cho Python 3.9.
Tuy nhiên, `TypedDict` không xây dựng các `class` cụ thể mà bạn có thể khởi tạo. Nó chỉ là cú pháp để viết `type hints` cho các tham số hàm và các biến sẽ chấp nhận các giá trị ánh xạ được sử dụng làm bản ghi, với các key là tên trường. Chúng ta sẽ thấy chúng trong Chương 15,
"`TypedDict`" trên trang 526.

### Table of contents

1. [Overview of Data Class Builders](#OverviewofDataClassBuilders)
  * 1.1. [Main Features](#MainFeatures)
2. [Classic Named Tuples](#ClassicNamedTuples)
3. [Typed Named Tuples](#TypedNamedTuples)
4. [Type Hints 101](#TypeHints101)
  * 4.1. [No Runtime Effect](#NoRuntimeEffect)
  * 4.2. [Variable Annotation Syntax](#VariableAnnotationSyntax)
  * 4.3. [The Meaning of Variable Annotations](#TheMeaningofVariableAnnotations)
5. [More About @dataclass](#MoreAboutdataclass)
  * 5.1. [Field Options](#FieldOptions)
  * 5.2. [Post-init Processing](#Post-initProcessing)
  * 5.3. [Typed Class Attributes](#TypedClassAttributes)
  * 5.4. [Initialization Variables That Are Not Fields](#InitializationVariablesThatAreNotFields)
  * 5.5. [@dataclass Example: Dublin Core Resource Record](#dataclassExample:DublinCoreResourceRecord)
6. [Data Class as a Code Smell](#DataClassasaCodeSmell)
  * 6.1. [Data Class as Scaffolding](#DataClassasScaffolding)
  * 6.2. [Data Class as Intermediate Representation](#DataClassasIntermediateRepresentation)
7. [Pattern Matching Class Instances](#PatternMatchingClassInstances)
  * 7.1. [Simple Class Patterns](#SimpleClassPatterns)
  * 7.2. [Keyword Class Patterns](#KeywordClassPatterns)
  * 7.3. [Positional Class Patterns](#PositionalClassPatterns)


###  1. <a name='OverviewofDataClassBuilders'></a>Overview of Data Class Builders

Các class đơn giản chủ yếu để lưu trữ dữ liệu. có 3 cách:

1. **`namedtuple`**: Cách cổ điển và đơn giản nhất, coi data class như một tuple đặc biệt.
2. **`typing.NamedTuple`**: Giống `namedtuple` nhưng cho phép chỉ định kiểu dữ liệu cho từng trường, giúp code rõ ràng và ít lỗi hơn.
3. **`@dataclass`**: Cách hiện đại và linh hoạt nhất, dùng decorator để tự động tạo ra các phương thức cần thiết cho data class.

Ví dụ về data class là class `Coordinate` để lưu tọa độ, với hai trường `lat` (vĩ độ) và `lon` (kinh độ).  

####  1.1. <a name='MainFeatures'></a>Main Features

![]({{site.url}}/images/data-class-main-feature.png)


**1. Mutable instances (Các trường hợp có thể thay đổi)**

* **Tưởng tượng:** Bạn có một hộp bút chì màu. 
    * `namedtuple` và `typing.NamedTuple` giống như hộp bút chì màu được dán kín. Sau khi cho bút chì vào, bạn không thể thay đổi số lượng hay màu sắc bút chì bên trong.
    * `@dataclass` giống như hộp bút chì màu bình thường. Bạn có thể thêm, bớt hoặc thay đổi bút chì bên trong bất cứ lúc nào.
* **Ví dụ:**

```python
from collections import namedtuple
from dataclasses import dataclass

# namedtuple - immutable (bất biến)
Point = namedtuple('Point', ['x', 'y'])
p1 = Point(1, 2)
# p1.x = 3  # Lỗi: không thể thay đổi giá trị của x

# @dataclass - mutable (có thể thay đổi)
@dataclass
class Point2:
    x: int
    y: int

p2 = Point2(1, 2)
p2.x = 3  # OK: có thể thay đổi giá trị của x
```

**2. Class statement syntax (Cú pháp câu lệnh lớp)**

* **Tưởng tượng:** Bạn muốn tạo ra một "khuôn mẫu" để làm bánh quy.
    * `typing.NamedTuple` và `@dataclass` cho phép bạn sử dụng cách viết giống như tạo khuôn bánh thông thường, dễ dàng thêm ghi chú về nguyên liệu, cách làm, v.v.
    * `collections.namedtuple` giống như bạn phải tạo khuôn bánh theo một cách đặc biệt, ít linh hoạt hơn.
* **Ví dụ:**

```python
from typing import NamedTuple
from dataclasses import dataclass

# typing.NamedTuple
class Car(NamedTuple):
    """
    Lớp đại diện cho một chiếc xe hơi.
    """
    brand: str
    model: str
    year: int

# @dataclass
@dataclass
class Car2:
    """
    Lớp đại diện cho một chiếc xe hơi.
    """
    brand: str
    model: str
    year: int

    def get_full_name(self):
        return f"{self.year} {self.brand} {self.model}"
```

**3. Construct dict (Xây dựng dict)**

* **Tưởng tượng:** Bạn có một danh sách các món đồ chơi và muốn chuyển chúng thành một "bảng danh sách" với tên đồ chơi và số lượng.
    * Cả ba trình tạo lớp đều có cách để làm điều này, chỉ khác nhau về cách gọi hàm.
* **Ví dụ:**

```python
from collections import namedtuple
from typing import NamedTuple
from dataclasses import dataclass, asdict

# namedtuple
Toy = namedtuple('Toy', ['name', 'quantity'])
toy1 = Toy('Xe hơi', 2)
toy1_dict = toy1._asdict()

# typing.NamedTuple
class Toy2(NamedTuple):
    name: str
    quantity: int

toy2 = Toy2('Búp bê', 3)
toy2_dict = toy2._asdict()

# @dataclass
@dataclass
class Toy3:
    name: str
    quantity: int

toy3 = Toy3('Gấu bông', 1)
toy3_dict = asdict(toy3)
```

**4. Get field names and default values (Lấy tên trường và giá trị mặc định)**

* **Tưởng tượng:** Bạn muốn biết danh sách các nguyên liệu và lượng nguyên liệu mặc định để làm bánh theo công thức.
    * Cả ba trình tạo lớp đều cho phép bạn xem danh sách nguyên liệu (tên trường) và lượng mặc định (giá trị mặc định).
* **Ví dụ:**

```python
from collections import namedtuple
from typing import NamedTuple
from dataclasses import dataclass, fields

# namedtuple
Recipe = namedtuple('Recipe', ['flour', 'sugar', 'eggs'], defaults=(200, 100, 2))
print(Recipe._fields)  # ('flour', 'sugar', 'eggs')
print(Recipe._field_defaults)  # {'eggs': 2, 'sugar': 100, 'flour': 200}

# typing.NamedTuple
class Recipe2(NamedTuple):
    flour: int = 200
    sugar: int = 100
    eggs: int = 2

# @dataclass
@dataclass
class Recipe3:
    flour: int = 200
    sugar: int = 100
    eggs: int = 2

recipe3_fields = fields(Recipe3)
for field in recipe3_fields:
    print(f"{field.name}: {field.default}")
```

**5. Get field types (Lấy kiểu trường)**

* **Tưởng tượng:** Bạn muốn biết mỗi nguyên liệu trong công thức là loại gì (bột mì, đường, trứng).
    * `typing.NamedTuple` và `@dataclass` cho phép bạn xem loại của mỗi trường (ví dụ: `int`, `str`).
* **Ví dụ:**

```python
from typing import NamedTuple, get_type_hints
from dataclasses import dataclass

# typing.NamedTuple
class Recipe(NamedTuple):
    flour: int
    sugar: int
    eggs: int

print(get_type_hints(Recipe))  # {'flour': <class 'int'>, 'sugar': <class 'int'>, 'eggs': <class 'int'>}

# @dataclass
@dataclass
class Recipe2:
    flour: int
    sugar: int
    eggs: int

print(get_type_hints(Recipe2))  # {'flour': <class 'int'>, 'sugar': <class 'int'>, 'eggs': <class 'int'>}
```

**6. New instance with changes (Trường hợp mới với các thay đổi)**

* **Tưởng tượng:** Bạn muốn tạo một bản sao của hộp bút chì màu, nhưng thay đổi một số màu bút chì.
    * Cả ba trình tạo lớp đều cho phép bạn tạo một hộp bút chì mới với các thay đổi mong muốn mà không làm ảnh hưởng đến hộp bút chì ban đầu.
* **Ví dụ:**

```python
from collections import namedtuple
from typing import NamedTuple
from dataclasses import dataclass, replace

# namedtuple
Point = namedtuple('Point', ['x', 'y'])
p1 = Point(1, 2)
p2 = p1._replace(x=3)

# typing.NamedTuple
class Point2(NamedTuple):
    x: int
    y: int

p3 = Point2(1, 2)
# p4 = p3._replace(x=3)  # Lỗi: typing.NamedTuple không có _replace

# @dataclass
@dataclass
class Point3:
    x: int
    y: int

p5 = Point3(1, 2)
p6 = replace(p5, x=3)
```

**7. New class at runtime (Lớp mới trong thời gian chạy)**

* **Tưởng tượng:** Bạn muốn tạo ra một loại bánh quy mới với các nguyên liệu và cách làm khác nhau, ngay trong khi đang làm bánh.
    * `collections.namedtuple`, `typing.NamedTuple` và `dataclasses` đều cho phép bạn tạo "khuôn mẫu" bánh quy mới ngay trong lúc làm bánh.
* **Ví dụ:**

```python
from collections import namedtuple
from typing import NamedTuple
from dataclasses import make_dataclass

# collections.namedtuple
NewRecipe = namedtuple('NewRecipe', ['flour', 'chocolate'])

# typing.NamedTuple
NewRecipe2 = NamedTuple('NewRecipe2', [('flour', int), ('chocolate', int)])

# dataclasses.make_dataclass
NewRecipe3 = make_dataclass('NewRecipe3', [('flour', int), ('chocolate', int)])
```
---

###  2. <a name='ClassicNamedTuples'></a>Classic Named Tuples

**`collections.namedtuple` là gì?**

Tưởng tượng `namedtuple` như một công cụ để tạo ra các loại "hộp đựng đồ" đặc biệt. Mỗi "hộp" này có:

* **Tên:**  Giống như nhãn dán trên hộp, giúp bạn phân biệt các loại hộp khác nhau.
* **Các ngăn:** Mỗi ngăn có một tên riêng, giúp bạn sắp xếp đồ đạc gọn gàng và dễ tìm kiếm.

Ví dụ, bạn có thể tạo một "hộp" tên là `SinhVien` với các ngăn "ho_ten", "tuoi", "diem".

**Ưu điểm của `namedtuple`:**

* **Dễ đọc:** Thay vì truy cập các phần tử bằng chỉ số như tuple thông thường (ví dụ `sinh_vien[0]`), bạn có thể dùng tên (`sinh_vien.ho_ten`). Code của bạn sẽ dễ hiểu hơn rất nhiều.
* **Tiện lợi:** `namedtuple` kế thừa tất cả các tính năng của `tuple` nên bạn có thể sử dụng các phương thức như `len()`, `sorted()`, ...
* **Nhẹ nhàng:** `namedtuple` không chiếm nhiều bộ nhớ như class.

**Ví dụ minh họa:**

```python
from collections import namedtuple

# Tạo "khuôn mẫu" cho hộp SinhVien
SinhVien = namedtuple('SinhVien', ['ho_ten', 'tuoi', 'diem'])

# Tạo "hộp" sv1 và "hộp" sv2
sv1 = SinhVien('Nguyen Van A', 20, 8.5)
sv2 = SinhVien('Tran Thi B', 21, 9.0)

# Truy cập thông tin bằng tên
print(f"{sv1.ho_ten} - {sv1.tuoi} tuổi - điểm: {sv1.diem}")
# Output: Nguyen Van A - 20 tuổi - điểm: 8.5

print(f"{sv2.ho_ten} - {sv2.tuoi} tuổi - điểm: {sv2.diem}")
# Output: Tran Thi B - 21 tuổi - điểm: 9.0

# Chuyển đổi "hộp" thành từ điển
sv1_dict = sv1._asdict()
print(sv1_dict)
# Output: {'ho_ten': 'Nguyen Van A', 'tuoi': 20, 'diem': 8.5}
```

Trong ví dụ trên, `SinhVien` là tên của "khuôn mẫu", `ho_ten`, `tuoi`, `diem` là tên các "ngăn".

**Lưu ý:**

* `namedtuple` tạo ra các "hộp" **bất biến (immutable)**, nghĩa là bạn không thể thay đổi nội dung sau khi đã tạo.
* Nếu cần các "hộp" có thể thay đổi, bạn nên sử dụng `@dataclass`.

---
###  3. <a name='TypedNamedTuples'></a>Typed Named Tuples

**`typing.NamedTuple` là gì?**

Nói một cách đơn giản, `typing.NamedTuple` giúp bạn tạo ra các tuple (bộ dữ liệu) mà mỗi phần tử trong đó có tên gọi riêng, giống như các trường (field) trong một class vậy. Điều này giúp code của bạn dễ đọc và dễ hiểu hơn rất nhiều.

**Ví dụ:**

Giả sử bạn cần lưu trữ thông tin về một sinh viên, bao gồm tên, tuổi và điểm trung bình. Bạn có thể dùng tuple thông thường:

```python
sinh_vien = ("An", 20, 8.5)
```

Nhưng khi nhìn vào tuple này, bạn không biết rõ số 20 và 8.5 đại diện cho gì. Với `typing.NamedTuple`, bạn có thể làm rõ ràng hơn:

```python
from typing import NamedTuple

class SinhVien(NamedTuple):
  ten: str
  tuoi: int
  diem: float

sinh_vien = SinhVien("An", 20, 8.5)
```

Bây giờ, bạn có thể truy cập thông tin sinh viên bằng tên:

```python
print(sinh_vien.ten)  # Output: An
print(sinh_vien.tuoi) # Output: 20
print(sinh_vien.diem) # Output: 8.5
```

**So sánh với `collections.namedtuple`:**

Trước đây, Python có `collections.namedtuple` để tạo tuple có tên. `typing.NamedTuple` tương tự, nhưng có thêm một lợi ích quan trọng: **chú thích kiểu dữ liệu (type annotations)**. 

Trong ví dụ trên, `ten: str` nghĩa là trường `ten` phải là chuỗi, `tuoi: int` nghĩa là trường `tuoi` phải là số nguyên, v.v. Việc này giúp bạn:

* **Phát hiện lỗi sớm:** Nếu bạn gán nhầm kiểu dữ liệu cho một trường, Python sẽ cảnh báo bạn.
* **Tăng khả năng đọc code:** Nhìn vào định nghĩa `SinhVien`, bạn biết ngay mỗi trường có kiểu dữ liệu gì.
* **Hỗ trợ các công cụ lập trình:** Các IDE và công cụ kiểm tra code có thể sử dụng type annotations để phân tích code và đưa ra gợi ý tốt hơn.

**Tóm lại:**

`typing.NamedTuple` là một cách tuyệt vời để tạo ra các tuple có tên và chú thích kiểu dữ liệu, giúp code của bạn rõ ràng, dễ đọc và ít lỗi hơn.

**Lưu ý:**

* `typing.NamedTuple` tạo ra các tuple **bất biến (immutable)**, nghĩa là bạn không thể thay đổi giá trị của các trường sau khi tạo.
* `typing.NamedTuple` có đầy đủ các phương thức của tuple thông thường, chẳng hạn như `len()`, `index()`, v.v.

---
###  4. <a name='TypeHints101'></a>Type Hints 101

**Type Hints là gì?**

Type Hints (còn gọi là Type Annotations) là một cách để bạn "gợi ý" cho Python về kiểu dữ liệu của các biến, tham số hàm, và giá trị trả về. 

**Ví dụ:**

```python
def chao_mung(ten: str) -> str:
  """Hàm này nhận vào tên và trả về lời chào."""
  return "Xin chào, " + ten + "!"
```

Trong ví dụ này:

* `ten: str`  nghĩa là tham số `ten`  mong đợi một giá trị kiểu chuỗi (`str`).
* `-> str` nghĩa là hàm `chao_mung` sẽ trả về một giá trị kiểu chuỗi (`str`).

**Tại sao cần Type Hints?**

Tuy Python không bắt buộc dùng Type Hints, nhưng chúng mang lại nhiều lợi ích:

* **Dễ đọc code hơn:** Nhìn vào khai báo hàm, bạn biết ngay tham số và giá trị trả về có kiểu gì.
* **Phát hiện lỗi sớm:**  Các công cụ như MyPy có thể kiểm tra Type Hints và cảnh báo bạn nếu có lỗi kiểu dữ liệu, giúp bạn tránh được lỗi khi chạy chương trình.
* **Hỗ trợ IDE:** Các IDE (như VS Code, PyCharm) sử dụng Type Hints để đưa ra gợi ý code, tự động hoàn thành, và phát hiện lỗi chính tả.
* **Nâng cao chất lượng code:**  Type Hints khuyến khích bạn suy nghĩ kỹ hơn về kiểu dữ liệu, giúp code rõ ràng và dễ bảo trì hơn.

**Type Hints không phải là ép kiểu:**

Lưu ý quan trọng là Type Hints chỉ là gợi ý, không phải ép kiểu. Python vẫn là ngôn ngữ động, nghĩa là bạn có thể truyền kiểu dữ liệu khác với Type Hints mà chương trình vẫn chạy. Tuy nhiên, điều này có thể gây ra lỗi logic khó phát hiện.

**Ví dụ về lỗi:**

```python
def tinh_tong(a: int, b: int) -> int:
  return a + b

ket_qua = tinh_tong(5, "10")  # Truyền chuỗi "10" thay vì số 10
print(ket_qua)  # Lỗi: TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Tóm lại:**

Type Hints là một tính năng hữu ích giúp code Python của bạn rõ ràng, dễ đọc và ít lỗi hơn. Khuyến khích bạn sử dụng Type Hints trong các dự án của mình.

####  4.1. <a name='NoRuntimeEffect'></a>No Runtime Effect

**Type Hints chỉ là "gợi ý"**:

Hãy tưởng tượng Type Hints giống như những "lời khuyên" bạn đưa ra cho Python. Python sẽ "lắng nghe" lời khuyên này, nhưng không "bắt buộc" phải làm theo. 

Cụ thể hơn, khi bạn khai báo Type Hints, Python sẽ không kiểm tra xem kiểu dữ liệu bạn truyền vào có đúng với Type Hints hay không. Điều này có nghĩa là ngay cả khi bạn truyền sai kiểu dữ liệu, chương trình vẫn có thể chạy được.

**Ví dụ:**

```python
def tinh_tong(a: int, b: int) -> int:
  """Hàm này nhận vào hai số nguyên và trả về tổng của chúng."""
  return a + b

ket_qua = tinh_tong(5, "10")  # Truyền chuỗi "10" thay vì số 10
print(ket_qua)  # Kết quả: 510 (Python tự động nối chuỗi)
```

Trong ví dụ này, mặc dù Type Hints chỉ ra rằng `a` và `b` phải là số nguyên (`int`), nhưng khi ta truyền chuỗi `"10"` vào cho `b`, Python vẫn chấp nhận và thực hiện phép cộng chuỗi thay vì phép cộng số học.

**Tại sao Python lại làm vậy?**

Lý do chính là vì Python là một ngôn ngữ **động (dynamically typed)**.  Điều này có nghĩa là kiểu dữ liệu của một biến được xác định trong thời gian chạy, chứ không phải khi biên dịch.  

Ưu điểm của việc này là code Python rất linh hoạt, bạn có thể thay đổi kiểu dữ liệu của biến một cách dễ dàng. Tuy nhiên, nhược điểm là dễ mắc phải lỗi kiểu dữ liệu nếu không cẩn thận.

**Vậy Type Hints có tác dụng gì?**

Tuy không có hiệu lực trong thời gian chạy, Type Hints vẫn rất hữu ích vì:

* **Tăng khả năng đọc code**: Giúp bạn hiểu rõ hơn về kiểu dữ liệu của các biến và hàm.
* **Phát hiện lỗi sớm**: Các công cụ kiểm tra kiểu dữ liệu tĩnh (như MyPy) có thể sử dụng Type Hints để phân tích code và tìm ra lỗi kiểu dữ liệu trước khi bạn chạy chương trình.
* **Hỗ trợ IDE**:  IDE có thể sử dụng Type Hints để đưa ra gợi ý code, tự động hoàn thành, và phát hiện lỗi chính tả.

**Tóm lại**:

Type Hints trong Python giống như những "lời khuyên" hữu ích, giúp bạn viết code rõ ràng, dễ đọc và ít lỗi hơn. Tuy nhiên, chúng không có hiệu lực trong thời gian chạy, vì vậy bạn vẫn cần cẩn thận khi làm việc với kiểu dữ liệu trong Python.

####  4.2. <a name='VariableAnnotationSyntax'></a>Variable Annotation Syntax

**Variable annotation là gì?**

Nói đơn giản, variable annotation là cách bạn "gắn nhãn" cho một biến để chỉ rõ kiểu dữ liệu mà biến đó sẽ chứa. 

**Cú pháp:**

Cú pháp của variable annotation rất đơn giản:

```python
tên_biến: kiểu_dữ_liệu
```

Ví dụ:

```python
tuoi: int = 20
ten: str = "An"
diem: float = 8.5
```

Trong ví dụ này:

* `tuoi: int` nghĩa là biến `tuoi` sẽ chứa giá trị kiểu số nguyên (`int`).
* `ten: str` nghĩa là biến `ten` sẽ chứa giá trị kiểu chuỗi (`str`).
* `diem: float` nghĩa là biến `diem` sẽ chứa giá trị kiểu số thực (`float`).

**Lợi ích của variable annotation:**

* **Tăng khả năng đọc code**: Nhìn vào khai báo biến, bạn biết ngay biến đó có kiểu dữ liệu gì.
* **Phát hiện lỗi sớm**: Các công cụ kiểm tra kiểu dữ liệu tĩnh (như MyPy) có thể sử dụng variable annotation để phân tích code và tìm ra lỗi kiểu dữ liệu trước khi bạn chạy chương trình.
* **Hỗ trợ IDE**:  IDE có thể sử dụng variable annotation để đưa ra gợi ý code, tự động hoàn thành, và phát hiện lỗi chính tả.

**Variable annotation trong `typing.NamedTuple` và `@dataclass`:**

Variable annotation được sử dụng rộng rãi trong `typing.NamedTuple` và `@dataclass` để định nghĩa kiểu dữ liệu cho các trường (field) của tuple và data class.

Ví dụ với `typing.NamedTuple`:

```python
from typing import NamedTuple

class SinhVien(NamedTuple):
  ten: str
  tuoi: int
  diem: float
```

Ví dụ với `@dataclass`:

```python
from dataclasses import dataclass

@dataclass
class SinhVien:
  ten: str
  tuoi: int
  diem: float
```

Trong cả hai ví dụ trên, variable annotation được sử dụng để chỉ rõ kiểu dữ liệu cho các trường `ten`, `tuoi`, và `diem`.

**Lưu ý:**

* Variable annotation chỉ là "gợi ý", không phải ép kiểu. Python vẫn là ngôn ngữ động, nghĩa là bạn có thể gán giá trị có kiểu dữ liệu khác với variable annotation mà chương trình vẫn chạy.
* Để tận dụng hết lợi ích của variable annotation, bạn nên sử dụng các công cụ kiểm tra kiểu dữ liệu tĩnh (như MyPy) hoặc IDE hỗ trợ type hints.


####  4.3. <a name='TheMeaningofVariableAnnotations'></a>The Meaning of Variable Annotations

**Type hints không chỉ là comment:**

Mặc dù `type hints` không ảnh hưởng đến hoạt động của chương trình khi chạy, nhưng chúng không chỉ đơn thuần là comment. Khi Python "đọc" code của bạn, nó sẽ thu thập các `type hints` và lưu chúng vào một thuộc tính đặc biệt tên là `__annotations__`.

**`__annotations__` là gì?**

`__annotations__` là một dictionary (từ điển) lưu trữ thông tin về kiểu dữ liệu của các biến, tham số hàm, và giá trị trả về trong code của bạn.

Ví dụ:

```python
def chao_mung(ten: str) -> str:
  """Hàm này nhận vào tên và trả về lời chào."""
  return "Xin chào, " + ten + "!"

print(chao_mung.__annotations__)
# Output: {'ten': <class 'str'>, 'return': <class 'str'>}
```

Như bạn thấy, `__annotations__` của hàm `chao_mung` chứa thông tin về kiểu dữ liệu của tham số `ten` (kiểu `str`) và giá trị trả về (kiểu `str`).

**`typing.NamedTuple` và `@dataclass` sử dụng `__annotations__` như thế nào?**

`typing.NamedTuple` và `@dataclass` sử dụng `__annotations__` để tạo ra các thuộc tính cho tuple và data class một cách tự động.

Ví dụ với `typing.NamedTuple`:

```python
from typing import NamedTuple

class SinhVien(NamedTuple):
  ten: str
  tuoi: int
  diem: float

sinh_vien = SinhVien("An", 20, 8.5)
print(sinh_vien.ten)  # Output: An
```

Trong ví dụ này, `typing.NamedTuple` sử dụng `type hints` (`ten: str`, `tuoi: int`, `diem: float`) để tạo ra các thuộc tính `ten`, `tuoi`, và `diem` cho tuple `SinhVien`.

Tương tự với `@dataclass`:

```python
from dataclasses import dataclass

@dataclass
class SinhVien:
  ten: str
  tuoi: int
  diem: float

sinh_vien = SinhVien("An", 20, 8.5)
print(sinh_vien.ten)  # Output: An
```

**Tóm lại:**

`Type hints` trong Python không chỉ là comment. Chúng được Python sử dụng để tạo ra `__annotations__`, từ đó `typing.NamedTuple` và `@dataclass` có thể sử dụng để tạo ra các thuộc tính cho tuple và data class một cách tự động.

---
###  5. <a name='MoreAboutdataclass'></a>More About @dataclass

Cho đến nay, chúng ta mới chỉ thấy các ví dụ đơn giản về cách sử dụng `@dataclass`. Trình trang trí này chấp nhận một số `keyword arguments`. Đây là chữ ký của nó:

```python
@dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
```

Dấu `*` ở vị trí đầu tiên có nghĩa là các tham số còn lại chỉ là `keyword-only`. Bảng 5-2 mô tả chúng.

![]({{site.url}}/images/data-class.png)

Các giá trị mặc định thực sự là các cài đặt hữu ích nhất cho các trường hợp sử dụng phổ biến. Các tùy chọn bạn có nhiều khả năng thay đổi so với mặc định là:

* `frozen=True`: Bảo vệ chống lại các thay đổi ngẫu nhiên đối với các `instance` của lớp.
* `order=True`: Cho phép sắp xếp các `instance` của `data class`.

Do tính chất động của các đối tượng Python, một lập trình viên tò mò không quá khó để vượt qua sự bảo vệ do `frozen=True` cung cấp. Nhưng các thủ thuật cần thiết sẽ dễ dàng bị phát hiện trong quá trình xem xét code.

Nếu cả hai `argument` `eq` và `frozen` đều là `True`, `@dataclass` sẽ tạo ra một phương thức `__hash__` phù hợp, do đó các `instance` sẽ có thể băm được. `__hash__` được tạo sẽ sử dụng dữ liệu từ tất cả các trường không bị loại trừ riêng lẻ bằng cách sử dụng tùy chọn trường mà chúng ta sẽ thấy trong "Tùy chọn Trường" ở trang 180. Nếu `frozen=False` (mặc định), `@dataclass` sẽ đặt `__hash__` thành `None`, báo hiệu rằng các `instance` không thể băm được, do đó ghi đè `__hash__` từ bất kỳ lớp cha nào.

PEP 557 - Data Classes có điều này để nói về `unsafe_hash`:

> Mặc dù không được khuyến khích, bạn có thể buộc Data Classes tạo phương thức `__hash__` với `unsafe_hash=True`. Đây có thể là trường hợp nếu lớp của bạn về mặt logic là bất biến nhưng vẫn có thể bị thay đổi. Đây là một trường hợp sử dụng chuyên biệt và cần được xem xét cẩn thận.

Tôi sẽ để `unsafe_hash` ở đó. Nếu bạn cảm thấy mình phải sử dụng tùy chọn đó, hãy kiểm tra tài liệu `dataclasses.dataclass`.

Việc tùy chỉnh thêm `data class` được tạo có thể được thực hiện ở cấp độ trường.


####  5.1. <a name='FieldOptions'></a>Field Options

Trong Python, khi định nghĩa một lớp (class) với `@dataclass`, bạn có thể sử dụng `default_factory` để chỉ định cách tạo giá trị mặc định cho một thuộc tính (attribute) của lớp. Điều này đặc biệt hữu ích khi giá trị mặc định là một đối tượng có thể thay đổi (mutable) như list, dict, hoặc set.

**Tại sao cần `default_factory`?**

Nếu bạn gán trực tiếp một giá trị mặc định có thể thay đổi cho thuộc tính, tất cả các instance của lớp sẽ chia sẻ cùng một đối tượng đó. Điều này có thể dẫn đến lỗi khó phát hiện, vì việc thay đổi thuộc tính ở một instance sẽ ảnh hưởng đến tất cả các instance khác.

Ví dụ, hãy xem xét lớp `ClubMember` sau:

```python
@dataclass
class ClubMember:
    name: str
    guests: list = []  # Sai!
```

Trong ví dụ này, tất cả các instance của `ClubMember` sẽ chia sẻ cùng một danh sách `guests`. Nếu bạn thêm một khách vào danh sách `guests` của một thành viên, danh sách `guests` của tất cả các thành viên khác cũng sẽ bị thay đổi.

**Cách sử dụng `default_factory`**

Để tránh vấn đề này, bạn có thể sử dụng `default_factory` để chỉ định một hàm (hoặc bất kỳ đối tượng nào có thể gọi được) sẽ được gọi để tạo giá trị mặc định mỗi khi một instance mới được tạo.

Ví dụ, đây là cách bạn có thể sửa lớp `ClubMember`:

```python
from dataclasses import dataclass, field

@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list)  # Đúng!
```

Trong ví dụ này, `default_factory=list` chỉ định rằng mỗi khi một instance `ClubMember` mới được tạo, một danh sách rỗng mới sẽ được tạo bằng cách gọi `list()`. Điều này đảm bảo rằng mỗi thành viên có danh sách khách riêng của họ.

**Ví dụ minh họa**

```python
from dataclasses import dataclass, field

@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list)

john = ClubMember("John Doe")
jane = ClubMember("Jane Doe")

john.guests.append("Peter Pan")

print(john)  # Output: ClubMember(name='John Doe', guests=['Peter Pan'])
print(jane)  # Output: ClubMember(name='Jane Doe', guests=[])
```

Như bạn thấy, việc thêm "Peter Pan" vào danh sách khách của `john` không ảnh hưởng đến danh sách khách của `jane`.

**Tóm lại**

`default_factory` là một công cụ hữu ích để tránh các lỗi tiềm ẩn khi làm việc với các giá trị mặc định có thể thay đổi trong `dataclass`. Bằng cách sử dụng `default_factory`, bạn đảm bảo rằng mỗi instance của lớp có giá trị mặc định riêng của nó, ngăn chặn các thay đổi không mong muốn ảnh hưởng đến các instance khác.


####  5.2. <a name='Post-initProcessing'></a>Post-init Processing

Phương thức `__post_init__` trong `dataclass` của Python cho phép bạn thực hiện các hành động bổ sung sau khi instance của lớp dữ liệu đã được khởi tạo bởi hàm `__init__` được tạo tự động. Nói cách khác, nó cho phép bạn tùy chỉnh thêm quá trình khởi tạo đối tượng.

**Khi nào cần sử dụng `__post_init__`?**

* **Xác thực dữ liệu (Validation):** Kiểm tra xem các giá trị được gán cho các thuộc tính có hợp lệ hay không. Ví dụ, bạn có thể kiểm tra xem một số nguyên có dương hay không, hoặc một chuỗi có phải là địa chỉ email hợp lệ hay không.
* **Tính toán giá trị thuộc tính:** Tính toán giá trị của một thuộc tính dựa trên các thuộc tính khác. Ví dụ, bạn có thể tính toán tuổi của một người dựa trên ngày sinh của họ.
* **Khởi tạo các thuộc tính không phải là trường:**  Khởi tạo các thuộc tính không được khai báo là trường (field) trong `dataclass`.
* **Thực hiện các tác vụ phụ thuộc:** Thực hiện các tác vụ phụ thuộc vào trạng thái của đối tượng sau khi các thuộc tính đã được khởi tạo.

**Ví dụ minh họa**

Hãy xem xét một ví dụ về lớp `Person` với các thuộc tính `name` (tên) và `age` (tuổi). Chúng ta muốn đảm bảo rằng `age` luôn không âm và tính toán thêm thuộc tính `birth_year` (năm sinh) dựa trên `age`.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Person:
    name: str
    age: int
    birth_year: int = field(init=False)  # Không khởi tạo trong __init__

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Tuổi không được âm")
        self.birth_year = datetime.now().year - self.age

person = Person("John Doe", 30)
print(person)  # Output: Person(name='John Doe', age=30, birth_year=1995)
```

Trong ví dụ này:

* `__post_init__` kiểm tra xem `age` có âm hay không. Nếu có, nó sẽ tạo ra một `ValueError`.
* `birth_year` được tính toán trong `__post_init__` dựa trên `age` hiện tại và năm hiện tại.
* `field(init=False)` được sử dụng để ngăn `birth_year` được khởi tạo trong hàm `__init__` được tạo tự động, vì nó được tính toán trong `__post_init__`.

**Tóm lại**

`__post_init__` là một phương thức mạnh mẽ cho phép bạn kiểm soát nhiều hơn quá trình khởi tạo đối tượng trong `dataclass`. Nó giúp bạn viết mã rõ ràng hơn, dễ bảo trì hơn và ít bị lỗi hơn bằng cách tách biệt logic xác thực và tính toán khỏi định nghĩa lớp chính.


####  5.3. <a name='TypedClassAttributes'></a>Typed Class Attributes

Trong Python, khi sử dụng `@dataclass` để tạo các lớp dữ liệu, đôi khi bạn cần định nghĩa các **thuộc tính lớp** (class attribute). Đây là những biến được chia sẻ bởi tất cả các instance của lớp, chứ không phải riêng lẻ cho từng instance. Ví dụ, bạn có thể muốn theo dõi tổng số thành viên trong một câu lạc bộ.

**Vấn đề với kiểu gợi ý**

Thông thường, bạn có thể thêm kiểu gợi ý (type hint) cho các biến trong Python để giúp trình kiểm tra kiểu như Mypy phát hiện lỗi. Tuy nhiên, khi sử dụng `@dataclass`, nếu bạn thêm kiểu gợi ý cho một thuộc tính lớp, `@dataclass` sẽ hiểu nhầm nó là một **thuộc tính instance** (instance attribute) và tạo ra một bản sao riêng cho mỗi instance.

**`ClassVar` đến giải cứu**

Để giải quyết vấn đề này, chúng ta sử dụng `ClassVar` từ module `typing`. `ClassVar` là một kiểu đặc biệt nói với `@dataclass` rằng đây là một thuộc tính lớp, không phải thuộc tính instance.

**Ví dụ minh họa**

Hãy tưởng tượng bạn đang tạo một lớp `Counter` để đếm số lần một hành động được thực hiện:

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Counter:
    count: ClassVar[int] = 0  # Khai báo thuộc tính lớp count với kiểu int

    def increment(self):
        Counter.count += 1

counter1 = Counter()
counter2 = Counter()

counter1.increment()
counter2.increment()

print(Counter.count)  # Output: 2
```

Trong ví dụ này:

* `count: ClassVar[int] = 0` khai báo `count` là một thuộc tính lớp có kiểu `int` và giá trị ban đầu là 0.
* `Counter.count` được sử dụng để truy cập và thay đổi giá trị của thuộc tính lớp.
* Cả `counter1` và `counter2` đều chia sẻ cùng một biến `count`.

**Tóm lại**

`ClassVar` giúp bạn định nghĩa rõ ràng các thuộc tính lớp trong `dataclass` và đảm bảo rằng chúng được chia sẻ bởi tất cả các instance. Điều này giúp mã của bạn dễ hiểu hơn, ít bị lỗi hơn và dễ bảo trì hơn.

####  5.4. <a name='InitializationVariablesThatAreNotFields'></a>Initialization Variables That Are Not Fields

Trong Python, `dataclass` cung cấp một cách tiện lợi để định nghĩa các lớp chứa chủ yếu dữ liệu. Thông thường, các thuộc tính của một `dataclass` được khởi tạo trực tiếp từ các tham số của hàm `__init__`. Tuy nhiên, đôi khi bạn cần truyền thêm thông tin vào `__init__` mà không muốn lưu trữ chúng như một thuộc tính của đối tượng. Đây là lúc `InitVar` trở nên hữu ích.

**`InitVar` là gì?**

`InitVar` là một kiểu đặc biệt trong `dataclass` cho phép bạn khai báo các biến chỉ được sử dụng trong quá trình khởi tạo đối tượng.  Các biến này sẽ được truyền vào hàm `__init__` và `__post_init__`, nhưng chúng sẽ không trở thành thuộc tính của đối tượng.

**Tại sao cần `InitVar`?**

* **Tránh lưu trữ dữ liệu không cần thiết:**  Nếu một biến chỉ được sử dụng để tính toán giá trị cho các thuộc tính khác trong quá trình khởi tạo, bạn không cần phải lưu trữ nó như một thuộc tính của đối tượng.
* **Tăng tính linh hoạt:** `InitVar` cho phép bạn truyền thêm thông tin vào `__init__` mà không cần phải thay đổi cấu trúc của lớp.

**Ví dụ minh họa**

Giả sử bạn đang xây dựng một hệ thống quản lý sản phẩm. Mỗi sản phẩm có tên, giá và mã giảm giá (tùy chọn). Bạn muốn tính toán giá cuối cùng của sản phẩm sau khi áp dụng mã giảm giá, nhưng bạn không muốn lưu trữ mã giảm giá như một thuộc tính của sản phẩm.

```python
from dataclasses import dataclass, InitVar

@dataclass
class Product:
    name: str
    price: float
    discount_code: InitVar[str] = None  # Khai báo discount_code là InitVar

    def __post_init__(self, discount_code):
        if discount_code == "SUMMER20":
            self.price *= 0.8  # Giảm giá 20%

product1 = Product("Áo phông", 200000, "SUMMER20")
product2 = Product("Quần jean", 500000)

print(product1)  # Output: Product(name='Áo phông', price=160000.0)
print(product2)  # Output: Product(name='Quần jean', price=500000)
```

Trong ví dụ này:

* `discount_code` được khai báo là `InitVar[str]`, cho phép nó được truyền vào `__init__` và `__post_init__`.
* Trong `__post_init__`, giá của sản phẩm được giảm 20% nếu `discount_code` là "SUMMER20".
* `discount_code` không được lưu trữ như một thuộc tính của `product1` hay `product2`.

**Tóm lại**

`InitVar` là một công cụ hữu ích trong `dataclass` khi bạn cần xử lý thông tin trong quá trình khởi tạo mà không muốn lưu trữ chúng như thuộc tính của đối tượng. Nó giúp bạn viết mã gọn gàng hơn, hiệu quả hơn và dễ bảo trì hơn.


####  5.5. <a name='dataclassExample:DublinCoreResourceRecord'></a>@dataclass Example: Dublin Core Resource Record

Mặc dù `@dataclass` cung cấp một cách tiện lợi để định nghĩa các lớp dữ liệu trong Python, việc lạm dụng nó có thể dẫn đến một số vấn đề trong dự án của bạn. Dưới đây là một số lý do tại sao bạn nên thận trọng khi sử dụng `@dataclass`:

**1. Mất tính linh hoạt:**

* `@dataclass` tập trung vào việc lưu trữ dữ liệu và tự động tạo ra các phương thức như `__init__`, `__repr__`, và `__eq__`. Điều này có thể hạn chế khả năng tùy chỉnh hành vi của lớp nếu bạn cần logic phức tạp hơn.
* Khi logic nghiệp vụ phát triển, bạn có thể cần thêm các phương thức và thuộc tính phức tạp vào lớp. Việc này có thể làm cho `dataclass` trở nên cồng kềnh và khó quản lý.

**2. Khuyến khích thiết kế kém:**

* Lạm dụng `@dataclass` có thể dẫn đến việc tạo ra quá nhiều lớp dữ liệu nhỏ, thiếu logic nghiệp vụ. Điều này làm cho mã nguồn trở nên phân mảnh và khó theo dõi.
* `@dataclass` có thể khuyến khích tư duy "hướng dữ liệu" thay vì "hướng đối tượng". Điều này có thể dẫn đến việc bỏ qua các nguyên tắc thiết kế hướng đối tượng quan trọng như đóng gói (encapsulation) và trừu tượng hóa (abstraction).

**3. Khó khăn trong việc bảo trì:**

* Khi dự án phát triển, các `dataclass` có thể trở nên phức tạp và khó hiểu, đặc biệt là khi có nhiều lớp dữ liệu liên quan đến nhau.
* Việc thay đổi cấu trúc của một `dataclass` có thể ảnh hưởng đến nhiều phần khác của mã nguồn, gây khó khăn cho việc bảo trì và phát triển.

**Ví dụ minh họa**

Giả sử bạn đang xây dựng một ứng dụng quản lý thư viện. Ban đầu, bạn sử dụng `@dataclass` để định nghĩa lớp `Book`:

```python
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    isbn: str
```

Tuy nhiên, sau đó bạn cần thêm các chức năng như kiểm tra tình trạng mượn trả, tính phí phạt quá hạn, và cập nhật thông tin sách. Việc này đòi hỏi thêm nhiều thuộc tính và phương thức vào lớp `Book`, khiến nó trở nên phức tạp và khó quản lý.

**Giải pháp thay thế**

Thay vì lạm dụng `@dataclass`, bạn nên xem xét sử dụng các lớp thông thường và tự định nghĩa các phương thức cần thiết. Điều này cho phép bạn kiểm soát tốt hơn hành vi của lớp và áp dụng các nguyên tắc thiết kế hướng đối tượng hiệu quả hơn.

**Tóm lại**

`@dataclass` là một công cụ hữu ích cho việc định nghĩa các lớp dữ liệu đơn giản trong Python. Tuy nhiên, bạn nên sử dụng nó một cách có chọn lọc và cân nhắc kỹ lưỡng trước khi áp dụng cho các lớp phức tạp hơn.  Việc lạm dụng `@dataclass` có thể dẫn đến mã nguồn kém linh hoạt, khó bảo trì và khó mở rộng.

---
###  6. <a name='DataClassasaCodeSmell'></a>Data Class as a Code Smell

Trong lập trình hướng đối tượng, "mùi mã" (code smell) là dấu hiệu cho thấy có thể có vấn đề tiềm ẩn trong thiết kế mã nguồn. Một trong những "mùi mã" phổ biến là **lớp dữ liệu** (data class).

**Lớp dữ liệu là gì?**

Lớp dữ liệu là lớp chỉ chứa dữ liệu (các thuộc tính) và các phương thức đơn giản để truy cập và thay đổi dữ liệu đó (getter/setter). Chúng giống như "hộp chứa" dữ liệu thụ động, không có hành vi (logic xử lý) đáng kể.

**Tại sao lớp dữ liệu là "mùi mã"?**

Lớp dữ liệu vi phạm nguyên tắc cơ bản của lập trình hướng đối tượng: **đóng gói dữ liệu và hành vi liên quan trong cùng một đơn vị (lớp)**. Khi một lớp chỉ chứa dữ liệu, logic xử lý dữ liệu đó thường bị phân tán ra các lớp khác, dẫn đến:

* **Mã nguồn khó đọc và khó bảo trì:** Logic xử lý bị phân mảnh, khó theo dõi và dễ gây lỗi khi thay đổi.
* **Trùng lặp mã:** Cùng một logic xử lý có thể được viết lại nhiều lần ở các lớp khác nhau.
* **Khó mở rộng:** Khi cần thêm chức năng mới, bạn phải sửa đổi nhiều lớp khác nhau, tăng nguy cơ gây ra lỗi.

**Ví dụ minh họa**

Giả sử bạn đang viết chương trình quản lý học sinh. Bạn có lớp `HocSinh` như sau:

```python
class HocSinh:
  def __init__(self, ten, tuoi, diem):
    self.ten = ten
    self.tuoi = tuoi
    self.diem = diem

  def lay_ten(self):
    return self.ten

  def lay_tuoi(self):
    return self.tuoi

  def lay_diem(self):
    return self.diem
```

Lớp này chỉ chứa dữ liệu về học sinh (tên, tuổi, điểm) và các phương thức getter. Logic xử lý dữ liệu (ví dụ: tính điểm trung bình, xếp loại học lực) sẽ nằm ở lớp khác, chẳng hạn `LopHoc`.

**Cách khắc phục**

Để loại bỏ "mùi mã" lớp dữ liệu, bạn nên **di chuyển logic xử lý liên quan đến dữ liệu vào chính lớp dữ liệu đó**. Ví dụ, bạn có thể thêm phương thức `tinh_diem_trung_binh()` vào lớp `HocSinh`.

```python
class HocSinh:
  # ... (các thuộc tính và getter như trên)

  def tinh_diem_trung_binh(self):
    # Tính toán và trả về điểm trung bình của học sinh
    pass
```

Bằng cách này, lớp `HocSinh` trở nên "thông minh" hơn, chứa cả dữ liệu và hành vi liên quan, giúp mã nguồn dễ đọc, dễ bảo trì và dễ mở rộng hơn.

**Tóm lại**

Lớp dữ liệu là "mùi mã" phổ biến trong lập trình hướng đối tượng. Nhận biết và khắc phục "mùi mã" này sẽ giúp bạn viết mã nguồn chất lượng cao hơn.

####  6.1. <a name='DataClassasScaffolding'></a>Data Class as Scaffolding

Trong phát triển phần mềm, **scaffolding** (giàn giáo) là một kỹ thuật tạo ra một cấu trúc cơ bản, tạm thời để hỗ trợ việc xây dựng và phát triển ứng dụng. Scaffolding giúp bạn nhanh chóng tạo ra một "bộ khung" cho ứng dụng, từ đó tập trung vào việc phát triển các tính năng chính.

**Lớp dữ liệu như Scaffolding**

Trong Python, `@dataclass` có thể được sử dụng như một dạng scaffolding để nhanh chóng tạo ra các lớp dữ liệu đơn giản. Ban đầu, lớp dữ liệu này có thể chỉ chứa các thuộc tính và các phương thức cơ bản như `__init__`, `__repr__`, và `__eq__`. Tuy nhiên, khi dự án phát triển, bạn có thể dần dần thêm các phương thức và thuộc tính phức tạp hơn vào lớp, biến nó từ một "bộ khung" đơn giản thành một lớp hoàn chỉnh với đầy đủ chức năng.

**Ưu điểm của việc sử dụng `@dataclass` như Scaffolding:**

* **Nhanh chóng tạo ra cấu trúc cơ bản:** `@dataclass` giúp bạn tiết kiệm thời gian và công sức trong việc định nghĩa các lớp dữ liệu, cho phép bạn tập trung vào việc phát triển logic nghiệp vụ.
* **Dễ dàng mở rộng:** Ban đầu, lớp dữ liệu có thể đơn giản, nhưng bạn có thể dễ dàng thêm các phương thức và thuộc tính mới khi cần thiết.
* **Tăng tính linh hoạt:** Scaffolding là tạm thời. Khi lớp dữ liệu đã phát triển đầy đủ, bạn có thể loại bỏ `@dataclass` và sử dụng lớp như một lớp thông thường.

**Ví dụ minh họa**

Giả sử bạn đang phát triển một ứng dụng quản lý nhân viên. Ban đầu, bạn có thể sử dụng `@dataclass` để tạo một lớp `NhanVien` đơn giản:

```python
from dataclasses import dataclass

@dataclass
class NhanVien:
    ten: str
    tuoi: int
    chuc_vu: str
```

Lớp này chỉ chứa các thuộc tính cơ bản về nhân viên. Sau đó, khi ứng dụng phát triển, bạn có thể thêm các phương thức như `tinh_luong()`, `cap_nhat_thong_tin()`, `danh_gia_hieu_qua()` vào lớp `NhanVien`.

**Kết luận**

Sử dụng `@dataclass` như scaffolding là một cách hiệu quả để nhanh chóng tạo ra các lớp dữ liệu trong Python. Kỹ thuật này giúp bạn tiết kiệm thời gian, tăng tính linh hoạt và dễ dàng mở rộng ứng dụng khi cần thiết.

####  6.2. <a name='DataClassasIntermediateRepresentation'></a>Data Class as Intermediate Representation

Trong nhiều ứng dụng, bạn cần trao đổi dữ liệu với các hệ thống khác, chẳng hạn như lưu trữ dữ liệu vào cơ sở dữ liệu, gửi dữ liệu qua mạng, hoặc đọc dữ liệu từ file cấu hình. Trong những trường hợp này, bạn cần một cách để biểu diễn dữ liệu dưới dạng trung gian, sao cho dễ dàng chuyển đổi giữa các định dạng khác nhau.

**Lớp dữ liệu như Biểu diễn trung gian**

Trong Python, `@dataclass` có thể đóng vai trò như một lớp biểu diễn trung gian hiệu quả.  Các trình tạo lớp dữ liệu của Python (`@dataclass`, `namedtuple`, `SimpleNamespace`) đều cung cấp các phương thức hoặc hàm để chuyển đổi một instance của lớp thành `dict`, và ngược lại. `dict` là một kiểu dữ liệu phổ biến, dễ dàng chuyển đổi sang các định dạng khác như JSON hoặc XML.

**Ưu điểm của việc sử dụng `@dataclass` như Biểu diễn trung gian:**

* **Rõ ràng và dễ đọc:** `@dataclass` giúp bạn định nghĩa cấu trúc dữ liệu một cách rõ ràng và dễ đọc.
* **Dễ dàng chuyển đổi:** Chuyển đổi giữa `@dataclass` và `dict` rất đơn giản, giúp bạn dễ dàng trao đổi dữ liệu với các hệ thống khác.
* **Kiểm tra kiểu:** `@dataclass` hỗ trợ kiểm tra kiểu, giúp bạn phát hiện lỗi sớm trong quá trình phát triển.

**Ví dụ minh họa**

Giả sử bạn đang xây dựng một ứng dụng web. Bạn cần lưu trữ thông tin người dùng vào cơ sở dữ liệu và gửi thông tin này đến trình duyệt web dưới dạng JSON. Bạn có thể sử dụng `@dataclass` để biểu diễn thông tin người dùng:

```python
from dataclasses import dataclass

@dataclass
class NguoiDung:
    ten: str
    email: str
    tuoi: int

nguoi_dung = NguoiDung("John Doe", "john.doe@example.com", 30)

# Chuyển đổi sang dict
nguoi_dung_dict = vars(nguoi_dung)  # {'ten': 'John Doe', 'email': 'john.doe@example.com', 'tuoi': 30}

# Chuyển đổi sang JSON
import json
nguoi_dung_json = json.dumps(nguoi_dung_dict)  # '{"ten": "John Doe", "email": "john.doe@example.com", "tuoi": 30}'
```

Trong ví dụ này:

* `@dataclass` được sử dụng để định nghĩa lớp `NguoiDung` với các thuộc tính `ten`, `email`, và `tuoi`.
* Hàm `vars()` được sử dụng để chuyển đổi instance `nguoi_dung` thành `dict`.
* Module `json` được sử dụng để chuyển đổi `dict` thành chuỗi JSON.

**Lưu ý:**

Khi sử dụng `@dataclass` như Biểu diễn trung gian, bạn nên coi các instance của lớp là bất biến. Tránh thay đổi giá trị của các thuộc tính sau khi đã chuyển đổi sang `dict` hoặc JSON, vì điều này có thể gây ra lỗi đồng bộ dữ liệu.

**Kết luận**

`@dataclass` là một công cụ hữu ích để biểu diễn dữ liệu trung gian trong Python. Nó giúp bạn trao đổi dữ liệu với các hệ thống khác một cách dễ dàng, rõ ràng và hiệu quả.

---
###  7. <a name='PatternMatchingClassInstances'></a>Pattern Matching Class Instances

Trong Python 3.10, tính năng **ghép nối mẫu** (pattern matching) đã được giới thiệu, cho phép bạn kiểm tra cấu trúc của dữ liệu và thực hiện các hành động khác nhau dựa trên cấu trúc đó. Một trong những kiểu mẫu mạnh mẽ là **mẫu lớp** (class pattern), được sử dụng để khớp với các instance của lớp.

####  7.1. <a name='SimpleClassPatterns'></a>Simple Class Patterns

Mẫu lớp đơn giản trong Python được sử dụng trong `match...case` để kiểm tra xem một đối tượng có thuộc một lớp cụ thể hay không. 

**Cú pháp:**

```python
case TenLop():
    # Thực hiện các hành động nếu đối tượng thuộc lớp TenLop
```

**Lưu ý quan trọng:**

* **Dấu ngoặc đơn `()`:**  Phải có dấu ngoặc đơn sau tên lớp để phân biệt với việc gán biến. Nếu không có dấu ngoặc đơn, Python sẽ coi tên lớp là một biến và gán giá trị của đối tượng cho biến đó.

**Ví dụ 1: Kiểm tra kiểu dữ liệu**

```python
def kiem_tra_kieu(du_lieu):
    match du_lieu:
        case int():
            print("Đây là số nguyên")
        case str():
            print("Đây là chuỗi")
        case float():
            print("Đây là số thực")
        case _:
            print("Kiểu dữ liệu không xác định")

kiem_tra_kieu(10)      # Output: Đây là số nguyên
kiem_tra_kieu("Hello")  # Output: Đây là chuỗi
kiem_tra_kieu(3.14)    # Output: Đây là số thực
kiem_tra_kieu([1, 2])   # Output: Kiểu dữ liệu không xác định
```

**Ví dụ 2: Kiểm tra instance của lớp tự định nghĩa**

```python
class HinhVuong:
    def __init__(self, canh):
        self.canh = canh

def tinh_dien_tich(hinh):
    match hinh:
        case HinhVuong():
            return hinh.canh * hinh.canh
        case _:
            return "Không thể tính diện tích"

hinh_vuong = HinhVuong(5)
print(tinh_dien_tich(hinh_vuong))  # Output: 25
```

**Phân biệt với việc gán biến:**

```python
match 10:
    case int:  # int được coi là biến, luôn khớp với mọi giá trị
        print("Luôn in ra câu này")  # Output: Luôn in ra câu này

match 10:
    case int():  # Kiểm tra xem giá trị có phải là số nguyên không
        print("Đây là số nguyên")  # Output: Đây là số nguyên
```

**Tóm lại:**

Mẫu lớp đơn giản là một cách hiệu quả để kiểm tra kiểu dữ liệu hoặc instance của lớp trong Python.  Hãy nhớ sử dụng dấu ngoặc đơn sau tên lớp để tránh nhầm lẫn với việc gán biến.


####  7.2. <a name='KeywordClassPatterns'></a>Keyword Class Patterns

Mẫu lớp từ khóa trong Python cho phép bạn kiểm tra kiểu của một đối tượng và so khớp các thuộc tính của nó với các giá trị mong muốn trong câu lệnh `match...case`.

**Cú pháp:**

```python
case TenLop(thuoc_tinh_1=gia_tri_1, thuoc_tinh_2=gia_tri_2, ...):
    # Thực hiện các hành động nếu đối tượng khớp với mẫu
```

**Cách hoạt động:**

* Mẫu sẽ kiểm tra xem đối tượng có phải là instance của `TenLop` hay không.
* Nếu đúng, mẫu sẽ tiếp tục kiểm tra xem các thuộc tính của đối tượng có khớp với các giá trị được chỉ định hay không.
* Nếu tất cả các điều kiện đều đúng, mẫu sẽ khớp và các hành động trong khối `case` sẽ được thực hiện.

**Ví dụ minh họa:**

```python
from dataclasses import dataclass

@dataclass
class SinhVien:
    ten: str
    tuoi: int
    diem: float

def xep_loai(sinh_vien):
    match sinh_vien:
        case SinhVien(ten="John Doe", tuoi=20, diem=9.0):
            print("Sinh viên xuất sắc")
        case SinhVien(diem=x) if x >= 8.0:
            print("Sinh viên giỏi")
        case SinhVien(diem=x) if x >= 5.0:
            print("Sinh viên khá")
        case _:
            print("Sinh viên trung bình")

sv1 = SinhVien("John Doe", 20, 9.0)
sv2 = SinhVien("Jane Doe", 21, 8.5)
sv3 = SinhVien("Peter Pan", 19, 6.0)
sv4 = SinhVien("Alice", 22, 4.5)

xep_loai(sv1)  # Output: Sinh viên xuất sắc
xep_loai(sv2)  # Output: Sinh viên giỏi
xep_loai(sv3)  # Output: Sinh viên khá
xep_loai(sv4)  # Output: Sinh viên trung bình
```

Trong ví dụ này:

* Mẫu `SinhVien(ten="John Doe", tuoi=20, diem=9.0)` khớp với `sv1` vì tất cả các thuộc tính đều khớp.
* Mẫu `SinhVien(diem=x) if x >= 8.0` khớp với `sv2` vì `diem` lớn hơn hoặc bằng 8.0.
* Mẫu `SinhVien(diem=x) if x >= 5.0` khớp với `sv3` vì `diem` lớn hơn hoặc bằng 5.0.
* Mẫu `_` là mẫu mặc định, khớp với `sv4` vì không có mẫu nào khác khớp.

**Ưu điểm của mẫu lớp từ khóa:**

* Dễ đọc và dễ hiểu.
* Linh hoạt, cho phép bạn kiểm tra các thuộc tính cụ thể.

**Nhược điểm:**

* Có thể dài dòng nếu bạn cần kiểm tra nhiều thuộc tính.

**Tóm lại:**

Mẫu lớp từ khóa là một công cụ hữu ích trong Python để so khớp các instance của lớp dựa trên kiểu và giá trị của các thuộc tính.


####  7.3. <a name='PositionalClassPatterns'></a>Positional Class Patterns

Với các định nghĩa từ Ví dụ 5-22, hàm sau sẽ trả về danh sách các thành phố châu Á, sử dụng mẫu lớp vị trí:

```python
def match_asian_cities_pos():
    results = []
    for city in cities:
        match city:
            case City('Asia'):
                results.append(city)
    return results
```

Mẫu `City('Asia')` khớp với bất kỳ **instance** `City` nào trong đó giá trị thuộc tính **đầu tiên** là 'Asia', bất kể giá trị của các thuộc tính khác.

Nếu bạn muốn thu thập giá trị của thuộc tính `country`, bạn có thể viết:

```python
def match_asian_countries_pos():
    results = []
    for city in cities:
        match city:
            case City('Asia', _, country):
                results.append(country)
    return results
```

Mẫu `City('Asia', _, country)` khớp với các thành phố giống như trước đây, nhưng bây giờ biến `country` được liên kết với thuộc tính **thứ ba** của **instance**.

Tôi đã đề cập đến thuộc tính “đầu tiên” hoặc “thứ ba”, nhưng điều đó thực sự có nghĩa là gì?

Điều làm cho `City` hoặc bất kỳ lớp nào hoạt động với các mẫu vị trí là sự hiện diện của một thuộc tính lớp đặc biệt có tên `__match_args__`, mà các trình tạo lớp trong chương này tự động tạo ra. Đây là giá trị của `__match_args__` trong lớp `City`:

```python
>>> City.__match_args__
('continent', 'name', 'country')
```

Như bạn có thể thấy, `__match_args__` khai báo tên của các thuộc tính theo thứ tự chúng sẽ được sử dụng trong các mẫu vị trí.

Trong “Hỗ trợ ghép nối mẫu vị trí” trên trang 377, chúng ta sẽ viết mã để định nghĩa `__match_args__` cho một lớp mà chúng ta sẽ tạo mà không cần sự trợ giúp của trình tạo lớp.
