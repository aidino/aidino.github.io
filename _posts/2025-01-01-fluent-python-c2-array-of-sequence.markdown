---
layout: post
title: "[Fluent python] Chapter 2. An array of sequences"
date: 2025-01-06 09:00:00 +0700
categories: fluent python
---

Trước khi tạo ra Python, Guido là một người đóng góp cho ngôn ngữ ABC—một dự án nghiên cứu kéo dài 10 năm nhằm thiết kế một môi trường lập trình cho người mới bắt đầu. ABC đã giới thiệu nhiều ý tưởng mà bây giờ chúng ta coi là "Pythonic": các thao tác chung trên các loại chuỗi khác nhau, các kiểu tuple và mapping tích hợp sẵn, cấu trúc bằng cách thụt lề, kiểu gõ mạnh mà không cần khai báo biến, và nhiều hơn nữa. Không phải ngẫu nhiên mà Python lại thân thiện với người dùng đến vậy.

Python được kế thừa từ ABC cách xử lý thống nhất các chuỗi. Chuỗi ký tự, danh sách, chuỗi byte, mảng, phần tử XML và kết quả cơ sở dữ liệu chia sẻ một tập hợp phong phú các thao tác chung, bao gồm lặp, cắt lát, sắp xếp và nối.

Hiểu được sự đa dạng của các chuỗi có sẵn trong Python giúp chúng ta không phải "tái tạo lại bánh xe", và giao diện chung của chúng truyền cảm hứng cho chúng ta tạo ra các API hỗ trợ và tận dụng đúng cách các kiểu chuỗi hiện có và trong tương lai.

Hầu hết các cuộc thảo luận trong chương này áp dụng cho các chuỗi nói chung, từ danh sách quen thuộc đến các kiểu `str` và `bytes` được thêm vào trong Python 3. Các chủ đề cụ thể về danh sách, tuple, mảng và hàng đợi cũng được đề cập ở đây, nhưng các chi tiết cụ thể của chuỗi Unicode và chuỗi byte xuất hiện trong Chương 4. Ngoài ra, ý tưởng ở đây là đề cập đến các kiểu chuỗi đã sẵn sàng để sử dụng. Việc tạo các kiểu chuỗi của riêng bạn là chủ đề của Chương 12.

[Example notebook](https://aidino.github.io/example_codes/fluent-python-c2-array-of-sequence.ipynb)

### Overview of Built-In Sequences

Thư viện chuẩn của Python cung cấp một tập hợp đa dạng các kiểu dữ liệu dạng chuỗi (sequence types) được triển khai bằng ngôn ngữ C:

**1. Chuỗi chứa (Container sequences):**

* Có thể chứa các phần tử thuộc nhiều kiểu dữ liệu khác nhau, bao gồm cả các chuỗi lồng nhau.
* Ví dụ: `list`, `tuple`, và `collections.deque`.

**2. Chuỗi phẳng (Flat sequences):**

* Chỉ chứa các phần tử thuộc cùng một kiểu dữ liệu đơn giản.
* Ví dụ: `str`, `bytes`, và `array.array`.

Một chuỗi chứa lưu trữ các tham chiếu đến các đối tượng mà nó chứa, các đối tượng này có thể thuộc bất kỳ kiểu dữ liệu nào. Trong khi đó, một chuỗi phẳng lưu trữ giá trị của nội dung trực tiếp trong không gian bộ nhớ của chính nó, không phải dưới dạng các đối tượng Python riêng biệt.

Do đó, chuỗi phẳng thường nhỏ gọn hơn, nhưng chúng bị giới hạn trong việc lưu trữ các giá trị nguyên thủy của máy tính như byte, số nguyên và số thực.

> Mỗi đối tượng Python trong bộ nhớ đều có một phần header chứa siêu dữ liệu. Đối tượng Python đơn giản nhất, một số thực, có một trường giá trị và hai trường siêu dữ liệu:
> * `ob_refcnt`: số lượng tham chiếu đến đối tượng.
> * `ob_type`: con trỏ trỏ đến kiểu dữ liệu của đối tượng.
> * `ob_fval`: một kiểu dữ liệu `double` của C lưu trữ giá trị của số thực.
> Trên một bản dựng Python 64-bit, mỗi trường này chiếm 8 byte. Đó là lý do tại sao một mảng các số thực nhỏ gọn hơn nhiều so với một tuple các số thực: mảng là một đối tượng duy nhất lưu trữ các giá trị thô của các số thực, trong khi tuple bao gồm nhiều đối tượng - bản thân tuple và mỗi đối tượng số thực chứa trong đó.

Một cách khác để phân loại các kiểu dữ liệu dạng chuỗi là dựa trên tính khả biến (mutability):

**1. Chuỗi khả biến (Mutable sequences):**

* Có thể thay đổi nội dung sau khi được tạo.
* Ví dụ: `list`, `bytearray`, `array.array`, và `collections.deque`.

**2. Chuỗi bất biến (Immutable sequences):**

* Không thể thay đổi nội dung sau khi được tạo.
* Ví dụ: `tuple`, `str`, và `bytes`.

Hình 2-2 giúp hình dung cách các chuỗi khả biến kế thừa tất cả các phương thức từ các chuỗi bất biến và triển khai thêm một số phương thức bổ sung. Các kiểu chuỗi cụ thể tích hợp sẵn không thực sự kế thừa từ các lớp cơ sở trừu tượng (ABC) `Sequence` và `MutableSequence`, nhưng chúng là các lớp con ảo được đăng ký với các ABC đó - như chúng ta sẽ thấy trong Chương 13. Là các lớp con ảo, `tuple` và `list` vượt qua các kiểm tra này:

```python
>>> from collections import abc
>>> issubclass(tuple, abc.Sequence)
True
>>> issubclass(list, abc.MutableSequence)
True
```

![]({{site.url}}/images/some-classes-from-collection-abc.png)

Hãy ghi nhớ những đặc điểm chung này: khả biến so với bất biến; chứa so với phẳng. Chúng hữu ích để suy rộng những gì bạn biết về một kiểu chuỗi sang các kiểu khác.

Kiểu chuỗi cơ bản nhất là `list`: một chuỗi chứa khả biến. Tôi hy vọng bạn đã rất quen thuộc với `list`, vì vậy chúng ta sẽ đi thẳng vào list comprehension, một cách mạnh mẽ để xây dựng danh sách mà đôi khi không được sử dụng đầy đủ vì cú pháp có thể trông lạ lùng lúc đầu. Nắm vững list comprehension sẽ mở ra cánh cửa cho generator expression, thứ mà - trong số các mục đích sử dụng khác - có thể tạo ra các phần tử để lấp đầy các chuỗi thuộc bất kỳ loại nào. Cả hai là chủ đề của phần tiếp theo.

### List Comprehensions and Generator Expressions

Một cách nhanh chóng để xây dựng một chuỗi là sử dụng list comprehension (nếu mục tiêu là một `list`) hoặc generator expression (cho các loại chuỗi khác). Nếu bạn không sử dụng các dạng cú pháp này hàng ngày, tôi cá là bạn đang bỏ lỡ cơ hội để viết mã dễ đọc hơn và thường nhanh hơn cùng một lúc.

Nếu bạn nghi ngờ tuyên bố của tôi rằng các cấu trúc này "dễ đọc hơn", hãy đọc tiếp. Tôi sẽ cố gắng thuyết phục bạn.

* **List comprehension**: Một cách viết ngắn gọn để tạo danh sách mới từ một danh sách hiện có, bằng cách áp dụng một biểu thức cho từng phần tử và lọc các phần tử theo điều kiện.
* **Generator expression**: Tương tự như list comprehension nhưng tạo ra một generator, một đối tượng lười biếng chỉ tạo ra các phần tử khi được yêu cầu. 

#### List Comprehensions and Readability

*Example 2-1. Build a list of Unicode code points from a string*

```python
>>> symbols = '$¢£¥€¤'
>>> codes = []
>>> for symbol in symbols:
...
codes.append(ord(symbol))
...
>>> codes
[36, 162, 163, 165, 8364, 164]
```

*Example 2-2. Build a list of Unicode code points from a string, using a listcomp*

```python
>>> symbols = '$¢£¥€¤'
>>> codes = [ord(symbol) for symbol in symbols]
>>> codes
[36, 162, 163, 165, 8364, 164]
```

Bất kỳ ai biết chút ít về Python đều có thể đọc Ví dụ 2-1. Tuy nhiên, sau khi học về listcomps (danh sách rút gọn), tôi thấy Ví dụ 2-2 dễ đọc hơn vì ý định của nó rõ ràng hơn.

Vòng lặp for có thể được sử dụng để làm rất nhiều việc khác nhau: quét một chuỗi để đếm hoặc chọn các mục, tính toán các giá trị tổng hợp (tổng, trung bình) hoặc bất kỳ nhiệm vụ nào khác. Mã trong Ví dụ 2-1 đang xây dựng một danh sách. Ngược lại, listcomp rõ ràng hơn. Mục tiêu của nó luôn là xây dựng một danh sách mới.

Tất nhiên, có thể lạm dụng listcomp để viết mã thực sự khó hiểu. Tôi đã thấy mã Python với listcomp được sử dụng chỉ để lặp lại một khối mã cho các tác dụng phụ của nó. Nếu bạn không làm gì với danh sách được tạo ra, bạn không nên sử dụng cú pháp đó. Ngoài ra, hãy cố gắng giữ cho nó ngắn gọn. Nếu listcomp kéo dài hơn hai dòng, tốt nhất là nên tách nó ra hoặc viết lại nó dưới dạng vòng lặp for thông thường. Hãy sử dụng khả năng phán đoán tốt nhất của bạn: đối với Python, cũng như đối với tiếng Anh, không có quy tắc cứng nhắc nào cho việc viết rõ ràng.

> Trong mã Python, các ngắt dòng bị bỏ qua bên trong các cặp [], {}, hoặc (). Vì vậy, bạn có thể xây dựng danh sách nhiều dòng, listcomp, tuple, từ điển, v.v., mà không cần sử dụng ký tự thoát tiếp tục dòng \, ký tự này sẽ không hoạt động nếu bạn vô tình nhập dấu cách sau nó. Ngoài ra, khi các cặp dấu phân cách đó được sử dụng để xác định một giá trị với một loạt các mục được phân tách bằng dấu phẩy, dấu phẩy ở cuối sẽ bị bỏ qua. Vì vậy, ví dụ, khi viết một giá trị danh sách nhiều dòng, nên đặt dấu phẩy sau mục cuối cùng, giúp cho người viết mã tiếp theo dễ dàng thêm một mục khác vào danh sách đó hơn một chút và giảm nhiễu khi đọc diffs.

**Phạm vi cục bộ trong các biểu thức rút gọn và biểu thức tạo**

Trong Python 3, listcomp, biểu thức tạo và các anh chị em của chúng là setcomp và dictcomp, có một phạm vi cục bộ để chứa các biến được gán trong mệnh đề for.

Tuy nhiên, các biến được gán bằng "toán tử Walrus" := vẫn có thể truy cập được sau khi các biểu thức rút gọn hoặc biểu thức đó trả về — không giống như các biến cục bộ trong một hàm. PEP 572 — Biểu thức gán xác định phạm vi của mục tiêu của := là hàm bao quanh, trừ khi có khai báo global hoặc nonlocal cho mục tiêu đó.

```python
>>> x = 'ABC'
>>> codes = [ord(x) for x in x]
>>> x
'ABC'
>>> codes
[65, 66, 67]
>>> codes = [last := ord(c) for c in x]
>>> last
67
>>> c
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
NameError: name 'c' is not defined
```

Listcomp xây dựng danh sách từ các chuỗi hoặc bất kỳ loại có thể lặp lại nào khác bằng cách lọc và chuyển đổi các mục. Các hàm dựng sẵn filter và map có thể được kết hợp để làm điều tương tự, nhưng khả năng đọc bị ảnh hưởng, như chúng ta sẽ thấy tiếp theo.

#### Listcomps Versus map and filter

Listcomps (list comprehensions) trong Python có thể thực hiện tất cả những gì mà hàm `map` và `filter` làm được, mà không cần phải sử dụng `lambda` - vốn bị hạn chế về mặt chức năng trong Python. Ví dụ như trong Example 2-3:

**Example 2-3:** Cùng một list được tạo bởi listcomp và kết hợp map/filter

```python
>>> symbols = '$¢£¥€¤'
>>> beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
>>> beyond_ascii
[162, 163, 165, 8364, 164]
>>> beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
>>> beyond_ascii
[162, 163, 165, 8364, 164]
```

Trước đây tôi từng nghĩ rằng `map` và `filter` nhanh hơn so với listcomps tương đương, nhưng Alex Martelli đã chỉ ra rằng điều đó không đúng - ít nhất là không phải trong các ví dụ trước. Script `02-array-seq/listcomp_speed.py` trong Fluent Python code repository là một bài kiểm tra tốc độ đơn giản so sánh listcomp với `filter`/`map`.

Tôi sẽ nói thêm về `map` và `filter` trong Chapter 7. Bây giờ chúng ta chuyển sang việc sử dụng listcomps để tính toán tích Descartes (Cartesian products): một list chứa các tuple được xây dựng từ tất cả các item từ hai hoặc nhiều list.

#### Tích Descartes (Cartesian Products)

Listcomps (list comprehensions) có thể xây dựng các list từ tích Descartes của hai hoặc nhiều iterables. Các item tạo nên tích Descartes là các tuple được tạo từ các item của mỗi iterable đầu vào. List kết quả có độ dài bằng tích của độ dài các iterable đầu vào.

Ví dụ, giả sử bạn cần tạo ra một list các áo phông có sẵn trong hai màu và ba kích cỡ. Example 2-4 cho thấy cách tạo ra list đó bằng cách sử dụng listcomp. Kết quả có sáu item.

**Example 2-4:** Tích Descartes (Cartesian product) sử dụng list comprehension

```python
>>> colors = ['black', 'white']
>>> sizes = ['S', 'M', 'L']
>>> tshirts = [(color, size) for color in colors for size in sizes]
>>> tshirts
[('black', 'S'), ('black', 'M'), ('black', 'L'), ('white', 'S'),
('white', 'M'), ('white', 'L')]

>>> for color in colors:
...     for size in sizes:
...         print((color, size))
...
('black', 'S')
('black', 'M')
('black', 'L')
('white', 'S')
('white', 'M')
('white', 'L')

>>> tshirts = [(color, size) for size in sizes 
...             for color in colors]
>>> tshirts
[('black', 'S'), ('white', 'S'), ('black', 'M'), ('white', 'M'),
('black', 'L'), ('white', 'L')]
```

Listcomps chỉ có một chức năng duy nhất: chúng xây dựng các list. Để tạo dữ liệu cho các kiểu sequence khác, genexp (generator expression) là cách nên làm. Phần tiếp theo là một cái nhìn ngắn gọn về genexps trong bối cảnh xây dựng các sequence không phải là list.

#### Generator Expressions

Để khởi tạo các tuple, array và các kiểu sequence khác, bạn cũng có thể bắt đầu từ một listcomp, nhưng genexp (generator expression) tiết kiệm bộ nhớ hơn vì nó sinh ra các item một cách lần lượt bằng cách sử dụng iterator protocol thay vì xây dựng toàn bộ list chỉ để đưa vào một constructor khác.

Genexps sử dụng cú pháp tương tự như listcomps, nhưng được đặt trong dấu ngoặc đơn thay vì dấu ngoặc vuông.

**Example 2-5:** Khởi tạo tuple và array từ generator expression

```python
>>> symbols = '$¢£¥€¤'
>>> tuple(ord(symbol) for symbol in symbols)
(36, 162, 163, 165, 8364, 164)
>>> import array
>>> array.array('I', (ord(symbol) for symbol in symbols))
array('I', [36, 162, 163, 165, 8364, 164])
```

**Example 2-6:** sử dụng genexp với tích Descartes (Cartesian product) để in ra danh sách các áo phông có hai màu và ba kích cỡ. Trái ngược với Example 2-4, ở đây list sáu item của áo phông không bao giờ được xây dựng trong bộ nhớ: generator expression cung cấp cho vòng lặp `for`, tạo ra từng item một. Nếu hai list được sử dụng trong tích Descartes có một nghìn item mỗi list, thì việc sử dụng generator expression sẽ tiết kiệm chi phí xây dựng một list với một triệu item chỉ để cung cấp cho vòng lặp `for`.

**Example 2-6:** Tích Descartes (Cartesian product) trong generator expression

```python
>>> colors = ['black', 'white']
>>> sizes = ['S', 'M', 'L']
>>> for tshirt in (f'{c} {s}' for c in colors for s in sizes):
...     print(tshirt)
...
black S
black M
black L
white S
white M
white L
```

### Tuples Are Not Just Immutable Lists

Một số tài liệu hướng dẫn về Python giới thiệu tuples như là "immutable lists" (danh sách không thể thay đổi), nhưng điều đó chưa đánh giá hết được vai trò của chúng. Tuples thực hiện hai nhiệm vụ: chúng có thể được sử dụng như những immutable lists và cũng như những records (bản ghi) không có tên trường. Cách sử dụng này đôi khi bị bỏ qua, vì vậy chúng ta sẽ bắt đầu với nó.

####  Tuples như bản ghi (Records)

Tuples lưu giữ các bản ghi: mỗi phần tử trong tuple chứa dữ liệu cho một trường, và vị trí của phần tử đó mang ý nghĩa của nó.

Nếu bạn coi tuple chỉ như một list bất biến (immutable), số lượng và thứ tự của các phần tử có thể quan trọng hoặc không, tùy thuộc vào ngữ cảnh. Nhưng khi sử dụng tuple như một tập hợp các trường, số lượng phần tử thường cố định và thứ tự của chúng luôn quan trọng.

Ví dụ 2-7 cho thấy các tuple được sử dụng làm bản ghi. Lưu ý rằng trong mỗi biểu thức, việc sắp xếp tuple sẽ phá hủy thông tin vì ý nghĩa của mỗi trường được xác định bởi vị trí của nó trong tuple.

**Ví dụ 2-7. Tuples được sử dụng làm bản ghi**

```python
>>> lax_coordinates = (33.9425, -118.408056)
>>> city, year, pop, chg, area = ('Tokyo', 2003, 32_450, 0.66, 8014)
>>> traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'),
...
('ESP', 'XDA205856')]
>>> for passport in sorted(traveler_ids):
...
    print('%s/%s' % passport)
...
BRA/CE342567
ESP/XDA205856
USA/31195855
>>> for country, _ in traveler_ids:
...
    print(country)
...
USA
BRA
ESP
```

> Nhìn chung, sử dụng `_` làm biến giả chỉ là một quy ước. Nó chỉ là một tên biến lạ nhưng hợp lệ. Tuy nhiên, trong câu lệnh `match/case`, `_` là một ký tự đại diện khớp với bất kỳ giá trị nào nhưng không bị ràng buộc với một giá trị. Xem "Pattern Matching with Sequences" trên trang 38. Và trong bảng điều khiển Python, kết quả của lệnh trước đó được gán cho `_`—trừ khi kết quả là `None`.

Chúng ta thường nghĩ về bản ghi như các cấu trúc dữ liệu với các trường được đặt tên. Chương 5 trình bày hai cách tạo tuple với các trường được đặt tên.

Nhưng thông thường, không cần phải tạo một class chỉ để đặt tên cho các trường, đặc biệt nếu bạn tận dụng unpacking và tránh sử dụng chỉ mục để truy cập các trường. Trong Ví dụ 2-7, chúng ta đã gán `('Tokyo', 2003, 32_450, 0.66, 8014)` cho `city`, `year`, `pop`, `chg`, `area` trong một câu lệnh duy nhất. Sau đó, toán tử `%` đã gán mỗi phần tử trong tuple `passport` vào vị trí tương ứng trong chuỗi định dạng trong đối số `print`. Đó là hai ví dụ về **tuple unpacking**.

> Thuật ngữ **tuple unpacking** được sử dụng rộng rãi bởi các Pythonista, nhưng **iterable unpacking** đang dần phổ biến, như trong tiêu đề của PEP 3132 — Extended Iterable Unpacking.
"Unpacking Sequences and Iterables" trên trang 35 trình bày nhiều hơn về việc unpacking không chỉ tuple mà còn cả sequences và iterables nói chung.

#### Tuples như List bất biến (Immutable Lists)

Trình thông dịch Python và thư viện chuẩn sử dụng rộng rãi tuple như list bất biến, và bạn cũng nên làm như vậy. Điều này mang lại hai lợi ích chính:

**Clarity (Rõ ràng)**

Khi bạn thấy một tuple trong code, bạn biết rằng độ dài của nó sẽ không bao giờ thay đổi.

**Performance (Hiệu suất)**

Một tuple sử dụng ít bộ nhớ hơn một list có cùng độ dài và nó cho phép Python thực hiện một số tối ưu hóa.

Tuy nhiên, lưu ý rằng tính bất biến của tuple chỉ áp dụng cho các tham chiếu (references) chứa trong đó. Các tham chiếu trong một tuple không thể bị xóa hoặc thay thế. Nhưng nếu một trong những tham chiếu đó trỏ đến một đối tượng có thể thay đổi (mutable object), và đối tượng đó bị thay đổi, thì giá trị của tuple cũng thay đổi. Đoạn mã sau minh họa điểm này bằng cách tạo hai tuple—`a` và `b`—ban đầu bằng nhau. Hình 2-4 biểu diễn bố cục ban đầu của tuple `b` trong bộ nhớ.

![]({{site.url}}/images/tuple-as-immutable-list.png)

Khi phần tử cuối cùng trong `b` bị thay đổi, `b` và `a` trở nên khác nhau:

```python
>>> a = (10, 'alpha', [1, 2])
>>> b = (10, 'alpha', [1, 2])
>>> a == b
True
>>> b[-1].append(99)
>>> a == b
False
>>> b
(10, 'alpha', [1, 2, 99])
```

Tuple với các phần tử có thể thay đổi có thể là nguồn gốc của lỗi. Như chúng ta sẽ thấy trong "What Is Hashable" trên trang 84, một đối tượng chỉ có thể băm (hashable) nếu giá trị của nó không bao giờ thay đổi. Một tuple không thể băm không thể được chèn làm khóa `dict` hoặc phần tử `set`.

Nếu bạn muốn xác định rõ ràng liệu một tuple (hoặc bất kỳ đối tượng nào) có giá trị cố định hay không, bạn có thể sử dụng hàm `hash` tích hợp sẵn để tạo một hàm `fixed` như sau:

```python
>>> def fixed(o):
...     try:
...         hash(o)
...     except TypeError:
...         return False
...     return True
...
>>> tf = (10, 'alpha', (1, 2))
>>> tm = (10, 'alpha', [1, 2])
>>> fixed(tf)
True

>>> fixed(tm)
False
```

Chúng ta sẽ khám phá vấn đề này sâu hơn trong "The Relative Immutability of Tuples" trên trang 207.

Mặc dù có lưu ý này, tuple vẫn được sử dụng rộng rãi như list bất biến. Chúng cung cấp một số lợi thế về hiệu suất được giải thích bởi nhà phát triển lõi Python Raymond Hettinger trong một câu trả lời trên StackOverflow cho câu hỏi: "Are tuples more efficient than lists in Python?". Tóm lại, Hettinger đã viết:

* Để đánh giá một tuple literal, trình biên dịch Python tạo ra bytecode cho một hằng số tuple trong một thao tác; nhưng đối với một list literal, bytecode được tạo ra sẽ đẩy từng phần tử như một hằng số riêng biệt vào ngăn xếp dữ liệu (data stack) và sau đó xây dựng list.
* Với một tuple `t`, `tuple(t)` chỉ đơn giản là trả về một tham chiếu đến cùng một `t`. Không cần phải sao chép. Ngược lại, với một list `l`, hàm tạo `list(l)` phải tạo một bản sao mới của `l`.
* Do độ dài cố định, một instance tuple được cấp phát chính xác không gian bộ nhớ mà nó cần. Mặt khác, các instance của list được cấp phát với dung lượng dự phòng để khấu hao chi phí cho các lần thêm phần tử (append) trong tương lai.
* Các tham chiếu đến các phần tử trong một tuple được lưu trữ trong một mảng trong cấu trúc tuple, trong khi một list chứa một con trỏ đến một mảng các tham chiếu được lưu trữ ở nơi khác. Việc gián tiếp là cần thiết vì khi một list phát triển vượt quá không gian hiện được cấp phát, Python cần phải cấp phát lại mảng các tham chiếu để tạo thêm dung lượng. Việc gián tiếp thêm này làm cho bộ nhớ đệm CPU kém hiệu quả hơn.

#### So sánh các phương thức của Tuple và List

Khi sử dụng tuple như một biến thể bất biến của list, điều quan trọng là phải biết API của chúng giống nhau như thế nào. Như bạn có thể thấy trong Bảng 2-1, tuple hỗ trợ tất cả các phương thức list mà không liên quan đến việc thêm hoặc xóa phần tử, ngoại trừ một trường hợp—tuple thiếu phương thức `__reversed__`. Tuy nhiên, đó chỉ là để tối ưu hóa; `reversed(my_tuple)` vẫn hoạt động mà không cần nó.

![]({{site.url}}/images/compare-tuple-and-list-1.png)
![]({{site.url}}/images/compare-tuple-and-list-2.png)

### Unpacking Sequences and Iterables

updating...