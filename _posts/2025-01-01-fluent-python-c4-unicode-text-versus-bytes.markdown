---
layout: post
title: "[Fluent python] Chapter 4. Unicode Text versus bytes"
date: 2025-01-10 09:00:00 +0700
categories: fluent python
---

Python 3 đã giới thiệu một sự phân biệt rõ ràng giữa chuỗi văn bản của con người (`Unicode text`) và chuỗi các byte thô (`raw bytes`). Việc chuyển đổi ngầm định (`implicit conversion`) các chuỗi byte thành văn bản Unicode đã là quá khứ. Chương này đề cập đến các chuỗi Unicode, chuỗi nhị phân (`binary sequences`) và các mã hóa (`encodings`) được sử dụng để chuyển đổi giữa chúng.

Tùy thuộc vào loại công việc bạn làm với Python, bạn có thể nghĩ rằng việc hiểu Unicode là không quan trọng. Điều đó khó xảy ra, nhưng dù sao thì cũng không thể thoát khỏi sự phân chia `str` so với `byte`. Thêm vào đó, bạn sẽ thấy rằng các kiểu chuỗi nhị phân chuyên biệt cung cấp các tính năng mà kiểu `str` "đa năng" của Python 2 không có.

### Table of content
1. [Character Issues](#CharacterIssues)
2. [Byte Essentials](#ByteEssentials)
3. [Basic Encoders/Decoders](#BasicEncodersDecoders)
4. [Understanding Encode/Decode Problems](#UnderstandingEncodeDecodeProblems)
    * 4.1. [Coping with UnicodeEncodeError](#CopingwithUnicodeEncodeError)
    * 4.2. [Coping with UnicodeDecodeError](#CopingwithUnicodeDecodeError)
    * 4.3. [SyntaxError When Loading Modules with Unexpected Encoding](#SyntaxErrorWhenLoadingModuleswithUnexpectedEncoding)
    * 4.4. [How to Discover the Encoding of a Byte Sequence](#HowtoDiscovertheEncodingofaByteSequence)
    * 4.5. [BOM: A Useful Gremlin](#BOM:AUsefulGremlin)
5. [Handling Text Files](#HandlingTextFiles)
    * 5.1. [Beware of Encoding Defaults](#BewareofEncodingDefaults)
6. [Normalizing Unicode for Reliable Comparisons](#NormalizingUnicodeforReliableComparisons)
    * 6.1. [Case Folding](#CaseFolding)
    * 6.2. [Utility Functions for Normalized Text Matching](#UtilityFunctionsforNormalizedTextMatching)
    * 6.3. [Extreme “Normalization”: Taking Out Diacritics - Chuẩn hóa "cực đoan": Loại bỏ dấu phụ](#ExtremeNormalization:TakingOutDiacritics-Chunhaccoan:Loibduph)
7. [Sorting Unicode Text](#SortingUnicodeText)
    * 7.1. [Sorting with the Unicode Collation Algorithm](#SortingwiththeUnicodeCollationAlgorithm)
8. [The Unicode Database](#TheUnicodeDatabase)
    * 8.1. [Finding Characters by Name](#FindingCharactersbyName)
9. [Tìm kiếm ký tự theo tên](#Tmkimkttheotn)
    * 9.1. [Numeric Meaning of Characters](#NumericMeaningofCharacters)
10. [Dual-Mode str and bytes APIs](#Dual-ModestrandbytesAPIs)
    * 10.1. [str Versus bytes in Regular Expressions](#strVersusbytesinRegularExpressions)
    * 10.2. [str Versus bytes in os Functions](#strVersusbytesinosFunctions)


###  1. <a name='CharacterIssues'></a>Character Issues

Khái niệm "chuỗi" (`string`) khá đơn giản: một chuỗi là một dãy các ký tự (`characters`). Vấn đề nằm ở định nghĩa của "ký tự".

Năm 2021, định nghĩa tốt nhất về "ký tự" mà chúng ta có là một ký tự Unicode. Theo đó, các mục chúng ta nhận được từ một `str` trong Python 3 là các ký tự Unicode, giống như các mục của một đối tượng `unicode` trong Python 2 — chứ không phải là các byte thô mà chúng ta nhận được từ một `str` trong Python 2.

Tiêu chuẩn Unicode tách biệt rõ ràng nhận dạng của các ký tự với các biểu diễn byte cụ thể:

*   Nhận dạng của một ký tự — điểm mã (`code point`) của nó — là một số từ 0 đến 1.114.111 (cơ số 10), được hiển thị trong tiêu chuẩn Unicode dưới dạng 4 đến 6 chữ số thập lục phân với tiền tố "U+", từ U+0000 đến U+10FFFF. Ví dụ: điểm mã cho chữ cái A là U+0041, ký hiệu Euro là U+20AC và ký hiệu âm nhạc G clef được gán cho điểm mã U+1D11E. Khoảng 13% điểm mã hợp lệ có các ký tự được gán cho chúng trong Unicode 13.0.0, tiêu chuẩn được sử dụng trong Python 3.10.0b4.
*   Các byte thực tế đại diện cho một ký tự phụ thuộc vào mã hóa (`encoding`) được sử dụng. Mã hóa là một thuật toán chuyển đổi các điểm mã thành chuỗi byte và ngược lại. Điểm mã cho chữ cái A (U+0041) được mã hóa thành một byte \x41 trong mã hóa UTF-8, hoặc là các byte \x41\x00 trong mã hóa UTF-16LE. Một ví dụ khác, UTF-8 yêu cầu ba byte — \xe2\x82\xac — để mã hóa ký hiệu Euro (U+20AC), nhưng trong UTF-16LE, cùng một điểm mã được mã hóa thành hai byte: \xac\x20.

Chuyển đổi từ điểm mã sang byte là mã hóa (`encoding`); chuyển đổi từ byte sang điểm mã là giải mã (`decoding`). Xem Ví dụ 4-1.

Ví dụ 4-1. Mã hóa và giải mã

```python
>>> s = 'café'
>>> len(s)
4
>>> b = s.encode('utf8')
>>> b
b'caf\xc3\xa9'
>>> len(b)
5
>>> b.decode('utf8')
'café'
```

`str` 'café' có bốn ký tự Unicode.

Mã hóa `str` thành `bytes` bằng cách sử dụng mã hóa UTF-8.

`bytes` literal có tiền tố b.

`bytes` b có năm byte (điểm mã cho "é" được mã hóa thành hai byte trong UTF-8).

Giải mã `bytes` thành `str` bằng cách sử dụng mã hóa UTF-8.

Mặc dù `str` trong Python 3 gần giống với kiểu `unicode` trong Python 2 với một tên mới, nhưng `bytes` trong Python 3 không chỉ đơn giản là `str` cũ được đổi tên và cũng có kiểu `bytearray` liên quan chặt chẽ. Vì vậy, điều đáng giá là xem xét các kiểu chuỗi nhị phân trước khi chuyển sang các vấn đề mã hóa/giải mã.

###  2. <a name='ByteEssentials'></a>Byte Essentials

Trong Python, khi làm việc với dữ liệu thô như hình ảnh, file âm thanh, hoặc dữ liệu mạng, bạn sẽ gặp kiểu dữ liệu **bytes**. Hãy tưởng tượng bytes như một chuỗi các hạt nhỏ, mỗi hạt mang một giá trị từ 0 đến 255.  

**Có 2 loại bytes:**

* **`bytes`**: Giống như một chuỗi hạt cố định, không thể thay đổi các hạt bên trong.
* **`bytearray`**: Giống như một chuỗi hạt có thể tháo lắp, bạn có thể thay đổi các hạt trong chuỗi này.

**Cách tạo ra bytes:**

* Chuyển từ chuỗi văn bản (`str`) sang `bytes` bằng cách chỉ định cách mã hóa (ví dụ: UTF-8).
* Liệt kê các giá trị từ 0 đến 255.
* Sao chép từ một vùng dữ liệu khác trong bộ nhớ.

**Đặc điểm của bytes:**

* Mỗi "hạt" trong `bytes` là một số nguyên, không phải ký tự.
* Có thể cắt `bytes` thành những `bytes` nhỏ hơn.
* `bytes` có nhiều phương thức giống với chuỗi văn bản (`str`) như `endswith`, `replace`, `strip`, ... giúp bạn dễ dàng xử lý dữ liệu.

**Lưu ý:**

* Khi hiển thị `bytes`, Python sẽ cố gắng hiển thị các ký tự ASCII tương ứng nếu có thể.
* `bytes` có phương thức `fromhex` để tạo `bytes` từ chuỗi các chữ số thập lục phân.


**Ví dụ:**

```python
# Tạo bytes từ chuỗi văn bản
cafe = bytes('café', encoding='utf_8') 
print(cafe)  # Output: b'caf\xc3\xa9'

# Lấy giá trị của byte đầu tiên
print(cafe[0])  # Output: 99

# Cắt bytes
print(cafe[:1])  # Output: b'c' 
```

###  3. <a name='BasicEncodersDecoders'></a>Basic Encoders/Decoders

Python cung cấp sẵn hơn 100 codec (bộ mã hóa/giải mã) để chuyển đổi qua lại giữa văn bản và byte. Mỗi codec có một tên, ví dụ như `'utf_8'`, và thường có các tên gọi khác như `'utf8'`, `'utf-8'` và `'U8'`, bạn có thể sử dụng làm đối số `encoding` trong các hàm như `open()`, `str.encode()`, `bytes.decode()`, v.v.

Ví dụ 4-4 cho thấy cùng một văn bản được mã hóa thành ba chuỗi byte khác nhau.

**Ví dụ 4-4.** Chuỗi "El Niño" được mã hóa bằng ba codec tạo ra các chuỗi byte rất khác nhau

```python
>>> for codec in ['latin_1', 'utf_8', 'utf_16']:
...     print(codec, 'El Niño'.encode(codec), sep='\t')
...
latin_1	b'El Ni\xf1o'
utf_8	b'El Ni\xc3\xb1o'
utf_16	b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'
```

Một số encoding, như ASCII và thậm chí cả GB2312 đa byte, không thể biểu diễn mọi ký tự Unicode. Tuy nhiên, các encoding UTF được thiết kế để xử lý mọi code point Unicode.

Các encoding được hiển thị trong Hình 4-1 được chọn làm mẫu đại diện:

* **latin1** (còn gọi là **iso8859_1**): Quan trọng vì nó là cơ sở cho các encoding khác, chẳng hạn như cp1252 và chính Unicode (lưu ý cách các giá trị byte latin1 xuất hiện trong các byte cp1252 và thậm chí trong các code point).
* **cp1252**: Một superset hữu ích của latin1 được tạo bởi Microsoft, thêm các ký hiệu hữu ích như dấu ngoặc kép cong và € (euro); một số ứng dụng Windows gọi nó là "ANSI", nhưng nó chưa bao giờ là một tiêu chuẩn ANSI thực sự.
* **cp437**: Bộ ký tự gốc của IBM PC, với các ký tự vẽ hộp. Không tương thích với latin1, xuất hiện sau này.
* **gb2312**: Tiêu chuẩn cũ để mã hóa các chữ tượng hình tiếng Trung giản thể được sử dụng ở Trung Quốc đại lục; một trong số nhiều encoding đa byte được triển khai rộng rãi cho các ngôn ngữ châu Á.
* **utf-8**: Encoding 8-bit phổ biến nhất trên web, tính đến tháng 7 năm 2021, "W3Techs: Usage statistics of character encodings for websites" tuyên bố rằng 97% các trang web sử dụng UTF-8, tăng từ 81,4% khi tôi viết đoạn này trong lần xuất bản đầu tiên của cuốn sách này vào tháng 9 năm 2014.
* **utf-16le**: Một dạng của lược đồ encoding UTF 16-bit; tất cả các encoding UTF-16 đều hỗ trợ các code point vượt quá U+FFFF thông qua các escape sequence được gọi là "surrogate pairs". UTF-16 đã thay thế encoding Unicode 1.0 16-bit ban đầu — UCS-2 — từ năm 1996. UCS-2 vẫn được sử dụng trong nhiều hệ thống mặc dù đã bị phản đối từ thế kỷ trước vì nó chỉ hỗ trợ các code point lên đến U+FFFF. Tính đến năm 2021, hơn 57% code point được phân bổ là trên U+FFFF, bao gồm cả các emoji quan trọng.

Với tổng quan về các encoding phổ biến này, chúng ta chuyển sang xử lý các vấn đề trong các hoạt động mã hóa và giải mã.

###  4. <a name='UnderstandingEncodeDecodeProblems'></a>Understanding Encode/Decode Problems

Mặc dù có một exception chung là `UnicodeError`, nhưng lỗi được Python báo cáo thường cụ thể hơn: `UnicodeEncodeError` (khi chuyển đổi `str` sang chuỗi nhị phân) hoặc `UnicodeDecodeError` (khi đọc chuỗi nhị phân thành `str`).

Việc tải các module Python cũng có thể gây ra `SyntaxError` khi encoding nguồn không chính xác.

####  4.1. <a name='CopingwithUnicodeEncodeError'></a>Coping with UnicodeEncodeError

Hầu hết các codec không phải UTF chỉ xử lý một tập hợp con nhỏ các ký tự Unicode. Khi chuyển đổi văn bản thành byte, nếu một ký tự không được định nghĩa trong encoding đích, `UnicodeEncodeError` sẽ được đưa ra, trừ khi xử lý đặc biệt được cung cấp bằng cách truyền đối số `errors` cho phương thức hoặc hàm encoding. Cách hoạt động của các trình xử lý lỗi được hiển thị trong Ví dụ 4-5.

**Ví dụ 4-5.** Mã hóa thành byte: thành công và xử lý lỗi

```python
>>> city = 'São Paulo'
>>> city.encode('utf_8')
b'S\xc3\xa3o Paulo'
>>> city.encode('utf_16')
b'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'
>>> city.encode('iso8859_1')
b'S\xe3o Paulo'
>>> city.encode('cp437')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "/.../lib/python3.4/encodings/cp437.py", line 12, in encode
return codecs.charmap_encode(input,errors,encoding_map)
UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in
position 1: character maps to <undefined>
>>> city.encode('cp437', errors='ignore')
b'So Paulo'
>>> city.encode('cp437', errors='replace')
b'S?o Paulo'
>>> city.encode('cp437', errors='xmlcharrefreplace')
b'S&#227;o Paulo'
```

- Các encoding UTF xử lý bất kỳ `str` nào.
- `iso8859_1` cũng hoạt động cho chuỗi 'São Paulo'.
- `cp437` không thể mã hóa 'ã' (“a” có dấu ngã). Trình xử lý lỗi mặc định — `'strict'` — đưa ra `UnicodeEncodeError`.
- Trình xử lý `error='ignore'` bỏ qua các ký tự không thể mã hóa; đây thường là một ý tưởng rất tồi, dẫn đến mất dữ liệu âm thầm.
- Khi mã hóa, `error='replace'` thay thế các ký tự không thể mã hóa bằng '?'; dữ liệu cũng bị mất, nhưng người dùng sẽ nhận được manh mối rằng có điều gì đó không ổn.
- `'xmlcharrefreplace'` thay thế các ký tự không thể mã hóa bằng một thực thể XML. Nếu bạn không thể sử dụng UTF và bạn không thể để mất dữ liệu, đây là lựa chọn duy nhất.

ASCII là một tập hợp con chung cho tất cả các encoding mà tôi biết, do đó, việc mã hóa sẽ luôn hoạt động nếu văn bản được tạo riêng từ các ký tự ASCII. Python 3.7 đã thêm một phương thức boolean mới `str.isascii()` để kiểm tra xem văn bản Unicode của bạn có phải là 100% ASCII thuần túy hay không. Nếu đúng như vậy, bạn sẽ có thể mã hóa nó thành byte trong bất kỳ encoding nào mà không cần đưa ra `UnicodeEncodeError`.


####  4.2. <a name='CopingwithUnicodeDecodeError'></a>Coping with UnicodeDecodeError

Không phải mọi byte đều chứa một ký tự ASCII hợp lệ và không phải mọi chuỗi byte đều là UTF-8 hoặc UTF-16 hợp lệ; do đó, khi bạn giả định một trong những encoding này trong khi chuyển đổi chuỗi nhị phân thành văn bản, bạn sẽ gặp `UnicodeDecodeError` nếu tìm thấy byte không mong muốn.

Mặt khác, nhiều encoding 8-bit cũ như `'cp1252'`, `'iso8859_1'` và `'koi8_r'` có thể giải mã bất kỳ luồng byte nào, bao gồm cả nhiễu ngẫu nhiên, mà không báo cáo lỗi. Do đó, nếu chương trình của bạn giả định sai encoding 8-bit, nó sẽ âm thầm giải mã rác.

Ví dụ 4-6 minh họa cách sử dụng codec sai có thể tạo ra các ký tự lạ hoặc `UnicodeDecodeError`.

**Ví dụ 4-6.** Giải mã từ `str` sang byte: thành công và xử lý lỗi

```python
>>> octets = b'Montr\xe9al'
>>> octets.decode('cp1252')
'Montréal'
>>> octets.decode('iso8859_7')
'Montrιal'
>>> octets.decode('koi8_r')
'MontrИal'
>>> octets.decode('utf_8')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
>>> octets.decode('utf_8', errors='replace')
'Montr�al'
```

- Từ “Montréal” được mã hóa dưới dạng latin1; `'\xe9'` là byte cho “é”.
- Giải mã bằng Windows 1252 hoạt động vì nó là một superset của latin1.
- ISO-8859-7 dành cho tiếng Hy Lạp, vì vậy byte `'\xe9'` bị hiểu sai và không có lỗi nào được đưa ra.
- KOI8-R dành cho tiếng Nga. Bây giờ `'\xe9'` là viết tắt của chữ cái Kirin "И".
- Codec `'utf_8'` phát hiện ra rằng `octets` không phải là UTF-8 hợp lệ và đưa ra `UnicodeDecodeError`.
- Sử dụng xử lý lỗi `'replace'`, `\xe9` được thay thế bằng “�” (code point U+FFFD), KÝ TỰ THAY THẾ Unicode chính thức nhằm đại diện cho các ký tự không xác định.


####  4.3. <a name='SyntaxErrorWhenLoadingModuleswithUnexpectedEncoding'></a>SyntaxError When Loading Modules with Unexpected Encoding

UTF-8 là encoding nguồn mặc định cho Python 3, giống như ASCII là mặc định cho Python 2. Nếu bạn tải một module `.py` chứa dữ liệu không phải UTF-8 và không có khai báo encoding, bạn sẽ nhận được thông báo như sau:

```
SyntaxError: Non-UTF-8 code starting with '\xe1' in file ola.py on line 
1, but no encoding declared; see https://python.org/dev/peps/pep-0263/ 
for details
```

Vì UTF-8 được triển khai rộng rãi trong các hệ thống GNU/Linux và macOS, một kịch bản có thể xảy ra là mở một file `.py` được tạo trên Windows với cp1252. Lưu ý rằng lỗi này xảy ra ngay cả trong Python cho Windows, vì encoding mặc định cho mã nguồn Python 3 là UTF-8 trên tất cả các nền tảng.

Để khắc phục sự cố này, hãy thêm một magic comment mã hóa ở đầu file, như được hiển thị trong Ví dụ 4-7.

**Ví dụ 4-7.** `ola.py`: “Hello, World!” trong tiếng Bồ Đào Nha

```python
# coding: cp1252
print('Olá, Mundo!')
```

> Bây giờ mã nguồn Python 3 không còn bị giới hạn ở ASCII và mặc định là encoding UTF-8 tuyệt vời, "cách khắc phục" tốt nhất cho mã nguồn trong các encoding cũ như `'cp1252'` là chuyển đổi chúng sang UTF-8, và không bận tâm đến các comment mã hóa. Nếu trình soạn thảo của bạn không hỗ trợ UTF-8, đã đến lúc chuyển đổi.

####  4.4. <a name='HowtoDiscovertheEncodingofaByteSequence'></a>How to Discover the Encoding of a Byte Sequence

Làm thế nào để bạn tìm ra encoding của một chuỗi byte? Câu trả lời ngắn gọn: bạn không thể. Bạn phải được cho biết.

Một số giao thức truyền thông và định dạng file, như HTTP và XML, chứa các header cho chúng ta biết rõ ràng nội dung được mã hóa như thế nào. Bạn có thể chắc chắn rằng một số luồng byte không phải là ASCII vì chúng chứa các giá trị byte trên 127 và cách UTF-8 và UTF-16 được xây dựng cũng giới hạn các chuỗi byte có thể có.

Tuy nhiên, xét rằng ngôn ngữ của con người cũng có các quy tắc và hạn chế riêng, một khi bạn giả định rằng một luồng byte là văn bản thuần túy của con người, thì có thể đánh hơi encoding của nó bằng cách sử dụng heuristics và thống kê. Ví dụ: nếu các byte `b'\x00'` phổ biến, thì có thể đó là encoding 16- hoặc 32-bit chứ không phải là lược đồ 8-bit, vì các ký tự null trong văn bản thuần túy là lỗi. Khi chuỗi byte `b'\x20\x00'` xuất hiện thường xuyên, thì nhiều khả năng đó là ký tự khoảng trắng (U+0020) trong encoding UTF-16LE, chứ không phải là ký tự U+2000 EN QUAD khó hiểu — dù đó là gì đi nữa.

Đó là cách package “Chardet — The Universal Character Encoding Detector” hoạt động để đoán một trong hơn 30 encoding được hỗ trợ. Chardet là một thư viện Python mà bạn có thể sử dụng trong các chương trình của mình, nhưng cũng bao gồm một tiện ích dòng lệnh, `chardetect`. Đây là những gì nó báo cáo trên file nguồn cho chương này:

```bash
$ chardetect 04-text-byte.asciidoc
04-text-byte.asciidoc: utf-8 with confidence 0.99
```

Mặc dù các chuỗi nhị phân của văn bản được mã hóa thường không mang theo gợi ý rõ ràng về encoding của chúng, nhưng các định dạng UTF có thể thêm một **byte order mark** vào nội dung văn bản. Điều đó được giải thích tiếp theo.


####  4.5. <a name='BOM:AUsefulGremlin'></a>BOM: A Useful Gremlin

Trong Ví dụ 4-4, bạn có thể đã nhận thấy một vài byte phụ ở đầu chuỗi được mã hóa UTF-16. Đây là chúng một lần nữa:

```bash
>>> u16 = 'El Niño'.encode('utf_16')
>>> u16
b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'
```

Các byte này là b'\xff\xfe'. Đó là một **BOM (byte-order mark)** — dấu thứ tự byte — biểu thị thứ tự byte “little-endian” của CPU Intel nơi quá trình mã hóa được thực hiện.

Trên một máy little-endian, đối với mỗi **code point**, byte ít quan trọng nhất đứng trước: chữ cái 'E', **code point** U+0045 (thập phân 69), được mã hóa trong byte bù 2 và 3 là 69 và 0:

```bash
>>> list(u16)
[255, 254, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]
```

Trên CPU big-endian, quá trình mã hóa sẽ bị đảo ngược; 'E' sẽ được mã hóa là 0 và 69.

Để tránh nhầm lẫn, mã hóa UTF-16 thêm vào đầu văn bản cần mã hóa với ký tự đặc biệt vô hình **ZERO WIDTH NO-BREAK SPACE (U+FEFF)**. Trên hệ thống little-endian, nó được mã hóa là b'\xff\xfe' (thập phân 255, 254). Bởi vì, theo thiết kế, không có ký tự U+FFFE trong Unicode, chuỗi byte b'\xff\xfe' phải có nghĩa là **ZERO WIDTH NO-BREAK SPACE** trên mã hóa little-endian, do đó **codec** biết thứ tự byte nào sẽ sử dụng.

Có một biến thể của UTF-16 — UTF-16LE — rõ ràng là little-endian, và một biến thể khác rõ ràng là big-endian, UTF-16BE. Nếu bạn sử dụng chúng, **BOM** sẽ không được tạo:

```bash
>>> u16le = 'El Niño'.encode('utf_16le')
>>> list(u16le)
[69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]
```

```bash
>>> u16be = 'El Niño'.encode('utf_16be')
>>> list(u16be)
[0, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111]
```

Nếu có, **BOM** được cho là sẽ được lọc bởi **codec UTF-16**, để bạn chỉ nhận được nội dung văn bản thực tế của tệp mà không có **ZERO WIDTH NO-BREAK SPACE** đứng đầu. Tiêu chuẩn Unicode nói rằng nếu một tệp là UTF-16 và không có **BOM**, thì nên giả định là UTF-16BE (big-endian). Tuy nhiên, kiến trúc Intel x86 là little-endian, vì vậy có rất nhiều UTF-16 little-endian không có **BOM**.

Toàn bộ vấn đề về **endianness** này chỉ ảnh hưởng đến các mã hóa sử dụng các từ có nhiều hơn một byte, như UTF-16 và UTF-32. Một lợi thế lớn của UTF-8 là nó tạo ra cùng một chuỗi byte bất kể **endianness** của máy, vì vậy không cần **BOM**.

Tuy nhiên, một số ứng dụng Windows (đáng chú ý là Notepad) vẫn thêm **BOM** vào các tệp UTF-8 — và Excel phụ thuộc vào **BOM** để phát hiện tệp UTF-8, nếu không nó sẽ giả định nội dung được mã hóa bằng **Windows code page**. Mã hóa UTF-8 này với **BOM** được gọi là UTF-8-SIG trong sổ đăng ký **codec** của Python. Ký tự U+FEFF được mã hóa trong UTF-8-SIG là chuỗi ba byte b'\xef\xbb\xbf'. Vì vậy, nếu một tệp bắt đầu bằng ba byte đó, thì có khả năng đó là tệp UTF-8 có **BOM**.

###  5. <a name='HandlingTextFiles'></a>Handling Text Files

Cách tốt nhất để xử lý Input/Output văn bản là sử dụng kỹ thuật "Unicode sandwich" (Hình 4-2). Điều này có nghĩa là các byte nên được **decode** thành **str** càng sớm càng tốt khi nhập (ví dụ: khi mở một tệp để đọc). "Nhân" của sandwich là logic nghiệp vụ của chương trình, nơi xử lý văn bản được thực hiện độc quyền trên các đối tượng **str**. Bạn không bao giờ nên **encode** hoặc **decode** ở giữa quá trình xử lý khác. Khi xuất, các **str** được **encode** thành byte càng muộn càng tốt. Hầu hết các web framework đều hoạt động như vậy, và chúng ta hiếm khi chạm vào byte khi sử dụng chúng. Ví dụ, trong Django, các view của bạn nên xuất ra Unicode **str**; Django sẽ tự động **encode** phản hồi thành byte, sử dụng UTF-8 theo mặc định.

Python 3 giúp việc tuân theo lời khuyên của "Unicode sandwich" dễ dàng hơn, bởi vì hàm `open()` tích hợp sẵn sẽ thực hiện **decode** cần thiết khi đọc và **encode** khi ghi tệp ở chế độ văn bản, vì vậy tất cả những gì bạn nhận được từ `my_file.read()` và truyền cho `my_file.write(text)` đều là các đối tượng **str**.

Do đó, việc sử dụng tệp văn bản rõ ràng là đơn giản. Nhưng nếu bạn dựa vào các **encoding** mặc định, bạn sẽ gặp rắc rối.

Hãy xem xét phiên console trong Ví dụ 4-8. Bạn có thể phát hiện ra lỗi không?

**Ví dụ 4-8:** Sự cố **encoding** nền tảng (nếu bạn thử điều này trên máy của mình, bạn có thể gặp sự cố hoặc không)

```python
>>> open('cafe.txt', 'w', encoding='utf_8').write('café')
4
>>> open('cafe.txt').read()
'cafÃ©'
```

Lỗi: Tôi đã chỉ định **encoding** UTF-8 khi ghi tệp nhưng không làm như vậy khi đọc tệp, vì vậy Python đã giả định **encoding** tệp mặc định của Windows — code page 1252 — và các byte cuối cùng trong tệp đã bị **decode** thành các ký tự 'Ã©' thay vì 'é'.

Tôi đã chạy Ví dụ 4-8 trên Python 3.8.1, 64 bit, trên Windows 10 (bản dựng 18363). Các câu lệnh tương tự chạy trên GNU/Linux hoặc macOS gần đây hoạt động hoàn hảo vì **encoding** mặc định của chúng là UTF-8, tạo ấn tượng sai lầm rằng mọi thứ đều ổn. Nếu đối số **encoding** bị bỏ qua khi mở tệp để ghi, **encoding** mặc định cục bộ sẽ được sử dụng và chúng ta sẽ đọc tệp chính xác bằng cách sử dụng cùng một **encoding**. Nhưng sau đó, tập lệnh này sẽ tạo các tệp có nội dung byte khác nhau tùy thuộc vào nền tảng hoặc thậm chí tùy thuộc vào cài đặt cục bộ trong cùng một nền tảng, tạo ra các vấn đề về khả năng tương thích.

Một chi tiết thú vị trong Ví dụ 4-8 là hàm `write` trong câu lệnh đầu tiên báo cáo rằng bốn ký tự đã được ghi, nhưng ở dòng tiếp theo, năm ký tự được đọc. Ví dụ 4-9 là phiên bản mở rộng của Ví dụ 4-8, giải thích điều đó và các chi tiết khác.

**Ví dụ 4-9:** Kiểm tra kỹ hơn Ví dụ 4-8 chạy trên Windows cho thấy lỗi và cách khắc phục

```python
>>> fp = open('cafe.txt', 'w', encoding='utf_8')
>>> fp
<_io.TextIOWrapper name='cafe.txt' mode='w' encoding='utf_8'>
>>> fp.write('café')
4
>>> fp.close()
>>> import os
>>> os.stat('cafe.txt').st_size
5
>>> fp2 = open('cafe.txt')
>>> fp2
<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='cp1252'>
>>> fp2.encoding
'cp1252'
>>> fp2.read()
'cafÃ©'
>>> fp3 = open('cafe.txt', encoding='utf_8')
>>> fp3
<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='utf_8'>
>>> fp3.read()
'café'
>>> fp4 = open('cafe.txt', 'rb')
>>> fp4
<_io.BufferedReader name='cafe.txt'>
>>> fp4.read()
b'caf\xc3\xa9'
```

* Theo mặc định, `open` sử dụng chế độ văn bản và trả về một đối tượng **TextIOWrapper** với **encoding** cụ thể.
* Phương thức `write` trên **TextIOWrapper** trả về số lượng ký tự Unicode đã ghi.
* `os.stat` cho biết tệp có 5 byte; UTF-8 **encode** 'é' thành 2 byte, 0xc3 và 0xa9.
* Mở tệp văn bản mà không có **encoding** rõ ràng sẽ trả về **TextIOWrapper** với **encoding** được đặt thành mặc định từ locale.
* Đối tượng **TextIOWrapper** có thuộc tính **encoding** mà bạn có thể kiểm tra: cp1252 trong trường hợp này.
* Trong **encoding** cp1252 của Windows, byte 0xc3 là "Ã" (A có dấu ngã) và 0xa9 là dấu bản quyền.
* Mở cùng một tệp với **encoding** chính xác.
* Kết quả mong đợi: bốn ký tự Unicode giống nhau cho 'café'.
* Cờ 'rb' mở tệp để đọc ở chế độ nhị phân.
* Đối tượng được trả về là **BufferedReader** chứ không phải **TextIOWrapper**.
* Đọc rằng trả về byte, như mong đợi.

Vấn đề trong Ví dụ 4-9 liên quan đến việc dựa vào cài đặt mặc định khi mở tệp văn bản. Có một số nguồn cho các mặc định như vậy, như phần tiếp theo cho thấy.

####  5.1. <a name='BewareofEncodingDefaults'></a>Beware of Encoding Defaults

**Vấn đề chính:**

* Python sử dụng **encoding** mặc định để đọc và ghi file.
* **Encoding** mặc định này khác nhau trên các hệ điều hành (Windows, macOS, Linux).
* Nếu không cẩn thận, văn bản có thể bị hiển thị sai khi chuyển giữa các hệ thống.

**Giải pháp:**

* Luôn chỉ rõ **encoding** khi làm việc với file văn bản (ví dụ: `encoding='utf-8'`).
* Kỹ thuật "Unicode sandwich": chuyển đổi byte sang Unicode (`str`) ngay khi đọc file và ngược lại khi ghi file.

###  6. <a name='NormalizingUnicodeforReliableComparisons'></a>Normalizing Unicode for Reliable Comparisons

**Vấn đề:**

* Unicode có nhiều cách để biểu diễn cùng một ký tự, ví dụ chữ "é" có thể là một ký tự duy nhất hoặc kết hợp từ "e" và dấu sắc.
* Python phân biệt hai cách này, dẫn đến so sánh chuỗi có thể sai.

**Giải pháp:**

* Sử dụng hàm `unicodedata.normalize()` để chuẩn hóa chuỗi Unicode về một dạng duy nhất.
* Có các dạng chuẩn hóa khác nhau (NFC, NFD, NFKC, NFKD) với mục đích khác nhau.
* NFC thường được dùng để so sánh chuỗi vì nó giữ nguyên ý nghĩa và rút gọn chuỗi.
* NFKC/NFKD thay thế các ký tự tương thích bằng dạng chuẩn, đôi khi làm thay đổi ý nghĩa.

Để hiểu rõ hơn về chuẩn hóa Unicode và các dạng NFC, NFD, NFKC, NFKD, chúng ta cùng xem xét một số ví dụ cụ thể:

**1. Ký tự có dấu:**

- Chữ "á" có thể được biểu diễn bằng một ký tự Unicode duy nhất (U+00E1) hoặc bằng sự kết hợp của ký tự "a" (U+0061) và dấu sắc (U+0301).
    - `s1 = 'á'`
    - `s2 = 'a\u0301'`
- Khi chuẩn hóa NFC, cả `s1` và `s2` đều trở thành 'á' (U+00E1).
- Khi chuẩn hóa NFD, cả `s1` và `s2` đều trở thành 'a\u0301'.

**2. Ký tự đặc biệt:**

- Ký hiệu "½" (U+00BD) có thể được chuẩn hóa NFKC thành chuỗi "1⁄2".
    - `s = '½'`
    - `normalize('NFKC', s)` -> `'1⁄2'`
- Ký hiệu "µ" (U+00B5) có thể được chuẩn hóa NFKC thành ký tự "μ" (U+03BC).
    - `s = 'µ'`
    - `normalize('NFKC', s)` -> `'μ'`

**3. Chuỗi ký tự hỗn hợp:**

- Chuỗi "café ½" có thể được chuẩn hóa theo nhiều cách khác nhau:
    - NFC: "café ½"
    - NFD: "cafe\u0301 ½"
    - NFKC: "cafe\u0301 1⁄2"
    - NFKD: "cafe\u0301 1⁄2"

**Ứng dụng:**

- **So sánh chuỗi:** Chuẩn hóa giúp so sánh chuỗi chính xác hơn, không bị ảnh hưởng bởi các dạng biểu diễn khác nhau của cùng một ký tự. Ví dụ:
    - `normalize('NFC', 'cafe\u0301') == normalize('NFC', 'café')` -> `True`
- **Tìm kiếm:** Chuẩn hóa giúp tìm kiếm văn bản hiệu quả hơn, bao gồm cả các trường hợp có dấu phụ hoặc ký tự đặc biệt.
- **Xử lý dữ liệu:** Chuẩn hóa giúp đảm bảo tính nhất quán của dữ liệu, đặc biệt khi dữ liệu được thu thập từ nhiều nguồn khác nhau.

**Lưu ý:**

- Việc chọn dạng chuẩn hóa nào phụ thuộc vào mục đích sử dụng.
- Nên cẩn thận khi sử dụng NFKC/NFKD vì chúng có thể làm thay đổi ý nghĩa của văn bản.


####  6.1. <a name='CaseFolding'></a>Case Folding

**Case folding** về cơ bản là chuyển đổi tất cả văn bản thành chữ thường, với một số biến đổi bổ sung. Nó được hỗ trợ bởi phương thức `str.casefold()`.

Đối với bất kỳ chuỗi `s` nào chỉ chứa các ký tự latin1, `s.casefold()` tạo ra kết quả giống như `s.lower()`, chỉ với hai ngoại lệ — dấu micro 'µ' được thay đổi thành chữ mu thường Hy Lạp (trông giống nhau trong hầu hết các phông chữ) và chữ Eszett tiếng Đức hoặc “s sắc” (ß) trở thành “ss”:

```python
>>> micro = 'µ'
>>> name(micro)
'MICRO SIGN'
>>> micro_cf = micro.casefold()
>>> name(micro_cf)
'GREEK SMALL LETTER MU'
>>> micro, micro_cf
('µ', 'μ')
>>> eszett = 'ß'
>>> name(eszett)
'LATIN SMALL LETTER SHARP S'
>>> eszett_cf = eszett.casefold()
>>> eszett, eszett_cf
('ß', 'ss')
```

Có gần 300 điểm mã mà `str.casefold()` và `str.lower()` trả về kết quả khác nhau.

Như thường lệ với bất cứ điều gì liên quan đến Unicode, **case folding** là một vấn đề khó với nhiều trường hợp đặc biệt về ngôn ngữ, nhưng nhóm Python cốt lõi đã nỗ lực để cung cấp một giải pháp hy vọng hoạt động cho hầu hết người dùng.

Trong vài phần tiếp theo, chúng ta sẽ sử dụng kiến thức chuẩn hóa của mình để phát triển các hàm tiện ích.


####  6.2. <a name='UtilityFunctionsforNormalizedTextMatching'></a>Utility Functions for Normalized Text Matching

Như chúng ta đã thấy, NFC và NFD an toàn để sử dụng và cho phép so sánh hợp lý giữa các chuỗi Unicode. NFC là dạng chuẩn hóa tốt nhất cho hầu hết các ứng dụng. `str.casefold()` là cách để thực hiện so sánh không phân biệt chữ hoa chữ thường.

Nếu bạn làm việc với văn bản bằng nhiều ngôn ngữ, một cặp hàm như `nfc_equal` và `fold_equal` trong Ví dụ 4-13 là những bổ sung hữu ích cho bộ công cụ của bạn.

**Ví dụ 4-13:** normeq.py: so sánh chuỗi Unicode được chuẩn hóa

```python
"""
Các hàm tiện ích cho so sánh chuỗi Unicode được chuẩn hóa.

Sử dụng Normal Form C, phân biệt chữ hoa chữ thường:
>>> s1 = 'café'
>>> s2 = 'cafe\u0301'
>>> s1 == s2
False
>>> nfc_equal(s1, s2)
True
>>> nfc_equal('A', 'a')
False

Sử dụng Normal Form C với case folding:
>>> s3 = 'Straße'
>>> s4 = 'strasse'
>>> s3 == s4
False
>>> nfc_equal(s3, s4)
False
>>> fold_equal(s3, s4)
True
>>> fold_equal(s1, s2)
True
>>> fold_equal('A', 'a')
True
"""

from unicodedata import normalize


def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)


def fold_equal(str1, str2):
    return (normalize('NFC', str1).casefold() ==
            normalize('NFC', str2).casefold())
```

Ngoài chuẩn hóa Unicode và case folding — cả hai đều là một phần của tiêu chuẩn Unicode — đôi khi việc áp dụng các phép biến đổi sâu hơn là hợp lý, chẳng hạn như thay đổi 'café' thành 'cafe'. Chúng ta sẽ xem xét khi nào và như thế nào trong phần tiếp theo.

####  6.3. <a name='ExtremeNormalization:TakingOutDiacritics-Chunhaccoan:Loibduph'></a>Extreme “Normalization”: Taking Out Diacritics - Chuẩn hóa "cực đoan": Loại bỏ dấu phụ

Bí quyết của Google Search liên quan đến nhiều thủ thuật, nhưng một trong số đó rõ ràng là bỏ qua dấu phụ (ví dụ: dấu trọng âm, cedilla, v.v.), ít nhất là trong một số ngữ cảnh. Loại bỏ dấu phụ không phải là một hình thức chuẩn hóa phù hợp vì nó thường làm thay đổi nghĩa của từ và có thể tạo ra kết quả dương tính giả khi tìm kiếm. Nhưng nó giúp đối phó với một số sự thật của cuộc sống: đôi khi mọi người lười biếng hoặc thiếu hiểu biết về cách sử dụng dấu phụ chính xác và các quy tắc chính tả thay đổi theo thời gian, nghĩa là dấu trọng âm đến rồi đi trong các ngôn ngữ sống.

Ngoài tìm kiếm, việc loại bỏ dấu phụ cũng giúp URL dễ đọc hơn, ít nhất là trong các ngôn ngữ dựa trên tiếng Latinh. Hãy xem URL cho bài viết trên Wikipedia về thành phố São Paulo:

[https://en.wikipedia.org/wiki/S%C3%A3o_Paulo](https://en.wikipedia.org/wiki/S%C3%A3o_Paulo)

Phần `%C3%A3` là phần được thoát URL, kết xuất UTF-8 của một chữ cái “ã” (“a” có dấu ngã). Điều sau đây dễ nhận ra hơn nhiều, ngay cả khi nó không phải là cách viết đúng:

[https://en.wikipedia.org/wiki/Sao_Paulo](https://en.wikipedia.org/wiki/Sao_Paulo)

Để loại bỏ tất cả dấu phụ khỏi `str`, bạn có thể sử dụng một hàm như Ví dụ 4-14.

**Ví dụ 4-14:** simplify.py: hàm để loại bỏ tất cả các dấu kết hợp

```python
import unicodedata
import string


def shave_marks(txt):
    """Loại bỏ tất cả dấu phụ"""
    norm_txt = unicodedata.normalize('NFD', txt)  # Phân tách tất cả các ký tự thành ký tự cơ sở và dấu kết hợp.
    shaved = ''.join(c for c in norm_txt
                    if not unicodedata.combining(c))  # Lọc ra tất cả các dấu kết hợp.
    return unicodedata.normalize('NFC', shaved)  # Kết hợp lại tất cả các ký tự.
```

Ví dụ 4-15 cho thấy một vài cách sử dụng `shave_marks`.

**Ví dụ 4-15:** Hai ví dụ sử dụng `shave_marks` từ Ví dụ 4-14

```python
>>> order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
>>> shave_marks(order)
'“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai.”'
>>> Greek = 'Ζέφυρος, Zéfiro'
>>> shave_marks(Greek)
'Ζεφυρος, Zefiro'
```

* Chỉ các chữ cái “è”, “ç” và “í” đã được thay thế.
* Cả “έ” và “é” đều đã được thay thế.

Hàm `shave_marks` từ Ví dụ 4-14 hoạt động tốt, nhưng có thể nó đi quá xa. Thông thường lý do để loại bỏ dấu phụ là để thay đổi văn bản Latinh thành ASCII thuần túy, nhưng `shave_marks` cũng thay đổi các ký tự không phải Latinh — như chữ cái Hy Lạp — sẽ không bao giờ trở thành ASCII chỉ bằng cách mất dấu trọng âm. Vì vậy, việc phân tích từng ký tự cơ sở và chỉ loại bỏ các dấu được đính kèm nếu ký tự cơ sở là một chữ cái từ bảng chữ cái Latinh là điều hợp lý. Đây là những gì Ví dụ 4-16 thực hiện.

**Ví dụ 4-16:** Hàm để loại bỏ các dấu kết hợp khỏi các ký tự Latinh (các câu lệnh import bị bỏ qua vì đây là một phần của mô-đun simplify.py từ Ví dụ 4-14)

```python
def shave_marks_latin(txt):
    """Loại bỏ tất cả dấu phụ khỏi các ký tự cơ sở Latinh"""
    norm_txt = unicodedata.normalize('NFD', txt)  # Phân tách tất cả các ký tự thành ký tự cơ sở và dấu kết hợp.
    latin_base = False
    preserve = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue  # bỏ qua dấu phụ trên ký tự cơ sở Latinh
        preserve.append(c)
        # nếu nó không phải là ký tự kết hợp, thì đó là ký tự cơ sở mới
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters  # Phát hiện ký tự cơ sở mới và xác định xem nó có phải là Latinh không.
    shaved = ''.join(preserve)
    return unicodedata.normalize('NFC', shaved)  # Kết hợp lại tất cả các ký tự.
```

Một bước thậm chí còn triệt để hơn là thay thế các ký hiệu phổ biến trong văn bản phương Tây (ví dụ: dấu ngoặc kép cong, dấu gạch ngang em, dấu đầu dòng, v.v.) thành các ký tự ASCII tương đương. Đây là những gì hàm `asciize` thực hiện trong Ví dụ 4-17.

**Ví dụ 4-17:** Biến đổi một số ký hiệu in ấn phương Tây thành ASCII (đoạn mã này cũng là một phần của simplify.py từ Ví dụ 4-14)

```python
single_map = str.maketrans("""‚ƒ„ˆ‹‘’“”•–—˜›""",
                          """'f"^<''""---~>""")  # Xây dựng bảng ánh xạ để thay thế ký tự thành ký tự.
multi_map = str.maketrans({
    '€': 'EUR',
    '…': '...',
    'Æ': 'AE',
    'æ': 'ae',
    'Œ': 'OE',
    'œ': 'oe',
    '™': '(TM)',
    '‰': '<per mille>',
    '†': '**',
    '‡': '***',
})  # Xây dựng bảng ánh xạ để thay thế ký tự thành chuỗi.
multi_map.update(single_map)  # Hợp nhất các bảng ánh xạ.


def dewinize(txt):
    """Thay thế các ký hiệu Win1252 bằng các ký tự hoặc chuỗi ASCII"""
    return txt.translate(multi_map)


def asciize(txt):
    no_marks = shave_marks_latin(dewinize(txt))  # Áp dụng dewinize và loại bỏ dấu phụ.
    no_marks = no_marks.replace('ß', 'ss')  # Thay thế Eszett bằng “ss” (chúng tôi không sử dụng case fold ở đây vì chúng tôi muốn giữ nguyên trường hợp).
    return unicodedata.normalize('NFKC', no_marks)  # Áp dụng chuẩn hóa NFKC để soạn các ký tự với các điểm mã tương thích của chúng.
```

* `dewinize` không ảnh hưởng đến văn bản ASCII hoặc latin1, chỉ ảnh hưởng đến các bổ sung của Microsoft cho latin1 trong cp1252.

Ví dụ 4-18 cho thấy `asciize` đang được sử dụng.

**Ví dụ 4-18:** Hai ví dụ sử dụng `asciize` từ Ví dụ 4-17

```python
>>> order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
>>> dewinize(order)
'"Herr Voß: - ½ cup of OEtker(TM) caffè latte - bowl of açaí."'
>>> asciize(order)
'"Herr Voss: - 1⁄2 cup of OEtker(TM) caffe latte - bowl of acai."'
```

* `dewinize` thay thế dấu ngoặc kép cong, dấu đầu dòng và ™ (ký hiệu thương hiệu).
* `asciize` áp dụng `dewinize`, bỏ dấu phụ và thay thế 'ß'.

Tóm lại, các hàm trong simplify.py vượt xa chuẩn hóa tiêu chuẩn và thực hiện phẫu thuật sâu trên văn bản, với khả năng cao thay đổi nghĩa của nó. Chỉ bạn mới có thể quyết định có nên đi xa đến vậy hay không, biết ngôn ngữ đích, người dùng của bạn và cách văn bản được chuyển đổi sẽ được sử dụng.

Điều này kết thúc cuộc thảo luận của chúng ta về việc chuẩn hóa văn bản Unicode.

Bây giờ hãy sắp xếp việc sắp xếp Unicode.

###  7. <a name='SortingUnicodeText'></a>Sorting Unicode Text

Python sắp xếp các chuỗi (sequence) thuộc bất kỳ kiểu nào bằng cách so sánh các mục trong mỗi chuỗi từng cái một. Đối với chuỗi ký tự, điều này có nghĩa là so sánh các điểm mã (code point). Thật không may, điều này tạo ra kết quả không thể chấp nhận được đối với bất kỳ ai sử dụng ký tự không phải ASCII.

Hãy xem xét việc sắp xếp danh sách các loại trái cây được trồng ở Brazil:

```python
>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted(fruits)
['acerola', 'atemoia', 'açaí', 'caju', 'cajá']
```

Các quy tắc sắp xếp khác nhau đối với các locale khác nhau, nhưng trong tiếng Bồ Đào Nha và nhiều ngôn ngữ sử dụng bảng chữ cái Latinh, dấu trọng âm và cedilla hiếm khi tạo ra sự khác biệt khi sắp xếp. Vì vậy, “cajá” được sắp xếp như “caja” và phải đứng trước “caju.”

Danh sách trái cây được sắp xếp phải là:

```
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
```

Cách tiêu chuẩn để sắp xếp văn bản không phải ASCII trong Python là sử dụng hàm `locale.strxfrm` mà theo tài liệu mô-đun locale, “biến đổi một chuỗi thành một chuỗi có thể được sử dụng trong các phép so sánh nhận biết locale.”

Để bật `locale.strxfrm`, trước tiên bạn phải đặt một locale phù hợp cho ứng dụng của mình và cầu nguyện rằng hệ điều hành hỗ trợ nó. Chuỗi lệnh trong Ví dụ 4-19 có thể phù hợp với bạn.

**Ví dụ 4-19:** locale_sort.py: sử dụng hàm `locale.strxfrm` làm khóa sắp xếp

```python
import locale

my_locale = locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
print(my_locale)

fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=locale.strxfrm)
print(sorted_fruits)
```

Chạy Ví dụ 4-19 trên GNU/Linux (Ubuntu 19.10) với locale pt_BR.UTF-8 được cài đặt, tôi nhận được kết quả chính xác:

```
'pt_BR.UTF-8'
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
```

Vì vậy, bạn cần gọi `setlocale(LC_COLLATE, «your_locale») ` trước khi sử dụng `locale.strxfrm` làm khóa khi sắp xếp.

Tuy nhiên, có một số lưu ý:

* Vì cài đặt locale là toàn cục, nên không khuyến khích gọi `setlocale` trong thư viện. Ứng dụng hoặc framework của bạn nên đặt locale khi quá trình bắt đầu và không nên thay đổi sau đó.
* Locale phải được cài đặt trên hệ điều hành, nếu không `setlocale` sẽ tạo ra ngoại lệ `locale.Error: unsupported locale setting`.
* Bạn phải biết cách viết tên locale.
* Locale phải được triển khai chính xác bởi các nhà sản xuất hệ điều hành. Tôi đã thành công trên Ubuntu 19.10, nhưng không thành công trên macOS 10.14. Trên macOS, lệnh gọi `setlocale(LC_COLLATE, 'pt_BR.UTF-8')` trả về chuỗi 'pt_BR.UTF-8' mà không có khiếu nại. Nhưng `sorted(fruits, key=locale.strxfrm)` tạo ra kết quả không chính xác giống như `sorted(fruits)` đã làm. Tôi cũng đã thử các locale fr_FR, es_ES và de_DE trên macOS, nhưng `locale.strxfrm` không bao giờ thực hiện được công việc của nó.

Vì vậy, giải pháp thư viện tiêu chuẩn để sắp xếp quốc tế hóa hoạt động, nhưng dường như chỉ được hỗ trợ tốt trên GNU/Linux (có lẽ cũng trên Windows, nếu bạn là chuyên gia). Ngay cả khi đó, nó phụ thuộc vào cài đặt locale, tạo ra sự cố khi triển khai.

May mắn thay, có một giải pháp đơn giản hơn: thư viện pyuca, có sẵn trên PyPI.

####  7.1. <a name='SortingwiththeUnicodeCollationAlgorithm'></a>Sorting with the Unicode Collation Algorithm

James Tauber, người đóng góp nhiều cho Django, hẳn đã cảm nhận được nỗi đau và tạo ra pyuca, một triển khai thuần Python của Thuật toán đối chiếu Unicode (UCA). Ví dụ 4-20 cho thấy cách sử dụng nó dễ dàng như thế nào.

**Ví dụ 4-20:** Sử dụng phương thức `pyuca.Collator.sort_key`

```python
>>> import pyuca
>>> coll = pyuca.Collator()
>>> fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
>>> sorted_fruits = sorted(fruits, key=coll.sort_key)
>>> sorted_fruits
['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
```

Điều này thật đơn giản và hoạt động trên GNU/Linux, macOS và Windows, ít nhất là với mẫu nhỏ của tôi.

pyuca không tính đến locale. Nếu bạn cần tùy chỉnh việc sắp xếp, bạn có thể cung cấp đường dẫn đến bảng đối chiếu tùy chỉnh cho hàm tạo `Collator()`. Ngoài ra, nó sử dụng allkeys.txt, được đóng gói cùng với dự án. Đó chỉ là một bản sao của Bảng phần tử đối chiếu Unicode mặc định từ Unicode.org.

Nhân tiện, bảng đối chiếu đó là một trong nhiều tệp dữ liệu bao gồm cơ sở dữ liệu Unicode, chủ đề tiếp theo của chúng ta.

###  8. <a name='TheUnicodeDatabase'></a>The Unicode Database

Tiêu chuẩn Unicode cung cấp toàn bộ cơ sở dữ liệu — dưới dạng một số tệp văn bản có cấu trúc — không chỉ bao gồm bảng ánh xạ các điểm mã (code point) tới tên ký tự mà còn có siêu dữ liệu (metadata) về các ký tự riêng lẻ và cách chúng liên quan với nhau. Ví dụ: cơ sở dữ liệu Unicode ghi lại xem một ký tự có thể in được hay không, là một chữ cái, là một chữ số thập phân hay là một số ký hiệu số khác. Đó là cách các phương thức `str.isalpha`, `isprintable`, `isdecimal` và `isnumeric` hoạt động. `str.casefold` cũng sử dụng thông tin từ bảng Unicode.

####  8.1. <a name='FindingCharactersbyName'></a>Finding Characters by Name

###  9. <a name='Tmkimkttheotn'></a>Tìm kiếm ký tự theo tên

Mô-đun `unicodedata` có các hàm để truy xuất siêu dữ liệu ký tự, bao gồm `unicodedata.name()`, trả về tên chính thức của ký tự theo tiêu chuẩn. Hình 4-5 minh họa chức năng đó.

![]({{site.url}}/images/finding-character-by-name.png)

Bạn có thể sử dụng hàm `name()` để xây dựng các ứng dụng cho phép người dùng tìm kiếm ký tự theo tên. Hình 4-6 minh họa tập lệnh dòng lệnh cf.py lấy một hoặc nhiều từ làm đối số và liệt kê các ký tự có các từ đó trong tên Unicode chính thức của chúng. Mã nguồn đầy đủ cho cf.py có trong Ví dụ 4-21.

![]({{site.url}}/images/finding-character-by-name-2.png)

Trong Ví dụ 4-21, lưu ý câu lệnh `if` trong hàm `find` sử dụng phương thức `.issubset()` để kiểm tra nhanh xem tất cả các từ trong tập hợp truy vấn có xuất hiện trong danh sách các từ được xây dựng từ tên của ký tự hay không. Nhờ API set phong phú của Python, chúng ta không cần vòng lặp `for` lồng nhau và một câu lệnh `if` khác để thực hiện kiểm tra này.

**Ví dụ 4-21:** cf.py: tiện ích tìm kiếm ký tự

```python
#!/usr/bin/env python3
import sys
import unicodedata

START, END = ord(' '), sys.maxunicode + 1  # Đặt giá trị mặc định cho phạm vi điểm mã để tìm kiếm.

def find(*query_words, start=START, end=END):
    """
    find chấp nhận query_words và các đối số chỉ từ khóa tùy chọn để giới hạn phạm vi tìm kiếm, 
    để tạo điều kiện thuận lợi cho việc kiểm tra.
    """
    query = {w.upper() for w in query_words}  # Chuyển đổi query_words thành một tập hợp các chuỗi được viết hoa.
    for code in range(start, end):
        char = chr(code)  # Lấy ký tự Unicode cho mã.
        name = unicodedata.name(char, None)  # Lấy tên của ký tự hoặc None nếu điểm mã không được gán.
        if name and query.issubset(name.split()):  # Nếu có tên, hãy tách nó thành một danh sách các từ, sau đó kiểm tra xem tập hợp truy vấn có phải là tập hợp con của danh sách đó hay không.
            print(f'U+{code:04X}\t{char}\t{name}')  # In ra dòng với điểm mã ở định dạng U+9999, ký tự và tên của nó.


def main(words):
    if words:
        find(*words)
    else:
        print('Please provide words to find.')


if __name__ == '__main__':
    main(sys.argv[1:])
```

Mô-đun `unicodedata` có các hàm thú vị khác. Tiếp theo, chúng ta sẽ thấy một số hàm liên quan đến việc lấy thông tin từ các ký tự có ý nghĩa số.

####  9.1. <a name='NumericMeaningofCharacters'></a>Numeric Meaning of Characters

Mô-đun `unicodedata` bao gồm các hàm để kiểm tra xem một ký tự Unicode có biểu thị một số hay không và nếu có, giá trị số của nó đối với con người — trái ngược với số điểm mã (code point) của nó. Ví dụ 4-22 cho thấy cách sử dụng `unicodedata.name()` và `unicodedata.numeric()`, cùng với các phương thức `.isdecimal()` và `.isnumeric()` của `str`.

**Ví dụ 4-22:** Bản demo siêu dữ liệu ký tự số của cơ sở dữ liệu Unicode (các chú thích mô tả từng cột trong đầu ra)

```python
import unicodedata
import re

re_digit = re.compile(r'\d')
sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
    print(f'U+{ord(char):04x}',  # Điểm mã ở định dạng U+0000.
          char.center(6),  # Ký tự được căn giữa trong một chuỗi str có độ dài 6.
          're_dig' if re_digit.match(char) else '-',  # Hiển thị re_dig nếu ký tự khớp với biểu thức chính quy r'\d'.
          'isdig' if char.isdigit() else '-',  # Hiển thị isdig nếu char.isdigit() là True.
          'isnum' if char.isnumeric() else '-',  # Hiển thị isnum nếu char.isnumeric() là True.
          f'{unicodedata.numeric(char):5.2f}',  # Giá trị số được định dạng với chiều rộng 5 và 2 chữ số thập phân.
          unicodedata.name(char),  # Tên ký tự Unicode
          sep='\t')
```

Cột thứ sáu của Hình 4-7 là kết quả của việc gọi `unicodedata.numeric(char)` trên ký tự. Nó cho thấy rằng Unicode biết giá trị số của các ký hiệu đại diện cho số. Vì vậy, nếu bạn muốn tạo một ứng dụng bảng tính hỗ trợ chữ số Tamil hoặc chữ số La Mã, hãy thử sức!

Hình 4-7 cho thấy biểu thức chính quy `r'\d'` khớp với chữ số “1” và chữ số Devanagari 3, nhưng không phải một số ký tự khác được hàm `isdigit` coi là chữ số. Mô-đun `re` không hiểu biết nhiều về Unicode như nó có thể. Mô-đun `regex` mới có sẵn trên PyPI được thiết kế để cuối cùng thay thế `re` và cung cấp hỗ trợ Unicode tốt hơn. Chúng ta sẽ quay lại mô-đun `re` trong phần tiếp theo.

Trong suốt chương này, chúng ta đã sử dụng một số hàm `unicodedata`, nhưng có nhiều hàm nữa mà chúng ta chưa đề cập đến. Xem tài liệu thư viện tiêu chuẩn cho mô-đun `unicodedata`.

Tiếp theo, chúng ta sẽ xem xét nhanh các API chế độ kép cung cấp các hàm chấp nhận đối số `str` hoặc `bytes` với cách xử lý đặc biệt tùy thuộc vào loại.

###  10. <a name='Dual-ModestrandbytesAPIs'></a>Dual-Mode str and bytes APIs

####  10.1. <a name='strVersusbytesinRegularExpressions'></a>str Versus bytes in Regular Expressions

Nếu bạn xây dựng một biểu thức chính quy với `bytes`, các mẫu như `\d` và `\w` chỉ khớp với các ký tự ASCII; ngược lại, nếu các mẫu này được đưa ra dưới dạng `str`, chúng sẽ khớp với các chữ số hoặc chữ cái Unicode ngoài ASCII. Ví dụ 4-23 và Hình 4-8 so sánh cách các chữ cái, chữ số ASCII, ký tự trên và chữ số Tamil được khớp bởi các mẫu `str` và `bytes`.

**Ví dụ 4-23:** ramanujan.py: so sánh hành vi của biểu thức chính quy `str` và `bytes` đơn giản

```python
import re

re_numbers_str = re.compile(r'\d+')  # Hai biểu thức chính quy đầu tiên thuộc loại str.
re_words_str = re.compile(r'\w+')
re_numbers_bytes = re.compile(rb'\d+')  # Hai biểu thức chính quy cuối cùng thuộc loại bytes.
re_words_bytes = re.compile(rb'\w+')

text_str = ("Ramanujan saw \u0be7\u0bed\u0be8\u0bef"  # Văn bản Unicode để tìm kiếm, chứa các chữ số Tamil cho 1729 (dòng logic tiếp tục cho đến mã thông báo dấu ngoặc đơn bên phải).
            " as 1729 = 1³ + 12³ = 9³ + 10³.")  # Chuỗi này được nối với chuỗi trước đó tại thời điểm biên dịch (xem “2.4.2. Nối chuỗi ký tự” trong Tài liệu tham khảo ngôn ngữ Python).
text_bytes = text_str.encode('utf_8')  # Cần có chuỗi bytes để tìm kiếm bằng các biểu thức chính quy bytes.

print(f'Text\n {text_str!r}')
print('Numbers')
print('  str :', re_numbers_str.findall(text_str))  # Mẫu str r'\d+' khớp với các chữ số Tamil và ASCII.
print(' bytes:', re_numbers_bytes.findall(text_bytes))  # Mẫu bytes rb'\d+' chỉ khớp với các byte ASCII cho chữ số.
print('Words')
print('  str :', re_words_str.findall(text_str))  # Mẫu str r'\w+' khớp với các chữ cái, ký tự trên, chữ số Tamil và ASCII.
print(' bytes:', re_words_bytes.findall(text_bytes))  # Mẫu bytes rb'\w+' chỉ khớp với các byte ASCII cho chữ cái và chữ số.
```

Đối với biểu thức chính quy `str`, có cờ `re.ASCII` làm cho `\w`, `\W`, `\b`, `\B`, `\d`, `\D`, `\s` và `\S` chỉ thực hiện khớp ASCII. Xem tài liệu của mô-đun `re` để biết đầy đủ chi tiết.

Một mô-đun chế độ kép quan trọng khác là `os`.


####  10.2. <a name='strVersusbytesinosFunctions'></a>str Versus bytes in os Functions

Nhân Linux không hiểu biết nhiều về Unicode, vì vậy trong thế giới thực, bạn có thể tìm thấy tên tệp được tạo thành từ các chuỗi byte không hợp lệ trong bất kỳ lược đồ mã hóa hợp lý nào và không thể được giải mã thành `str`. Các máy chủ tệp có máy khách sử dụng nhiều hệ điều hành khác nhau đặc biệt dễ gặp phải sự cố này.

Để giải quyết vấn đề này, tất cả các hàm mô-đun `os` chấp nhận tên tệp hoặc tên đường dẫn đều lấy đối số dưới dạng `str` hoặc `bytes`. Nếu một hàm như vậy được gọi với đối số `str`, đối số sẽ được tự động chuyển đổi bằng cách sử dụng codec được đặt tên bởi `sys.getfilesystemencoding()` và phản hồi của hệ điều hành sẽ được giải mã bằng cùng một codec. Đây hầu như luôn là điều bạn muốn, phù hợp với phương pháp hay nhất của Unicode sandwich.

Nhưng nếu bạn phải xử lý (và có thể sửa) các tên tệp không thể xử lý theo cách đó, bạn có thể chuyển các đối số `bytes` cho các hàm `os` để nhận các giá trị trả về `bytes`. Tính năng này cho phép bạn xử lý bất kỳ tệp hoặc tên đường dẫn nào, bất kể bạn có thể tìm thấy bao nhiêu gremlin. Xem Ví dụ 4-24.

**Ví dụ 4-24:** `listdir` với các đối số và kết quả `str` và `bytes`

```python
>>> os.listdir('.')
['abc.txt', 'digits-of-π.txt']
>>> os.listdir(b'.')
[b'abc.txt', b'digits-of-\xcf\x80.txt']
```

* Tên tệp thứ hai là “digits-of-π.txt” (với chữ cái Hy Lạp pi).
* Với đối số byte, `listdir` trả về tên tệp dưới dạng byte: `b'\xcf\x80'` là mã hóa UTF-8 của chữ cái Hy Lạp pi.

Để giúp xử lý thủ công các chuỗi `str` hoặc `bytes` là tên tệp hoặc tên đường dẫn, mô-đun `os` cung cấp các hàm mã hóa và giải mã đặc biệt `os.fsencode(name_or_path)` và `os.fsdecode(name_or_path)`. Cả hai hàm này đều chấp nhận một đối số thuộc loại `str`, `bytes` hoặc một đối tượng triển khai giao diện `os.PathLike` kể từ Python 3.6.

Unicode là một hang thỏ sâu. Đã đến lúc kết thúc chuyến khám phá `str` và `bytes` của chúng ta.
