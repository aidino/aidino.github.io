---
layout: post
title: "[Fluent python] Chapter 7. Functions as First-Class Objects"
date: 2025-01-14 11:00:00 +0700
categories: fluent python
---

Hàm được coi như những "đối tượng hạng nhất" (first-class objects).
Điều này có nghĩa là hàm trong Python rất linh hoạt, giống như các kiểu dữ liệu khác (như số, chuỗi). Bạn có thể:

- **Tạo ra hàm ngay trong lúc chương trình đang chạy.**
- **Lưu hàm vào biến hoặc trong các cấu trúc dữ liệu.**
- **Đưa hàm vào làm tham số cho một hàm khác.**
- **Tạo ra hàm mới mà kết quả trả về là một hàm khác.**

Mặc dù tính năng này phổ biến trong các ngôn ngữ lập trình hàm (functional programming language), nhưng nó hữu ích đến mức các ngôn ngữ khác (như JavaScript, Go, Java) cũng đã áp dụng.

### Table of contents

1. [Treating a Function Like an Object](#TreatingaFunctionLikeanObject)
2. [Higher-Order Functions](#Higher-OrderFunctions)
  * 2.1. [Modern Replacements for map, filter, and reduce](#ModernReplacementsformapfilterandreduce)
3. [Anonymous Functions](#AnonymousFunctions)
4. [The Nine Flavors of Callable Objects](#TheNineFlavorsofCallableObjects)
5. [User-Defined Callable Types](#User-DefinedCallableTypes)
6. [From Positional to Keyword-Only Parameters](#FromPositionaltoKeyword-OnlyParameters)
  * 6.1. [Positional-Only Parameters](#Positional-OnlyParameters)
7. [Packages for Functional Programming](#PackagesforFunctionalProgramming)
  * 7.1. [The operator Module](#TheoperatorModule)
  * 7.2. [Freezing Arguments with functools.partial](#FreezingArgumentswithfunctools.partial)

---

###  1. <a name='TreatingaFunctionLikeanObject'></a>Treating a Function Like an Object

**Hàm trong Python cũng là đối tượng:**

Hãy tưởng tượng "đối tượng" như một món đồ chơi. Món đồ chơi này có thể có những đặc điểm (thuộc tính) như màu sắc, kích thước và có thể thực hiện các hành động (phương thức). 

Trong Python, hàm cũng giống như một món đồ chơi vậy. Nó có:

* **Đặc điểm (thuộc tính):** Ví dụ, hàm có thuộc tính `__doc__` để lưu trữ đoạn mô tả về hàm đó.
* **Hành động (phương thức):**  Bản thân hàm chính là một phương thức, khi được gọi sẽ thực hiện một loạt các lệnh.

**Ví dụ minh họa:**

```python
def chao_mung(ten):
  """Hàm này chào mừng người dùng."""
  print(f"Chào mừng, {ten}!")

# Gọi hàm
chao_mung("Linh")  # Output: Chào mừng, Linh!

# Truy cập thuộc tính __doc__
print(chao_mung.__doc__)  # Output: Hàm này chào mừng người dùng.
```

Trong ví dụ trên:

* `chao_mung` là tên của hàm (món đồ chơi).
* `__doc__` là thuộc tính của hàm, chứa mô tả "Hàm này chào mừng người dùng."
* Việc gọi `chao_mung("Linh")` chính là thực hiện hành động (phương thức) của hàm, in ra lời chào.

**Vì sao hàm là đối tượng thì có lợi?**

Vì hàm là đối tượng nên ta có thể:

* **Gán hàm cho một biến khác:** Giống như ta có thể đặt tên khác cho món đồ chơi, ta cũng có thể gán hàm cho một biến khác và gọi hàm thông qua biến đó.
* **Truyền hàm như một đối số:** Ta có thể đưa hàm vào làm "nguyên liệu" cho một hàm khác, giống như đưa món đồ chơi vào một chiếc hộp.

**Ví dụ minh họa:**

```python
def tinh_binh_phuong(x):
  return x * x

# Gán hàm cho biến khác
bp = tinh_binh_phuong
print(bp(5))  # Output: 25

# Truyền hàm như một đối số
danh_sach_so = [1, 2, 3, 4, 5]
danh_sach_binh_phuong = list(map(tinh_binh_phuong, danh_sach_so))
print(danh_sach_binh_phuong)  # Output: [1, 4, 9, 16, 25] 
```

Trong ví dụ này:

* Ta gán hàm `tinh_binh_phuong` cho biến `bp`.
* Ta truyền hàm `tinh_binh_phuong` vào hàm `map` để tính bình phương cho từng số trong danh sách.


---

###  2. <a name='Higher-OrderFunctions'></a>Higher-Order Functions

**Hàm bậc cao là gì?**

Hãy tưởng tượng bạn có một chiếc máy chế biến thức ăn đa năng. Chiếc máy này có thể thực hiện nhiều chức năng khác nhau như xay sinh tố, ép trái cây, làm kem,...  và bạn có thể thay đổi các lưỡi dao (bộ phận xử lý) để thực hiện các chức năng mong muốn.

Hàm bậc cao trong lập trình cũng tương tự như vậy. Nó là một hàm đặc biệt có khả năng:

* **Nhận một hàm khác làm đầu vào:** Giống như việc bạn lắp các lưỡi dao khác nhau vào máy chế biến.
* **Trả về một hàm khác làm kết quả:**  Giống như việc bạn tạo ra một "chế độ" mới cho máy chế biến bằng cách kết hợp các lưỡi dao.

**Ví dụ minh họa:**

```python
def ap_dung_ham(ham, danh_sach):
  """Hàm này áp dụng một hàm cho từng phần tử trong danh sách."""
  ket_qua = []
  for phan_tu in danh_sach:
    ket_qua.append(ham(phan_tu))
  return ket_qua

def tang_len_1(x):
  """Hàm này tăng giá trị đầu vào lên 1."""
  return x + 1

danh_sach_so = [1, 2, 3, 4, 5]

# Áp dụng hàm tang_len_1 cho từng số trong danh sách
ket_qua = ap_dung_ham(tang_len_1, danh_sach_so)
print(ket_qua)  # Output: [2, 3, 4, 5, 6]
```

Trong ví dụ trên, `ap_dung_ham` là một hàm bậc cao vì nó nhận hàm `tang_len_1` làm đầu vào. Hàm `ap_dung_ham` giống như chiếc máy chế biến, còn `tang_len_1` giống như lưỡi dao được lắp vào để thực hiện chức năng cụ thể.

**Lợi ích của hàm bậc cao:**

* **Tái sử dụng mã:** Bạn có thể viết một hàm bậc cao để xử lý chung cho nhiều trường hợp, chỉ cần thay đổi hàm đầu vào.
* **Tăng tính linh hoạt:**  Bạn có thể dễ dàng thay đổi chức năng của chương trình bằng cách thay đổi hàm được truyền vào.
* **Code ngắn gọn, dễ đọc:** Hàm bậc cao giúp giảm thiểu việc lặp lại code, làm cho chương trình dễ hiểu hơn.

**Một số hàm bậc cao phổ biến trong Python:**

* `map()`: Áp dụng một hàm cho từng phần tử trong một iterable (list, tuple,...).
* `filter()`: Lọc các phần tử trong một iterable dựa trên một điều kiện.
* `sorted()`: Sắp xếp các phần tử trong một iterable, có thể sử dụng hàm `key` để tùy chỉnh cách sắp xếp.

**Ví dụ với `sorted()`:**

```python
chuoi = "xin chào"

# Sắp xếp các ký tự trong chuỗi theo thứ tự bảng chữ cái
ket_qua = sorted(chuoi)
print(ket_qua)  # Output: [' ', 'à', 'c', 'h', 'i', 'n', 'o', 'x']
```

####  2.1. <a name='ModernReplacementsformapfilterandreduce'></a>Modern Replacements for map, filter, and reduce

Trong Python, `map`, `filter` và `reduce` là những hàm bậc cao hữu ích, nhưng đôi khi có những cách khác hiện đại và dễ đọc hơn để thực hiện cùng chức năng. Hãy cùng tìm hiểu với các ví dụ minh họa nhé!

**1. `map` và `filter` với List Comprehension/Generator Expression:**

* `map`: Áp dụng một hàm cho từng phần tử trong một danh sách (hoặc tuple,...)
* `filter`: Lọc các phần tử trong danh sách dựa trên một điều kiện.

Thay vì dùng `map` và `filter`, ta có thể sử dụng list comprehension hoặc generator expression để code ngắn gọn và dễ hiểu hơn.

**Ví dụ:**

```python
# Tính bình phương của các số từ 0 đến 5 bằng map
danh_sach_so = [0, 1, 2, 3, 4, 5]
binh_phuong_map = list(map(lambda x: x*x, danh_sach_so)) 
print(binh_phuong_map)  # Output: [0, 1, 4, 9, 16, 25]

# Tính bình phương bằng list comprehension
binh_phuong_lc = [x*x for x in danh_sach_so]
print(binh_phuong_lc)  # Output: [0, 1, 4, 9, 16, 25]

# Lọc các số chẵn từ 0 đến 5 bằng filter
so_chan_filter = list(filter(lambda x: x % 2 == 0, danh_sach_so))
print(so_chan_filter)  # Output: [0, 2, 4]

# Lọc các số chẵn bằng list comprehension
so_chan_lc = [x for x in danh_sach_so if x % 2 == 0]
print(so_chan_lc)  # Output: [0, 2, 4]
```

Như bạn thấy, list comprehension giúp code ngắn gọn và dễ đọc hơn so với `map` và `filter`.

**2. `reduce` với `sum`:**

`reduce` áp dụng một hàm (ví dụ hàm cộng) lặp đi lặp lại cho các phần tử trong danh sách để cuối cùng thu được một giá trị duy nhất. Tuy nhiên, trong trường hợp tính tổng, hàm `sum` tích hợp sẵn của Python lại hiệu quả và dễ hiểu hơn.

**Ví dụ:**

```python
from functools import reduce 

# Tính tổng các số từ 1 đến 10 bằng reduce
tong_reduce = reduce(lambda x, y: x + y, range(1, 11))
print(tong_reduce)  # Output: 55

# Tính tổng bằng sum
tong_sum = sum(range(1, 11))
print(tong_sum)  # Output: 55
```

**Tóm lại:**

Mặc dù `map`, `filter` và `reduce` là những hàm mạnh mẽ, nhưng Python cung cấp những lựa chọn thay thế hiện đại hơn. List comprehension/generator expression và hàm `sum` thường giúp code ngắn gọn, dễ đọc và hiệu quả hơn.

**Lưu ý:**

* `reduce` không còn là hàm tích hợp sẵn trong Python 3, bạn cần import từ module `functools` để sử dụng.
* `map` và `filter` trong Python 3 trả về generator (một dạng iterator), khác với Python 2 trả về list.

---

###  3. <a name='AnonymousFunctions'></a>Anonymous Functions

**Hàm ẩn danh là gì?**

Trong Python, hàm ẩn danh (hay còn gọi là lambda function) là một hàm nhỏ gọn, không cần đặt tên. Nó giống như một công thức ngắn gọn để thực hiện một tác vụ đơn giản, mà không cần phải định nghĩa một hàm đầy đủ bằng từ khóa `def`.

**Cú pháp:**

```python
lambda arguments: expression
```

* `lambda`: Từ khóa để khai báo hàm ẩn danh.
* `arguments`: Các tham số của hàm, giống như trong hàm thông thường.
* `expression`: Biểu thức sẽ được tính toán và trả về kết quả.

**Ví dụ:**

```python
binh_phuong = lambda x: x * x
print(binh_phuong(5))  # Output: 25
```

Trong ví dụ này, `lambda x: x * x` là một hàm ẩn danh nhận một tham số `x` và trả về bình phương của `x`.

**Đặc điểm:**

* **Ngắn gọn:** Hàm ẩn danh thường chỉ gồm một dòng code duy nhất.
* **Không tên:**  Không cần đặt tên cho hàm, nên gọi là "ẩn danh".
* **Hạn chế:** Chỉ có thể chứa một biểu thức duy nhất, không thể chứa các câu lệnh phức tạp như `if`, `else`, `for`,...
* **Thường dùng với hàm bậc cao:**  Hàm ẩn danh thường được sử dụng làm đối số cho các hàm bậc cao như `map`, `filter`, `sorted`.

**Ví dụ với hàm bậc cao `sorted`:**

```python
danh_sach_ten = ["Linh", "Nam", "An"]

# Sắp xếp danh sách tên theo độ dài (từ ngắn đến dài)
danh_sach_sap_xep = sorted(danh_sach_ten, key=lambda ten: len(ten))
print(danh_sach_sap_xep)  # Output: ['An', 'Nam', 'Linh']
```

Trong ví dụ này, `lambda ten: len(ten)` là một hàm ẩn danh trả về độ dài của một chuỗi. Hàm `sorted` sử dụng hàm ẩn danh này để sắp xếp danh sách tên theo độ dài.

**Khi nào nên sử dụng hàm ẩn danh?**

* Khi cần một hàm đơn giản, chỉ dùng một lần.
* Khi cần truyền một hàm làm đối số cho hàm bậc cao.
* Khi muốn code ngắn gọn hơn.

**Lưu ý:**

* Nếu hàm ẩn danh quá phức tạp, khó đọc, nên sử dụng hàm thông thường (`def`) để thay thế.
* Hàm ẩn danh chỉ nên được sử dụng khi thực sự cần thiết, tránh lạm dụng làm code khó hiểu.

---

###  4. <a name='TheNineFlavorsofCallableObjects'></a>The Nine Flavors of Callable Objects

Trong Python, "đối tượng có thể gọi" (callable object) là những đối tượng mà bạn có thể sử dụng toán tử `()` để "gọi" chúng, giống như cách bạn gọi một hàm. Hãy tưởng tượng chúng như những chiếc chuông cửa với 9 kiểu dáng khác nhau, mỗi kiểu khi bấm sẽ tạo ra âm thanh hoặc hiệu ứng riêng biệt.

Dưới đây là 9 "hương vị" callable object trong Python, cùng với ví dụ minh họa:

1. **Hàm do người dùng định nghĩa (User-defined functions):**  Đây là những hàm mà bạn tự tạo ra bằng từ khóa `def` hoặc `lambda`.

   ```python
   def chao_mung(ten):
       print(f"Xin chào, {ten}!")

   chao_mung("Linh")  # Output: Xin chào, Linh!
   ```

2. **Hàm tích hợp sẵn (Built-in functions):** Python cung cấp sẵn nhiều hàm hữu ích như `len`, `print`, `type`, ...

   ```python
   danh_sach = [1, 2, 3]
   do_dai = len(danh_sach)  # Output: 3
   ```

3. **Phương thức tích hợp sẵn (Built-in methods):**  Các kiểu dữ liệu như list, string, dictionary có sẵn các phương thức (method) để thao tác với chúng.

   ```python
   chuoi = "xin chào"
   chuoi_hoa = chuoi.upper()  # Output: XIN CHÀO
   ```

4. **Phương thức (Methods):**  Khi bạn định nghĩa một lớp (class), bạn có thể tạo ra các phương thức bên trong lớp đó.

   ```python
   class Cho:
       def sua(self):
           print("Gâu gâu!")

   cho_con = Cho()
   cho_con.sua()  # Output: Gâu gâu!
   ```

5. **Lớp (Classes):**  Bản thân lớp cũng là một callable object. Khi bạn gọi một lớp, nó sẽ tạo ra một đối tượng (instance) của lớp đó.

   ```python
   class Nguoi:
       def __init__(self, ten):
           self.ten = ten

   linh = Nguoi("Linh")  # Tạo đối tượng linh từ lớp Nguoi
   ```

6. **Thể hiện của lớp (Class instances):**  Nếu bạn định nghĩa phương thức đặc biệt `__call__` trong một lớp, thì các đối tượng của lớp đó cũng trở thành callable.

   ```python
   class Counter:
       def __init__(self):
           self.count = 0

       def __call__(self):
           self.count += 1
           return self.count

   dem = Counter()
   print(dem())  # Output: 1
   print(dem())  # Output: 2
   ```

7. **Hàm generator (Generator functions):**  Đây là những hàm sử dụng từ khóa `yield` để tạo ra một chuỗi giá trị.

   ```python
   def fibonacci(n):
       a, b = 0, 1
       for _ in range(n):
           yield a
           a, b = b, a + b

   for so in fibonacci(5):
       print(so)  # Output: 0 1 1 2 3
   ```

8. **Hàm coroutine (Native coroutine functions):**  Sử dụng trong lập trình không đồng bộ (asynchronous programming) với từ khóa `async def`.

   ```python
   async def chao():
       return "Xin chào!"

   # Cần sử dụng trong async framework như asyncio để chạy hàm này
   ```

9. **Hàm asynchronous generator (Asynchronous generator functions):**  Kết hợp `async def` và `yield` để tạo ra một chuỗi giá trị không đồng bộ.

   ```python
   async def count_async(n):
       for i in range(n):
           yield i
           await asyncio.sleep(1)  # Giả lập delay

   # Cần sử dụng trong async framework như asyncio để chạy hàm này
   ```

Để kiểm tra xem một đối tượng có phải là callable object hay không, bạn có thể sử dụng hàm `callable()`.

```python
print(callable(chao_mung))  # Output: True
print(callable("xin chào"))  # Output: False
```
---

###  5. <a name='User-DefinedCallableTypes'></a>User-Defined Callable Types

Thông thường, khi nghĩ về "callable object" (đối tượng có thể gọi), ta thường nghĩ ngay đến các hàm (function). Tuy nhiên, Python cho phép bạn biến những đối tượng bình thường thành "callable", nghĩa là bạn có thể dùng toán tử `()` để gọi chúng như hàm!

**Bí mật nằm ở phương thức `__call__`:**

* Mỗi đối tượng trong Python đều có thể có các phương thức (method) - những hàm được định nghĩa bên trong đối tượng.
* Phương thức `__call__` là một phương thức đặc biệt. Nếu một đối tượng có phương thức này, thì đối tượng đó sẽ trở thành "callable".

**Ví dụ minh họa:**

Hãy tưởng tượng bạn muốn tạo một đối tượng "Hộp quà" (GiftBox). Mỗi khi "gọi" hộp quà này, bạn sẽ nhận được một món quà ngẫu nhiên từ bên trong.

```python
import random

class HopQua:
    def __init__(self, qua):
        self.qua = list(qua)  # Lưu danh sách quà vào hộp

    def __call__(self):
        # Chọn ngẫu nhiên một món quà và trả về
        return random.choice(self.qua)

hop_qua = HopQua(["Búp bê", "Ô tô", "Sách"])

# "Gọi" hộp quà để nhận quà
mon_qua_1 = hop_qua()  
mon_qua_2 = hop_qua()
print(mon_qua_1)  # Output: (ví dụ) Búp bê
print(mon_qua_2)  # Output: (ví dụ) Sách
```

Trong ví dụ này:

* `HopQua` là một lớp (class) đại diện cho "Hộp quà".
* Phương thức `__init__` dùng để khởi tạo hộp quà với danh sách quà.
* Phương thức `__call__` được định nghĩa để khi "gọi" đối tượng `hop_qua`, nó sẽ chọn ngẫu nhiên một món quà từ danh sách `self.qua`.

**Lợi ích:**

* **Tạo ra các đối tượng "giống hàm" nhưng có trạng thái:**  Đối tượng có thể lưu trữ thông tin (trạng thái) bên trong và sử dụng thông tin đó mỗi khi được gọi.
* **Triển khai decorator:** Decorator là những hàm đặc biệt dùng để "trang trí" cho các hàm khác, và `__call__` rất hữu ích trong việc tạo ra decorator.

**Tóm lại:**

Phương thức `__call__` cho phép bạn tạo ra các đối tượng Python có thể hoạt động như hàm, mở rộng khả năng và tính linh hoạt trong lập trình.


---

###  6. <a name='FromPositionaltoKeyword-OnlyParameters'></a>From Positional to Keyword-Only Parameters

Python nổi tiếng với sự linh hoạt trong việc xử lý tham số của hàm. Bài này sẽ tập trung vào hai khía cạnh quan trọng:

* **Tham số theo vị trí (Positional arguments):** Đây là kiểu tham số truyền thống, giá trị được gán cho tham số dựa trên thứ tự khi gọi hàm.
* **Tham số chỉ theo từ khóa (Keyword-only arguments):**  Kiểu tham số này chỉ có thể được truyền bằng cách chỉ định tên tham số khi gọi hàm, giúp code rõ ràng hơn và tránh nhầm lẫn.

**Ví dụ:**

```python
def chao_mung(ten, loi_chao="Xin chào"):
    """Hàm chào mừng với tham số chỉ theo từ khóa."""
    print(f"{loi_chao}, {ten}!")

chao_mung("Linh")  # Output: Xin chào, Linh!
chao_mung("Nam", loi_chao="Chào bạn")  # Output: Chào bạn, Nam!
```

Trong ví dụ này:

* `ten` là tham số theo vị trí, bắt buộc phải truyền khi gọi hàm.
* `loi_chao` là tham số chỉ theo từ khóa, có giá trị mặc định là "Xin chào". Bạn có thể truyền giá trị khác bằng cách chỉ định tên tham số (`loi_chao="Chào bạn"`).

**Lợi ích của tham số chỉ theo từ khóa:**

* **Tăng tính rõ ràng:**  Khi gọi hàm với nhiều tham số, việc chỉ định tên tham số giúp code dễ đọc và hiểu hơn.
* **Tránh nhầm lẫn:**  Thứ tự tham số không quan trọng, giảm thiểu lỗi do truyền sai thứ tự.
* **Tăng tính linh hoạt:**  Bạn có thể thêm các tham số mới vào hàm mà không làm hỏng code cũ.

**Ký hiệu `*` và `**`:**

Python sử dụng `*` và `**` để xử lý tham số linh hoạt hơn:

* `*args`:  Nắm bắt tất cả các tham số theo vị trí còn lại và lưu chúng vào một tuple.
* `**kwargs`: Nắm bắt tất cả các tham số theo từ khóa còn lại và lưu chúng vào một dictionary.

**Ví dụ:**

```python
def in_thong_tin(*args, **kwargs):
    """Hàm in thông tin với *args và **kwargs."""
    print("Tham số theo vị trí:", args)
    print("Tham số theo từ khóa:", kwargs)

in_thong_tin(1, 2, 3, ten="Linh", tuoi=20)
# Output:
# Tham số theo vị trí: (1, 2, 3)
# Tham số theo từ khóa: {'ten': 'Linh', 'tuoi': 20}
```

**Tạo tham số chỉ theo từ khóa:**

Để tạo tham số chỉ theo từ khóa, bạn đặt một dấu `*` trước tham số đó trong định nghĩa hàm:

```python
def tinh_tong(a, *, b):
    """Hàm tính tổng với b là tham số chỉ theo từ khóa."""
    return a + b

print(tinh_tong(1, b=2))  # Output: 3
```

**Lưu ý:**

* Tham số chỉ theo từ khóa không nhất thiết phải có giá trị mặc định.
* Bạn có thể kết hợp các kiểu tham số khác nhau trong cùng một hàm.

####  6.1. <a name='Positional-OnlyParameters'></a>Positional-Only Parameters

Kể từ Python 3.8, bạn có thể chỉ định **tham số chỉ vị trí** trong các hàm do người dùng định nghĩa. Điều này có nghĩa là khi gọi hàm, bạn **bắt buộc phải truyền đối số theo đúng thứ tự**, không được sử dụng tên tham số như với tham số theo từ khóa.

**Cú pháp:** Sử dụng ký tự `/` trong danh sách tham số để phân biệt tham số chỉ vị trí. Các tham số đứng **trước `/`** sẽ là chỉ vị trí.

**Ví dụ 1: Hàm `divmod`**

```python
def divmod(a, b, /):
  """
  Hàm này trả về thương số và số dư của phép chia a cho b.
  """
  return (a // b, a % b)

print(divmod(10, 3))  # Hợp lệ, in ra (3, 1)
print(divmod(a=10, b=3))  # Lỗi! TypeError: divmod() takes no keyword arguments
```

Trong ví dụ này, `a` và `b` là tham số chỉ vị trí. Bạn chỉ có thể gọi hàm bằng cách truyền giá trị trực tiếp theo thứ tự, ví dụ `divmod(10, 3)`. Việc sử dụng từ khóa như `divmod(a=10, b=3)` sẽ gây ra lỗi.

**Ví dụ 2: Hàm `tag`**

```python
def tag(name, /, *content, class_=None, **attrs):
  """
  Hàm này tạo ra một thẻ HTML.
  """
  if class_ is not None:
    attrs['class'] = class_
  attr_str = ''.join(f' {attr}="{value}"' for attr, value in sorted(attrs.items()))
  if content:
    return f"<{name}{attr_str}>{''.join(content)}</{name}>"
  else:
    return f"<{name}{attr_str} />"

print(tag('p', 'hello', 'world'))  # Hợp lệ, in ra <p>helloworld</p>
print(tag(name='p', 'hello', 'world'))  # Lỗi! TypeError: tag() got some positional-only arguments passed as keyword arguments
print(tag('p', 'hello', 'world', class_='sidebar'))  # Hợp lệ, in ra <p class="sidebar">helloworld</p>
print(tag('p', 'hello', 'world', id='main'))  # Hợp lệ, in ra <p id="main">helloworld</p>
```

Ở đây, `name` là tham số chỉ vị trí. `content`, `class_` và `attrs` là các tham số thông thường. 

**Lợi ích của tham số chỉ vị trí:**

* **Tăng tính rõ ràng:**  Nó giúp người đọc code dễ dàng hiểu cách sử dụng hàm.
* **Linh hoạt trong việc thay đổi tên tham số:**  Bạn có thể thay đổi tên tham số chỉ vị trí mà không ảnh hưởng đến code gọi hàm.
* **Tối ưu hóa hiệu suất:**  Trong một số trường hợp, việc sử dụng tham số chỉ vị trí có thể giúp cải thiện hiệu suất của hàm.

---

###  7. <a name='PackagesforFunctionalProgramming'></a>Packages for Functional Programming
####  7.1. <a name='TheoperatorModule'></a>The operator Module

Module `operator` trong Python cung cấp một tập hợp các hàm tương đương với các toán tử thông thường. Điều này cho phép bạn sử dụng các toán tử như những hàm số, giúp cho việc lập trình hàm trở nên thuận tiện hơn.

**1. Tại sao cần `operator`?**

Trong lập trình hàm, đôi khi bạn cần sử dụng một toán tử như một hàm số. Ví dụ, khi bạn muốn tính giai thừa bằng `reduce`, bạn cần một hàm để nhân hai số. Thay vì viết một hàm `lambda` đơn giản như `lambda a, b: a*b`, bạn có thể sử dụng hàm `mul` từ module `operator`.

**Ví dụ:** Tính giai thừa bằng `reduce` và `operator.mul`

```python
from functools import reduce
from operator import mul

def factorial(n):
  return reduce(mul, range(1, n+1))

print(factorial(5))  # Output: 120
```

**2. `itemgetter` và `attrgetter`**

`operator` cũng cung cấp hai hàm hữu ích là `itemgetter` và `attrgetter` để lấy dữ liệu từ các đối tượng.

* **`itemgetter`**: Trả về một hàm lấy ra phần tử từ một chuỗi hoặc ánh xạ dựa trên chỉ mục.

**Ví dụ:** Sắp xếp danh sách tuple theo mã quốc gia

```python
from operator import itemgetter

metro_data = [
    ('Tokyo', 'JP', 36.933),
    ('Delhi NCR', 'IN', 21.935),
    ('Mexico City', 'MX', 20.142),
]

for city in sorted(metro_data, key=itemgetter(1)):
  print(city)
```

Kết quả:

```
('Delhi NCR', 'IN', 21.935)
('Tokyo', 'JP', 36.933)
('Mexico City', 'MX', 20.142)
```

* **`attrgetter`**: Trả về một hàm lấy ra thuộc tính của một đối tượng dựa trên tên thuộc tính.

**Ví dụ:** Lấy tên và dân số của các thành phố

```python
from collections import namedtuple
from operator import attrgetter

Metropolis = namedtuple('Metropolis', 'name pop')
metro_areas = [Metropolis('Tokyo', 36.933), Metropolis('Delhi NCR', 21.935)]

name_pop = attrgetter('name', 'pop')
for city in metro_areas:
  print(name_pop(city))
```

Kết quả:

```
('Tokyo', 36.933)
('Delhi NCR', 21.935)
```

**3. `methodcaller`**

`methodcaller` tạo ra một hàm gọi một phương thức cụ thể trên một đối tượng.

**Ví dụ:** Chuyển đổi chuỗi thành chữ hoa

```python
from operator import methodcaller

s = 'hello world'
upcase = methodcaller('upper')
print(upcase(s))  # Output: HELLO WORLD
```

**Tóm lại,** module `operator` cung cấp các hàm tiện lợi giúp cho việc lập trình hàm trong Python trở nên dễ dàng và hiệu quả hơn. Nó giúp bạn tránh phải viết các hàm `lambda` đơn giản, đồng thời cung cấp các công cụ mạnh mẽ để làm việc với dữ liệu.

####  7.2. <a name='FreezingArgumentswithfunctools.partial'></a>Freezing Arguments with functools.partial

Module `functools` cung cấp một số hàm bậc cao (higher-order functions). Chúng ta đã thấy `reduce` trong “Modern Replacements for map, filter, and reduce” ở trang 235. Một hàm khác là `partial`: với một hàm có thể gọi được (callable), nó tạo ra một hàm có thể gọi được mới với một số đối số của hàm ban đầu được liên kết với các giá trị được xác định trước. Điều này hữu ích để điều chỉnh một hàm nhận một hoặc nhiều đối số cho một API yêu cầu một hàm gọi lại (callback) với ít đối số hơn.


**Ví dụ 7-16.** Sử dụng `partial` để sử dụng hàm hai đối số trong trường hợp yêu cầu hàm có thể gọi được một đối số

```python
>>> from operator import mul
>>> from functools import partial
>>> triple = partial(mul, 3)  # Tạo hàm triple mới từ mul, liên kết đối số vị trí đầu tiên với 3.
>>> triple(7)  # Kiểm tra nó.
21
>>> list(map(triple, range(1, 10)))  # Sử dụng triple với map; mul sẽ không hoạt động với map trong ví dụ này.
[3, 6, 9, 12, 15, 18, 21, 24, 27]
```

Một ví dụ hữu ích hơn liên quan đến hàm `unicode.normalize` mà chúng ta đã thấy trong “Normalizing Unicode for Reliable Comparisons” ở trang 140. Nếu bạn làm việc với văn bản từ nhiều ngôn ngữ, bạn có thể muốn áp dụng `unicode.normalize('NFC', s)` cho bất kỳ chuỗi `s` nào trước khi so sánh hoặc lưu trữ nó. Nếu bạn làm điều đó thường xuyên, thật tiện lợi khi có một hàm `nfc` để làm như vậy, như trong Ví dụ 7-17.

**Ví dụ 7-17.** Xây dựng một hàm chuẩn hóa Unicode tiện lợi với `partial`

```python
>>> import unicodedata, functools
>>> nfc = functools.partial(unicodedata.normalize, 'NFC')
>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> s1, s2
('café', 'café')
>>> s1 == s2
False
>>> nfc(s1) == nfc(s2)
True
```

`partial` nhận một hàm có thể gọi được làm đối số đầu tiên, theo sau là một số lượng tùy ý các đối số vị trí và từ khóa để liên kết.

Ví dụ 7-18 cho thấy việc sử dụng `partial` với hàm `tag` từ Ví dụ 7-9, để đóng băng một đối số vị trí và một đối số từ khóa.

**Ví dụ 7-18.** Demo về `partial` được áp dụng cho hàm `tag` từ Ví dụ 7-9

```python
>>> from tagger import tag  # Nhập tag từ Ví dụ 7-9 và hiển thị ID của nó.
>>> tag
<function tag at 0x10206d1e0>
>>> from functools import partial
>>> picture = partial(tag, 'img', class_='pic-frame')  # Tạo hàm picture từ tag bằng cách cố định đối số vị trí đầu tiên bằng 'img' và đối số từ khóa class_ bằng 'pic-frame'.
>>> picture(src='wumpus.jpeg')  # picture hoạt động như mong đợi.
'<img class="pic-frame" src="wumpus.jpeg" />'
>>> picture
functools.partial(<function tag at 0x10206d1e0>, 'img', class_='pic-frame')  # partial() trả về một đối tượng functools.partial.
>>> picture.func  # Một đối tượng functools.partial có các thuộc tính cung cấp quyền truy cập vào hàm ban đầu và các đối số cố định.
<function tag at 0x10206d1e0>
>>> picture.args
('img',)
>>> picture.keywords
{'class_': 'pic-frame'}
```

Hàm `functools.partialmethod` thực hiện công việc tương tự như `partial`, nhưng được thiết kế để hoạt động với các phương thức.

Module `functools` cũng bao gồm các hàm bậc cao được thiết kế để sử dụng làm trình trang trí hàm (function decorators), chẳng hạn như `cache` và `singledispatch`, cùng những hàm khác. Những hàm đó được đề cập trong Chương 9, cũng giải thích cách triển khai các trình trang trí tùy chỉnh.
