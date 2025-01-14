---
layout: post
title: "[Fluent python] Chapter 6. Object reference, Mutability and Recycling"
date: 2025-01-14 10:00:00 +0700
categories: fluent python
---

Tưởng tượng mỗi **variable** (biến) như một cái nhãn dán chứ không phải cái hộp. Nhãn dán này được dùng để dán lên các **object** (đối tượng). 

Vậy nên, khi ta gán một biến cho một biến khác, ta chỉ đơn giản là dán thêm một nhãn lên cùng một đối tượng đó, chứ không phải tạo ra một đối tượng mới. Đây gọi là **aliasing** (bí danh).

Điều thú vị là **tuple** (bộ) tuy **immutable** (bất biến) nhưng giá trị bên trong nó vẫn có thể thay đổi nếu chứa các đối tượng **mutable** (có thể thay đổi) như list. Vì vậy, cần phân biệt **shallow copy** (sao chép nông) và **deep copy** (sao chép sâu).

Đoạn văn cũng đề cập đến các vấn đề liên quan đến tham chiếu khi truyền tham số cho hàm, đặc biệt là với các tham số **mutable** (có thể thay đổi) và cách xử lý chúng an toàn.

Cuối cùng là **garbage collection** (thu gom rác), lệnh **del** và một số thủ thuật Python áp dụng với các đối tượng **immutable** (bất biến).

### Table of contents
1. [Variables Are Not Boxes](#VariablesAreNotBoxes)
2. [Identity, Equality, and Aliases](#IdentityEqualityandAliases)
  * 2.1. [Choosing Between == and is](#ChoosingBetweenandis)
  * 2.2. [The Relative Immutability of Tuples](#TheRelativeImmutabilityofTuples)
3. [Copies Are Shallow by Default](#CopiesAreShallowbyDefault)
  * 3.1. [Deep and Shallow Copies of Arbitrary Objects](#DeepandShallowCopiesofArbitraryObjects)
4. [Function Parameters as References](#FunctionParametersasReferences)
  * 4.1. [Mutable Types as Parameter Defaults: Bad Idea](#MutableTypesasParameterDefaults:BadIdea)
  * 4.2. [Defensive Programming with Mutable Parameters](#DefensiveProgrammingwithMutableParameters)
5. [del and Garbage Collection](#delandGarbageCollection)
6. [Tricks Python Plays with Immutables](#TricksPythonPlayswithImmutables)

---
###  1. <a name='VariablesAreNotBoxes'></a>Variables Are Not Boxes

**1. Phép ẩn dụ "biến là hộp" là sai lầm:**

* Quan niệm truyền thống về biến như những chiếc hộp chứa đựng giá trị không chính xác trong Python. 
* Thay vào đó, biến trong Python hoạt động giống như "nhãn dán" (sticky notes) được gắn vào các đối tượng.

**2. Biến như "nhãn dán":**

* Khi bạn gán một giá trị cho một biến, bạn không sao chép giá trị đó vào biến. 
* Thay vào đó, bạn đang dán nhãn đó vào đối tượng chứa giá trị. 
* Nhiều biến có thể được gắn vào cùng một đối tượng.

**3. Ví dụ minh họa:**

```python
a = [1, 2, 3]  # Tạo một danh sách và dán nhãn "a" vào nó.
b = a          # Dán nhãn "b" vào cùng đối tượng với "a".
a.append(4)    # Thay đổi đối tượng bằng cách thêm 4 vào danh sách.
print(b)       # In ra [1, 2, 3, 4] - cả a và b đều trỏ đến cùng một danh sách.
```

* Nếu "a" và "b" là các hộp riêng biệt, việc thay đổi "a" sẽ không ảnh hưởng đến "b". 
* Tuy nhiên, vì cả hai đều là nhãn dán trên cùng một đối tượng, nên thay đổi đối tượng thông qua "a" sẽ được phản ánh khi truy cập thông qua "b".

**4. "Bind" thay vì "Assign":**

* Đoạn dịch đề xuất sử dụng thuật ngữ "bind" (ràng buộc) thay vì "assign" (gán) để mô tả chính xác hơn mối quan hệ giữa biến và đối tượng.
* Biến được "ràng buộc" với đối tượng, nghĩa là nó được liên kết với đối tượng đó.

**5. Vế phải được thực hiện trước:**

* Trong câu lệnh gán, vế phải luôn được thực hiện trước. 
* Đối tượng được tạo hoặc truy xuất trước, sau đó biến mới được ràng buộc với đối tượng đó.

**Tóm lại:**

Hiểu rõ cách thức hoạt động của biến trong Python là rất quan trọng. Phép ẩn dụ "nhãn dán" giúp hình dung rõ hơn về **reference variables** và tránh nhầm lẫn khi làm việc với các đối tượng có thể thay đổi (mutable) như danh sách.


---
###  2. <a name='IdentityEqualityandAliases'></a>Identity, Equality, and Aliases

**1. Đồng nhất (Identity)**

* Hai biến **đồng nhất** khi chúng cùng tham chiếu đến **cùng một đối tượng** trong bộ nhớ.
* Kiểm tra đồng nhất bằng toán tử `is` hoặc hàm `id()`. 
    * `a is b` trả về `True` nếu `a` và `b` cùng trỏ đến một đối tượng.
    * `id(a)` trả về một số nguyên duy nhất đại diện cho địa chỉ bộ nhớ của đối tượng mà `a` tham chiếu.

**Ví dụ:**

```python
a = [1, 2, 3]
b = a
print(a is b)  # Output: True
print(id(a) == id(b))  # Output: True
```

Trong ví dụ này, `a` và `b` là **đồng nhất** vì cả hai đều trỏ đến cùng một danh sách trong bộ nhớ.

**2. Bằng nhau (Equality)**

* Hai biến **bằng nhau** khi chúng có **cùng giá trị**, nhưng có thể tham chiếu đến các đối tượng khác nhau trong bộ nhớ.
* Kiểm tra bằng nhau bằng toán tử `==`.

**Ví dụ:**

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # Output: True
print(a is b)  # Output: False
```

Ở đây, `a` và `b` **bằng nhau** vì chúng chứa cùng giá trị, nhưng chúng **không đồng nhất** vì mỗi biến trỏ đến một danh sách riêng biệt trong bộ nhớ.

**3. Biệt danh (Aliases)**

* **Biệt danh** là hai hoặc nhiều biến cùng tham chiếu đến cùng một đối tượng. Nói cách khác, chúng là những tên gọi khác nhau cho cùng một thứ.
* Trong ví dụ đầu tiên ở trên, `b` là **biệt danh** của `a`.

Hiểu rõ sự khác biệt này rất quan trọng khi làm việc với các đối tượng có thể thay đổi (mutable) trong Python, vì thay đổi đối tượng thông qua một biến sẽ ảnh hưởng đến tất cả các biến khác cùng trỏ đến nó.

####  2.1. <a name='ChoosingBetweenandis'></a>Choosing Between == and is

Trong Python, cả `==` và `is` đều được sử dụng để so sánh, nhưng chúng thực hiện việc so sánh theo những cách khác nhau.

**1. Toán tử `==` (so sánh giá trị)**

Toán tử `==` so sánh **giá trị** của hai đối tượng. Nói cách khác, nó kiểm tra xem hai đối tượng có chứa dữ liệu giống nhau hay không.

**Ví dụ:**

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # Output: True (vì a và b chứa cùng giá trị)

c = "hello"
d = "hello"
print(c == d)  # Output: True (vì c và d chứa cùng giá trị)
```

**2. Toán tử `is` (so sánh bản sắc)**

Toán tử `is` so sánh **bản sắc** của hai đối tượng.  Nó kiểm tra xem hai biến có cùng trỏ đến một đối tượng trong bộ nhớ hay không. Mỗi đối tượng trong Python đều có một ID duy nhất, và toán tử `is` so sánh các ID này.

**Ví dụ:**

```python
a = [1, 2, 3]
b = a
print(a is b)  # Output: True (vì a và b cùng trỏ đến một đối tượng)

c = [1, 2, 3]
d = [1, 2, 3]
print(c is d)  # Output: False (vì c và d là hai đối tượng khác nhau, mặc dù có cùng giá trị)
```

**3. Khi nào nên sử dụng `is`?**

Mặc dù `==` được sử dụng phổ biến hơn, có một số trường hợp `is` là lựa chọn tốt hơn:

* **So sánh với `None`:** Kiểm tra xem một biến có giá trị là `None` hay không là một trường hợp phổ biến để sử dụng `is`.  
   ```python
   x = None
   if x is None:
       print("x là None")
   ```

* **Singleton:**  Singleton là các đối tượng mà chỉ có một thể hiện duy nhất trong chương trình.  `is` thường được sử dụng để kiểm tra xem một biến có trỏ đến một singleton cụ thể hay không.

   ```python
   class Singleton:
       _instance = None
       def __new__(cls):
           if not cls._instance:
               cls._instance = super(Singleton, cls).__new__(cls)
           return cls._instance

   a = Singleton()
   b = Singleton()
   print(a is b)  # Output: True (vì a và b cùng trỏ đến singleton duy nhất)
   ```

**4. `is` vs `==` với các kiểu dữ liệu khác nhau**

* **Số nguyên nhỏ:**  Python tối ưu hóa việc lưu trữ các số nguyên nhỏ (thường từ -5 đến 256),  do đó, các biến có cùng giá trị số nguyên nhỏ sẽ trỏ đến cùng một đối tượng trong bộ nhớ.

   ```python
   a = 100
   b = 100
   print(a is b)  # Output: True
   ```

* **Chuỗi:**  Đối với các chuỗi ngắn và bất biến, Python cũng có thể tối ưu hóa bằng cách sử dụng cùng một đối tượng trong bộ nhớ cho các chuỗi giống nhau. Tuy nhiên, điều này không phải lúc nào cũng đúng, đặc biệt là với các chuỗi dài hoặc được tạo động.

   ```python
   a = "hello"
   b = "hello"
   print(a is b)  # Output: True (có thể thay đổi tùy thuộc vào môi trường)
   ```

* **List, Tuple, Dictionary:**  Các kiểu dữ liệu này luôn tạo ra các đối tượng mới, ngay cả khi chúng có cùng giá trị.

   ```python
   a = [1, 2, 3]
   b = [1, 2, 3]
   print(a is b)  # Output: False
   ```

**5. Tóm lại**

* Sử dụng `==` khi bạn muốn so sánh giá trị của hai đối tượng.
* Sử dụng `is` khi bạn muốn kiểm tra xem hai biến có trỏ đến cùng một đối tượng trong bộ nhớ hay không.
* `is` thường được sử dụng để so sánh với `None` và kiểm tra singleton.

####  2.2. <a name='TheRelativeImmutabilityofTuples'></a>The Relative Immutability of Tuples

Tuple trong Python được biết đến là một kiểu dữ liệu bất biến (immutable). Điều này có nghĩa là một khi tuple đã được tạo, bạn không thể thay đổi nội dung của nó. Tuy nhiên, có một sự thật thú vị là tính bất biến này chỉ áp dụng cho cấu trúc của tuple, chứ không hoàn toàn áp dụng cho các đối tượng mà nó chứa.

Hãy tưởng tượng tuple như một hộp đựng đồ. Khi bạn đã đóng gói hộp, bạn không thể thay đổi vị trí các ngăn trong hộp hay thêm/bớt ngăn. Tuy nhiên, nếu trong hộp có chứa những vật dụng có thể thay đổi (như một túi đất sét), thì hình dạng của túi đất sét có thể thay đổi mà không ảnh hưởng đến cấu trúc của hộp.

**Ví dụ 1:**

```python
my_tuple = (1, 2, [3, 4])  # Tuple chứa một list (list là mutable)

print(my_tuple)  # Output: (1, 2, [3, 4])

my_tuple[2].append(5)  # Thay đổi list bên trong tuple

print(my_tuple)  # Output: (1, 2, [3, 4, 5]) 
```

Trong ví dụ này, mặc dù `my_tuple` là một tuple (bất biến), nhưng nó chứa một list (có thể thay đổi).  Vì vậy, ta có thể thay đổi nội dung của list mà không gặp lỗi.  

**Tại sao lại như vậy?**

Tuple lưu trữ các **tham chiếu** đến các đối tượng, chứ không phải bản sao của các đối tượng đó. Khi bạn thay đổi một đối tượng mutable được tham chiếu bởi tuple, bản thân tuple không thay đổi (vẫn giữ nguyên các tham chiếu), nhưng đối tượng được tham chiếu đó đã thay đổi.

**Ví dụ 2:**

```python
a = [1, 2]
b = (a, 3)  # Tuple b chứa tham chiếu đến list a

print(b)  # Output: ([1, 2], 3)

a.append(4)  # Thay đổi list a

print(b)  # Output: ([1, 2, 4], 3)
```

**Lưu ý:**

* Các kiểu dữ liệu như `str`, `bytes` và `array.array` là bất biến hoàn toàn vì chúng lưu trữ giá trị trực tiếp trong bộ nhớ, không phải tham chiếu.

**Kết luận:**

Tuple trong Python có tính bất biến tương đối.  Cấu trúc của tuple là bất biến, nhưng các đối tượng mutable được tham chiếu bởi tuple vẫn có thể thay đổi.  Điều này có thể gây ra một số nhầm lẫn, vì vậy hãy cẩn thận khi làm việc với tuple chứa các đối tượng mutable.


---
###  3. <a name='CopiesAreShallowbyDefault'></a>Copies Are Shallow by Default

Hãy tưởng tượng bạn có một hộp quà (list) chứa các món quà khác nhau: một quyển sách (immutable - không thể thay đổi), một hộp bút chì màu (mutable - có thể thay đổi) và một con gấu bông (cũng mutable).

**Sao chép nông** giống như bạn chụp ảnh hộp quà này. Bức ảnh (bản sao) trông giống hệt hộp quà gốc, nhưng thực chất chỉ là hình ảnh (tham chiếu) của các món quà bên trong. 

**Ví dụ:**

```python
hop_qua_goc = ["sách", ["bút chì đỏ", "bút chì xanh"], "gấu bông"]
hop_qua_sao_chep = list(hop_qua_goc) 

# Thay đổi hộp quà gốc
hop_qua_goc.append("ô tô")  # Thêm "ô tô" vào hộp quà gốc
hop_qua_goc[1].remove("bút chì xanh")  # Lấy "bút chì xanh" ra khỏi hộp bút chì

print(hop_qua_goc)  # Output: ['sách', ['bút chì đỏ'], 'gấu bông', 'ô tô']
print(hop_qua_sao_chep)  # Output: ['sách', ['bút chì đỏ'], 'gấu bông']
```

**Giải thích:**

* `hop_qua_sao_chep` là bản sao nông của `hop_qua_goc`.
* Khi thêm "ô tô" vào `hop_qua_goc`, `hop_qua_sao_chep` không thay đổi vì nó chỉ là "hình ảnh" của hộp quà ban đầu.
* Tuy nhiên, khi lấy "bút chì xanh" ra khỏi hộp bút chì trong `hop_qua_goc`, `hop_qua_sao_chep` cũng bị ảnh hưởng. Vì cả hai hộp quà đều "nhìn" vào cùng một hộp bút chì.

**Tóm lại:**

Sao chép nông chỉ tạo ra một bản sao mới của "hộp quà", nhưng các "món quà" bên trong vẫn được chia sẻ giữa bản gốc và bản sao. Điều này có thể gây ra những thay đổi không mong muốn nếu "món quà" là mutable (có thể thay đổi).

**Lưu ý:**

* Các kiểu dữ liệu immutable trong Python bao gồm: số (int, float), chuỗi (str), tuple.
* Các kiểu dữ liệu mutable bao gồm: list, dictionary, set.


####  3.1. <a name='DeepandShallowCopiesofArbitraryObjects'></a>Deep and Shallow Copies of Arbitrary Objects

Tiếp tục với ví dụ hộp quà, **sao chép sâu** giống như bạn mua một hộp quà mới hoàn toàn và mua lại tất cả các món quà giống hệt như trong hộp quà gốc. Lúc này, hai hộp quà hoàn toàn độc lập với nhau. 

**Ví dụ:**

```python
import copy

hop_qua_goc = ["sách", ["bút chì đỏ", "bút chì xanh"], "gấu bông"]
hop_qua_sao_chep = copy.deepcopy(hop_qua_goc)

# Thay đổi hộp quà gốc
hop_qua_goc.append("ô tô")  # Thêm "ô tô" vào hộp quà gốc
hop_qua_goc[1].remove("bút chì xanh")  # Lấy "bút chì xanh" ra khỏi hộp bút chì

print(hop_qua_goc)  # Output: ['sách', ['bút chì đỏ'], 'gấu bông', 'ô tô']
print(hop_qua_sao_chep)  # Output: ['sách', ['bút chì đỏ', 'bút chì xanh'], 'gấu bông']
```

**Giải thích:**

* `hop_qua_sao_chep` là bản sao sâu của `hop_qua_goc`.
* Khi thêm "ô tô" vào `hop_qua_goc`, `hop_qua_sao_chep` không thay đổi vì nó là một hộp quà hoàn toàn khác biệt.
* Khi lấy "bút chì xanh" ra khỏi hộp bút chì trong `hop_qua_goc`, `hop_qua_sao_chep` cũng không bị ảnh hưởng. Vì hộp bút chì trong `hop_qua_sao_chep` là một hộp bút chì khác, độc lập với hộp bút chì trong `hop_qua_goc`.

**Tóm lại:**

Sao chép sâu tạo ra một bản sao hoàn toàn mới, bao gồm cả "hộp quà" và tất cả các "món quà" bên trong. Mọi thay đổi trên bản gốc sẽ không ảnh hưởng đến bản sao và ngược lại.

**Khi nào nên dùng sao chép sâu?**

* Khi bạn muốn tạo ra một bản sao hoàn toàn độc lập với bản gốc.
* Khi bạn làm việc với các đối tượng phức tạp có nhiều lớp lồng nhau.
* Khi bạn muốn tránh những thay đổi không mong muốn do việc chia sẻ dữ liệu giữa các đối tượng.

**Lưu ý:**

* Sử dụng `copy.deepcopy()` từ module `copy` để tạo bản sao sâu.
* Sao chép sâu có thể tốn nhiều tài nguyên hơn sao chép nông, đặc biệt là với các đối tượng lớn.
 
---
###  4. <a name='FunctionParametersasReferences'></a>Function Parameters as References

Trong Python, việc truyền tham số cho hàm hoạt động theo cơ chế gọi là "**call by sharing**". Nói một cách đơn giản, nó giống như việc bạn đưa cho bạn bè **chìa khóa nhà** của mình chứ không phải đưa cả căn nhà. 

**Giải thích chi tiết:**

* Khi bạn gọi một hàm và truyền tham số, Python sẽ tạo ra một bản sao của "chìa khóa" (tham chiếu) đến đối tượng mà bạn truyền vào. 
* Bên trong hàm, bạn có thể sử dụng "chìa khóa" này để truy cập và thay đổi đối tượng gốc. 
* Tuy nhiên, bạn không thể thay đổi "chìa khóa" này để trỏ đến một "ngôi nhà" (đối tượng) khác.

**Ví dụ minh họa:**

```python
def thay_doi_danh_sach(danh_sach):
  """Hàm này thêm một phần tử vào danh sách."""
  danh_sach.append(4)

danh_sach_cua_toi = [1, 2, 3]
thay_doi_danh_sach(danh_sach_cua_toi)
print(danh_sach_cua_toi)  # Output: [1, 2, 3, 4]
```

**Giải thích:**

1. `danh_sach_cua_toi` là một list chứa các số `[1, 2, 3]`.
2. Khi gọi hàm `thay_doi_danh_sach(danh_sach_cua_toi)`, Python tạo ra một bản sao "chìa khóa" đến `danh_sach_cua_toi` và đưa cho tham số `danh_sach` bên trong hàm.
3. Bên trong hàm, `danh_sach` sử dụng "chìa khóa" này để thêm số `4` vào list gốc.
4. Do đó, `danh_sach_cua_toi` bên ngoài hàm cũng bị thay đổi.

**So sánh với Call by Value:**

Một số ngôn ngữ lập trình khác sử dụng cơ chế "**call by value**", giống như việc bạn đưa cho bạn bè **bản sao của cả căn nhà**.  Trong trường hợp này, mọi thay đổi bạn thực hiện bên trong hàm sẽ chỉ ảnh hưởng đến "bản sao nhà", không ảnh hưởng đến "nhà" gốc.

**Lưu ý quan trọng:**

* **Đối tượng mutable (có thể thay đổi) như list, dictionary**: Khi truyền làm tham số, hàm có thể thay đổi nội dung của đối tượng gốc.
* **Đối tượng immutable (không thể thay đổi) như số, chuỗi, tuple**: Khi truyền làm tham số, hàm không thể thay đổi giá trị của đối tượng gốc.

**Tóm lại:**

Hiểu rõ cơ chế "call by sharing" trong Python là rất quan trọng để tránh những lỗi bất ngờ khi làm việc với hàm và tham số.


####  4.1. <a name='MutableTypesasParameterDefaults:BadIdea'></a>Mutable Types as Parameter Defaults: Bad Idea

Python cho phép chúng ta định nghĩa giá trị mặc định cho các tham số trong hàm. Điều này rất tiện lợi, nhưng cũng tiềm ẩn nguy cơ khi sử dụng **kiểu dữ liệu có thể thay đổi (mutable)** làm giá trị mặc định.

**Tại sao lại nguy hiểm?**

Vấn đề nằm ở chỗ giá trị mặc định chỉ được tạo **một lần duy nhất** khi hàm được định nghĩa, chứ không phải mỗi khi hàm được gọi.  

Hãy tưởng tượng bạn có một chiếc hộp bút chì (list) dùng chung cho cả lớp. Mỗi khi có học sinh mới vào lớp mà không mang bút chì, họ sẽ được lấy bút chì từ hộp bút chung này.

```python
def them_hoc_sinh(danh_sach_lop=[], hoc_sinh_moi="An"):
  """Thêm học sinh mới vào danh sách lớp."""
  danh_sach_lop.append(hoc_sinh_moi)
  return danh_sach_lop

print(them_hoc_sinh())  # Output: ['An']
print(them_hoc_sinh(hoc_sinh_moi="Bình"))  # Output: ['An', 'Bình'] 
print(them_hoc_sinh())  # Output: ['An', 'Bình', 'An'] 
```

**Giải thích:**

1. Lần gọi `them_hoc_sinh()` đầu tiên, `danh_sach_lop` là `[]` (hộp bút rỗng), sau đó thêm "An" vào.
2. Lần gọi thứ hai, ta chỉ định `hoc_sinh_moi="Bình"`, hàm hoạt động bình thường.
3. **Lần gọi thứ ba**, ta lại không truyền `danh_sach_lop`. Lúc này, thay vì tạo một list mới, hàm lại sử dụng **cùng list đã được tạo ở lần gọi đầu tiên**. Do đó, "An" được thêm vào một lần nữa, mặc dù ta không hề mong muốn điều này.

**Hậu quả:**

* Các lời gọi hàm có thể ảnh hưởng lẫn nhau một cách khó lường.
* Gây ra lỗi khó debug, đặc biệt trong các chương trình lớn.

**Cách khắc phục:**

* Sử dụng `None` làm giá trị mặc định.
* Kiểm tra `None` bên trong hàm và tạo đối tượng mới nếu cần.

```python
def them_hoc_sinh(danh_sach_lop=None, hoc_sinh_moi="An"):
  """Thêm học sinh mới vào danh sách lớp."""
  if danh_sach_lop is None:
    danh_sach_lop = []  # Tạo list mới mỗi khi hàm được gọi
  danh_sach_lop.append(hoc_sinh_moi)
  return danh_sach_lop
```

**Tóm lại:**

Tránh sử dụng kiểu dữ liệu mutable làm giá trị mặc định cho tham số hàm. Thay vào đó, hãy sử dụng `None` và khởi tạo đối tượng mới bên trong hàm để đảm bảo tính độc lập giữa các lần gọi hàm.


####  4.2. <a name='DefensiveProgrammingwithMutableParameters'></a>Defensive Programming with Mutable Parameters

Khi viết hàm nhận tham số có thể thay đổi (như list, dictionary), cần cẩn trọng xem xét liệu hàm có nên thay đổi đối tượng gốc hay không. Điều này phụ thuộc vào mục đích của hàm và kỳ vọng của người sử dụng hàm.

**Ví dụ:**

Giả sử bạn viết hàm `sap_xep_danh_sach(danh_sach)` để sắp xếp một danh sách. Liệu người dùng có mong muốn danh sách gốc của họ bị thay đổi sau khi gọi hàm? Có thể có, cũng có thể không.

**Lập trình phòng thủ:**

Để tránh những thay đổi ngoài ý muốn, hãy tuân thủ nguyên tắc:

* **Nếu hàm cần thay đổi đối tượng gốc:** Hãy ghi rõ trong tài liệu hàm để người dùng biết.
* **Nếu hàm không cần thay đổi đối tượng gốc:**
    * Tạo một bản sao của đối tượng và thao tác trên bản sao đó.
    * Hoặc sử dụng các phương thức không thay đổi đối tượng gốc (ví dụ: `sorted()` thay vì `.sort()`).

**Minh họa:**

```python
def sap_xep_danh_sach(danh_sach):
  """Sắp xếp danh sách.
  
  Ghi chú: Hàm này thay đổi danh sách gốc.
  """
  danh_sach.sort()

def sap_xep_danh_sach_an_toan(danh_sach):
  """Sắp xếp danh sách mà không thay đổi danh sách gốc."""
  danh_sach_moi = sorted(danh_sach)  # Tạo bản sao và sắp xếp
  return danh_sach_moi
```

**Lợi ích:**

* Tránh gây ra lỗi khó hiểu cho người dùng.
* Tăng tính "an toàn" và dự đoán được của hàm.
* Giảm thiểu rủi ro khi làm việc với dữ liệu quan trọng.

**Tóm lại:**

Hãy luôn suy nghĩ kỹ về tác động của hàm đối với dữ liệu của người dùng. Lập trình phòng thủ giúp bạn viết ra những hàm đáng tin cậy và dễ sử dụng hơn.


---
###  5. <a name='delandGarbageCollection'></a>del and Garbage Collection

Trong Python, việc quản lý bộ nhớ được thực hiện tự động thông qua cơ chế **thu gom rác (garbage collection)**. Nói một cách đơn giản, nó giống như một đội vệ sinh tự động dọn dẹp những "rác" (đối tượng không còn sử dụng) trong bộ nhớ máy tính.

**Câu lệnh `del`:**

`del` không phải là một hàm, mà là một **câu lệnh**. Nó được sử dụng để xóa **tham chiếu** đến một đối tượng, chứ không phải xóa đối tượng đó trực tiếp.

**Ví dụ:**

```python
a = [1, 2, 3]  # Tạo một list và gán cho biến a
b = a          # Biến b cũng tham chiếu đến cùng list đó
del a          # Xóa tham chiếu a
print(b)       # Output: [1, 2, 3] (List vẫn tồn tại vì b vẫn tham chiếu đến nó)
```

**Thu gom rác:**

Khi một đối tượng không còn bất kỳ tham chiếu nào đến nó, nó sẽ trở thành "rác" và được bộ thu gom rác tự động dọn dẹp.

**Ví dụ:**

```python
a = [1, 2, 3]  # Tạo một list
b = a          # b cũng tham chiếu đến list
del a          # Xóa tham chiếu a
b = "hello"    # b bây giờ tham chiếu đến một chuỗi khác
# Lúc này, list [1, 2, 3] không còn tham chiếu nào, 
# nó sẽ được thu gom rác tự động
```

**Phương thức `__del__`:**

Mặc dù hiếm khi sử dụng, Python cung cấp phương thức đặc biệt `__del__` cho phép bạn định nghĩa những hành động cần thực hiện trước khi một đối tượng bị hủy. Tuy nhiên, việc sử dụng `__del__` khá phức tạp và cần thận trọng.

**Tham chiếu yếu (weak reference):**

Python cung cấp `weakref` module cho phép tạo các **tham chiếu yếu**. Tham chiếu yếu không ngăn đối tượng bị thu gom rác. Điều này hữu ích trong các trường hợp như bộ nhớ đệm (cache), nơi bạn không muốn các đối tượng được giữ trong bộ nhớ chỉ vì chúng đang được cache.

Dưới đây là một số ví dụ minh họa cách sử dụng `weakref`:

**Theo dõi sự tồn tại của đối tượng:**

```python
import weakref

class MyObject:
  def __init__(self, name):
    self.name = name

  def __del__(self):
    print(f"Đối tượng {self.name} đã bị hủy.")

obj = MyObject("A")
ref = weakref.ref(obj)

print(ref() is obj)  # Output: True (ref() truy cập đối tượng được tham chiếu)

del obj

print(ref() is None)  # Output: True (Đối tượng đã bị hủy, ref() trả về None)
```

**Cache:**

```python
import weakref

class Cache:
  def __init__(self):
    self._cache = weakref.WeakValueDictionary()

  def get(self, key):
    return self._cache.get(key)

  def set(self, key, value):
    self._cache[key] = value

cache = Cache()
obj = MyObject("B")

cache.set("my_key", obj)
print(cache.get("my_key") is obj)  # Output: True

del obj
print(cache.get("my_key") is None)  # Output: True (Đối tượng đã bị hủy, cache tự động xóa)
```

**Tránh vòng lặp tham chiếu:**

```python
import weakref

class Node:
  def __init__(self, data):
    self.data = data
    self.next = None

node1 = Node(1)
node2 = Node(2)

node1.next = node2
node2.next = weakref.ref(node1)  # Sử dụng weakref để tránh vòng lặp

# ...
```

**Lưu ý:**

* Không phải tất cả các đối tượng đều có thể được tham chiếu yếu.
* `weakref` cung cấp các class và hàm khác nhau để làm việc với tham chiếu yếu, bao gồm `weakref.ref`, `weakref.proxy`, `weakref.WeakKeyDictionary`, và `weakref.WeakValueDictionary`.


**Tóm lại:**

* `del` xóa tham chiếu, không phải đối tượng.
* Bộ thu gom rác tự động dọn dẹp các đối tượng không còn được sử dụng.
* `__del__` cho phép định nghĩa hành động trước khi đối tượng bị hủy.
* Tham chiếu yếu không ngăn đối tượng bị thu gom rác.


---
###  6. <a name='TricksPythonPlayswithImmutables'></a>Tricks Python Plays with Immutables

Python có một số "mánh khóe" thú vị khi làm việc với các kiểu dữ liệu immutable như tuple, str, bytes và frozenset. Mặc dù những điều này không ảnh hưởng đến cách bạn sử dụng Python hàng ngày, nhưng hiểu rõ chúng có thể giúp bạn tránh nhầm lẫn và tối ưu hóa code.

**1. "Sao chép" tuple:**

Khi bạn "sao chép" một tuple bằng cách slicing (`t[:]`) hoặc dùng constructor (`tuple(t)`), Python thực chất không tạo ra một bản sao mới. Thay vào đó, nó chỉ đơn giản là trả về một tham chiếu đến cùng một đối tượng tuple ban đầu.

**Ví dụ:**

```python
t1 = (1, 2, 3)
t2 = t1[:]
t3 = tuple(t1)

print(t1 is t2)  # Output: True (t1 và t2 là cùng một đối tượng)
print(t1 is t3)  # Output: True (t1 và t3 cũng là cùng một đối tượng)
```

**2. Interning:**

Python sử dụng kỹ thuật gọi là "interning" để tối ưu hóa bộ nhớ. Đối với một số đối tượng immutable nhất định (như string literals ngắn hoặc số nguyên nhỏ), Python chỉ lưu trữ một bản sao duy nhất trong bộ nhớ. Mỗi khi bạn tạo ra một đối tượng giống hệt, Python sẽ chỉ đơn giản là tham chiếu đến bản sao đã tồn tại.

**Ví dụ:**

```python
s1 = "hello"
s2 = "hello"

print(s1 is s2)  # Output: True (s1 và s2 tham chiếu đến cùng một đối tượng string)
```

**3. `frozenset.copy()`:**

Phương thức `copy()` của `frozenset` cũng là một "mánh khóe". Nó không thực sự tạo ra một bản sao mới mà chỉ trả về tham chiếu đến chính `frozenset` ban đầu.

**Lý do:**

* **Tối ưu hóa bộ nhớ:** Tránh lãng phí bộ nhớ bằng cách không tạo ra các bản sao không cần thiết.
* **Tăng hiệu suất:** Giảm thời gian xử lý bằng cách sử dụng lại các đối tượng đã tồn tại.
* **Đảm bảo tính bất biến:** Vì các đối tượng immutable không thể thay đổi, nên việc chia sẻ chúng không gây ra vấn đề gì.

**Lưu ý:**

* Những "mánh khóe" này là chi tiết triển khai nội bộ của Python và có thể thay đổi trong tương lai.
* Không nên dựa vào chúng để viết code.
* Luôn sử dụng `==` để so sánh giá trị của các đối tượng, thay vì `is` (dùng để so sánh identity).

**Tóm lại:**

Python áp dụng một số tối ưu hóa ngầm với các kiểu dữ liệu immutable. Hiểu rõ những điều này giúp bạn tránh nhầm lẫn và viết code hiệu quả hơn. Tuy nhiên, đừng quá phụ thuộc vào chúng vì chúng có thể thay đổi trong các phiên bản Python tương lai.
