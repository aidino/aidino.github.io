---
layout: post
title: "Building LLMs for Production"
date: 2025-02-25 07:00:00 +0700
categories: developing large language models
---

Cuốn sách này mang đến một cách tiếp cận độc đáo, thực hành và thực tế, đồng thời cân bằng giữa lý thuyết và khái niệm. Sách giới thiệu các xu hướng mới nhất trong xử lý ngôn ngữ tự nhiên (Natural Language Processing - **NLP**), chủ yếu là các mô hình ngôn ngữ lớn (Large Language Models - **LLMs**), cung cấp cái nhìn sâu sắc về cách các mạng này hoạt động. Ngoài ra, sách còn bao gồm các dự án minh họa ứng dụng của các mô hình này trong việc tạo ra các pipeline sinh dữ liệu tăng cường truy xuất (Retrieval-Augmented Generation - **RAG**). Những khái niệm này đại diện cho những phát triển tiên tiến trong lĩnh vực, cho phép chúng ta xử lý văn bản viết và tương tác với nó ở cấp độ ngữ cảnh.

Giống như hầu hết các cuốn sách liên quan đến **LLMs**, chúng ta bắt đầu với nền tảng bằng cách khám phá chi tiết kiến trúc **transformer** để hiểu cách các mô hình này được đào tạo và cách tương tác với chúng bằng kỹ thuật **prompting**. Sau đó, chúng ta đi sâu vào các phần tập trung vào ngành, đầu tiên là bao gồm hai frameworks nổi tiếng có thể được sử dụng để tận dụng các mô hình này để tạo ra các ứng dụng hỗ trợ **RAG** (LlamaIndex và LangChain). Điều này bao gồm nhiều dự án cung cấp trải nghiệm thực hành, giúp hiểu sâu sắc và áp dụng các khái niệm này. Chúng ta cũng khám phá các kỹ thuật nâng cao, chẳng hạn như sử dụng các **autonomous agents** hoặc kết hợp khả năng thị giác để nâng cao khả năng trả lời câu hỏi. Cuối cùng, chúng ta khám phá các tùy chọn triển khai để lưu trữ ứng dụng và các mẹo để làm cho quá trình hiệu quả hơn.

Cuốn sách này được thiết kế cho những độc giả không có kiến thức trước về trí tuệ nhân tạo hoặc **NLP**. Sách giới thiệu các chủ đề từ cơ bản, nhằm giúp bạn cảm thấy thoải mái khi sử dụng sức mạnh của AI trong dự án tiếp theo hoặc nâng dự án hiện tại của bạn lên một tầm cao mới. Hiểu biết cơ bản về Python giúp hiểu mã và các triển khai, trong khi các trường hợp sử dụng nâng cao của các kỹ thuật mã hóa được giải thích chi tiết trong sách. Mỗi chương của cuốn sách giới thiệu một chủ đề mới, tiếp theo là một dự án thực tế và triển khai đi kèm (dưới dạng Google Colab Notebooks) để chạy mã và tái tạo kết quả. Cách tiếp cận thực hành này giúp hiểu các khái niệm và áp dụng chúng một cách hiệu quả. Đây là tổng quan ngắn gọn về những gì mong đợi trong mỗi chương:

**Chương I: Giới thiệu về LLMs**

Bước đầu tiên để tận dụng AI cho dự án của bạn là hiểu những gì đang diễn ra bên trong. Mặc dù bạn có thể không cần tạo mô hình của riêng mình từ đầu và có thể sử dụng các API độc quyền (như OpenAI), nhưng việc hiểu các khái niệm như **Scaling Laws**, **Context Windows**, **Emergent Abilities** giải thích tại sao **LLMs** lại mạnh mẽ đến vậy. Chương đầu tiên tập trung vào thuật ngữ cơ bản của **LLM**, điều này rất quan trọng để hiểu phần còn lại của cuốn sách một cách hiệu quả. Ngoài ra, chúng tôi cung cấp các ví dụ đơn giản về việc sử dụng **LLMs** cho các tác vụ như dịch thuật hoặc xác định các mẫu từ dữ liệu, cho phép bạn tổng quát hóa cho các tác vụ mới và chưa từng thấy.

**Chương II: Kiến trúc LLM và Bối cảnh**

Chương này sẽ khám phá các kiến trúc mô hình khác nhau và các lựa chọn thiết kế của chúng cho các tác vụ khác nhau, tập trung vào kiến trúc **transformer** và các thành phần của nó ở mỗi lớp, cũng như họ mô hình GPT, cung cấp sức mạnh cho các sản phẩm như ChatGPT. Chúng tôi đề cập đến các mục tiêu đào tạo của các mô hình này, giới thiệu một loạt các mô hình, thảo luận về tính hữu ích của chúng, khám phá các ứng dụng thực tế của chúng và minh họa cách chúng cung cấp sức mạnh cho các ngành công nghiệp khác nhau.

Đây thường là nơi các trường học kết thúc, và cuốn sách thực sự bắt đầu!

**Chương III: LLMs trong Thực tiễn**

Trong thực tế, **LLMs** vẫn có những hạn chế. Vượt qua những hạn chế này để làm cho chúng sẵn sàng cho sản xuất là lý do tại sao chúng tôi quyết định viết cuốn sách này. Chương này khám phá một số vấn đề đã biết với họ mô hình này, chẳng hạn như ảo giác (hallucination), nơi mô hình tạo ra các phản hồi sai lệch về mặt thực tế với độ tin cậy cao hoặc thiên vị đối với giới tính hoặc chủng tộc. Sách nhấn mạnh tầm quan trọng của việc tận dụng các frameworks đánh giá để đánh giá phản hồi và thử nghiệm với các siêu tham số khác nhau để kiểm soát đầu ra của mô hình, chẳng hạn như các kỹ thuật giải mã khác nhau hoặc điều chỉnh độ sáng tạo của mô hình thông qua tham số nhiệt độ (temperature).

**Chương IV: Giới thiệu về Prompting**

Một cuốn sách về **LLMs** phải bao gồm một chương về **prompting**: cách chúng ta nói chuyện với chúng. Cách tốt nhất để tương tác với **instruction-tuned LLMs** (các mô hình được đào tạo để trả lời câu hỏi) là trực tiếp đặt câu hỏi hoặc nêu những gì bạn muốn mô hình làm. Quá trình này, được gọi là **prompting**, đã phát triển thành một thực hành tinh vi. Trong chương này, chúng tôi kiểm tra các kỹ thuật **prompting** khác nhau với các ví dụ mã. Chúng tôi đề cập đến các phương pháp như học ít lần (few-shot learning), nơi bạn cung cấp một vài ví dụ cho mô hình, **chain prompting**, hữu ích khi gán danh tính cho mô hình, và hơn thế nữa.

**Chương V: Giới thiệu về LangChain & LlamaIndex**

Có hai frameworks chính được sử dụng rộng rãi giúp đơn giản hóa việc làm việc với **LLMs** để giảm ảo giác và thiên vị hoặc dễ dàng triển khai chúng trong quy trình của bạn: các gói LangChain và LlamaIndex. Chương này tập trung vào ý tưởng sử dụng các tài nguyên bên ngoài để nâng cao phản hồi của mô hình, tiếp theo là triển khai các dự án khác nhau, chẳng hạn như một công cụ tóm tắt tin tức cạo một trang web để truy xuất nội dung để tóm tắt. Mục tiêu là học các kiến thức cơ bản của cả hai frameworks và hiểu khi nào chúng hữu ích.

**Chương VI: Prompting với LangChain**

LangChain cung cấp nhiều giao diện cho các kỹ thuật **prompting** khác nhau, điều này làm cho quá trình trực quan hơn. Chúng tôi giải thích việc sử dụng các loại **prompt** khác nhau để đặt các quy tắc cơ bản cho mô hình (hệ thống), tương tác của con người và phản hồi của chatbot để theo dõi các tương tác (tất cả đều có ví dụ thực tế). Ngoài ra, chương này nhấn mạnh tầm quan trọng của việc có một cơ chế kiểm soát để quản lý phản hồi của mô hình. Chúng tôi cũng thảo luận về cách thư viện này cung cấp các cách để nhận phản hồi ở các định dạng cụ thể, chẳng hạn như danh sách Python hoặc CSV, và thậm chí cung cấp các giải pháp để khắc phục sự cố định dạng nếu chúng phát sinh.

**Chương VII: Sinh dữ liệu tăng cường truy xuất (Retrieval-Augmented Generation - RAG)**

Sau khi hiểu các trường hợp sử dụng cơ bản của thư viện LangChain để triển khai một pipeline đơn giản, chương này khám phá chi tiết quá trình và hoạt động bên trong của nó. Chúng tôi tập trung vào việc tạo chỉ mục, các phương pháp khác nhau để tải dữ liệu từ nhiều nguồn dữ liệu khác nhau và chia các phần thông tin lớn thành các phần nhỏ hơn. Chúng tôi cũng khám phá cách lưu trữ thông tin này trong cơ sở dữ liệu để truy cập dễ dàng và nhanh hơn. Chương này cũng bao gồm hai dự án thú vị: phiên âm video YouTube và tóm tắt các điểm chính.

**Chương VIII: RAG Nâng cao**

Chương này giới thiệu các kỹ thuật nâng cao hơn để cải thiện bất kỳ pipeline **RAG** nào. Chúng tôi tập trung vào thư viện LlamaIndex, thư viện liên tục triển khai các giải pháp mới, chẳng hạn như mở rộng truy vấn, truy xuất đệ quy và tìm kiếm kết hợp. Chương này tập trung vào các thách thức tiềm ẩn, kỹ thuật tối ưu hóa và quy trình đánh giá hiệu suất chatbot của bạn. Sách cũng đề cập đến dịch vụ LangSmith, cung cấp một trung tâm để giải quyết các vấn đề khác nhau và một cách để chia sẻ các triển khai của bạn với những người khác trong cộng đồng.

**Chương IX: Agents**

Chương này giới thiệu khái niệm về các **intelligent agents**, có thể tương tác với môi trường bên ngoài. Chúng có thể truy cập dữ liệu từ nhiều tài nguyên khác nhau, gọi API và sử dụng các công cụ như chạy hàm để hoàn thành một tác vụ thành công mà không cần giám sát. Các agents này thường tạo một kế hoạch hành động dựa trên thông số kỹ thuật của người dùng và làm theo từng bước. Chúng tôi bao gồm một số dự án để minh họa cách các công cụ có thể nâng cao pipeline của bạn.

## Introduction

Cuốn sách này sẽ tập trung vào **essential tech stack** được xác định để điều chỉnh một **large language model (LLM)** cho một **specific use case** và đạt được ngưỡng đủ về độ chính xác và độ tin cậy để sử dụng có thể mở rộng bởi khách hàng trả phí. Cụ thể, nó sẽ đề cập đến **Prompt Engineering**, **Fine-tuning**, và **Retrieval-Augmented Generation (RAG)**.

Việc xây dựng các ứng dụng và sản phẩm sẵn sàng sản xuất của riêng bạn bằng cách sử dụng các mô hình này vẫn đòi hỏi một nỗ lực phát triển đáng kể. Do đó, cuốn sách này yêu cầu kiến thức trung cấp về Python. Mặc dù không cần kiến thức lập trình để khám phá các khái niệm cụ thể về AI và LLM trong cuốn sách này, chúng tôi khuyên bạn nên sử dụng danh sách các tài nguyên Python hữu ích và miễn phí để có trải nghiệm học tập thực hành hơn.

Chúng tôi hiện đang làm việc trên một khóa học về Python cho LLMs. Trong thời gian chờ đợi, một vài chương đầu tiên của cuốn sách này vẫn sẽ nhẹ nhàng và dễ hiểu. Song song đó, chúng tôi khuyên bạn nên xem qua Python và các tài nguyên khác mà chúng tôi có để phát triển các kỹ năng và hiểu biết kỹ thuật về AI của bạn. Việc xem qua một hoặc hai tài nguyên Python được liệt kê tại towardsai.net/book là đủ để bạn chuẩn bị cho cuốn sách này. Khi bạn tự tin hơn về kỹ năng lập trình của mình, hãy quay lại các phần tập trung vào code.

Bất chấp những nỗ lực đáng kể của các phòng thí nghiệm AI trung tâm và các nhà phát triển mã nguồn mở trong các lĩnh vực như **Reinforcement Learning with Human Feedback** để điều chỉnh các **foundation models** theo yêu cầu và **use cases** của con người, các **off-the-shelf foundation models** vẫn có những hạn chế hạn chế việc sử dụng trực tiếp của chúng trong sản xuất, ngoại trừ các tác vụ đơn giản nhất.

Có nhiều cách để điều chỉnh một **off-the-shelf “foundation model” LLM** cho một ứng dụng và **use case** cụ thể. Quyết định ban đầu là có nên sử dụng LLM qua API hay một nền tảng linh hoạt hơn, nơi bạn có toàn quyền truy cập vào **model weights**. Một số người cũng có thể muốn thử nghiệm đào tạo các mô hình của riêng họ; tuy nhiên, theo ý kiến của chúng tôi, điều này hiếm khi thực tế hoặc kinh tế bên ngoài các phòng thí nghiệm AI và công ty công nghệ hàng đầu. Hiện có hơn 5 triệu người đang xây dựng trên LLMs trên các nền tảng như OpenAI, Anthropic, Nvidia và Hugging Face. Cuốn sách này hướng dẫn bạn vượt qua những hạn chế của LLM và phát triển các sản phẩm LLM sẵn sàng sản xuất với các **key tech stacks**!

> "Off-the-shelf “foundation model” LLM" đề cập đến một mô hình ngôn ngữ lớn (LLM) được đào tạo trước (pre-trained) và sẵn sàng sử dụng ngay lập tức, mà không cần phải xây dựng từ đầu.

## Why Prompt Engineering, Fine-Tuning, and RAG?

Các LLM (Large Language Models) như GPT-4 thường thiếu kiến thức domain-specific, gây khó khăn trong việc tạo ra các phản hồi chính xác hoặc phù hợp trong các lĩnh vực chuyên môn. Chúng cũng gặp khó khăn khi xử lý khối lượng dữ liệu lớn, hạn chế tính hữu dụng trong các kịch bản data-intensive. Một hạn chế quan trọng khác là khó khăn trong việc xử lý các thuật ngữ mới hoặc technical, dẫn đến hiểu nhầm hoặc thông tin sai lệch. Hallucinations, khi LLM tạo ra thông tin sai lệch hoặc gây hiểu nhầm, càng làm phức tạp việc sử dụng chúng. Hallucinations là kết quả trực tiếp của mục tiêu huấn luyện mô hình là next token prediction - ở một mức độ nào đó, chúng là một feature cho phép các câu trả lời "creative" của mô hình. Tuy nhiên, LLM khó biết được khi nào nó đang trả lời từ các facts đã ghi nhớ và trí tưởng tượng. Điều này tạo ra nhiều errors trong các workflows được hỗ trợ bởi LLM, khiến chúng khó xác định. Bên cạnh hallucinations, LLM đôi khi cũng đơn giản là không sử dụng dữ liệu có sẵn một cách hiệu quả, dẫn đến các phản hồi không liên quan hoặc không chính xác.

LLM thường được sử dụng trong production cho các use cases "copilot" nhằm nâng cao hiệu suất và năng suất, với con người vẫn hoàn toàn tham gia vào vòng lặp thay vì cho các nhiệm vụ hoàn toàn tự động do những hạn chế này. Nhưng có một hành trình dài từ một basic LLM prompt đến độ chính xác, độ tin cậy và observability đủ cho một target copilot use case. Hành trình này được gọi là "march of 9s" và được phổ biến trong phát triển xe tự lái. Thuật ngữ này mô tả sự cải thiện dần dần về độ tin cậy, thường được đo bằng số lượng nines (ví dụ: độ tin cậy 99,9%) cần thiết để cuối cùng đạt được hiệu suất ngang con người.

Chúng tôi cho rằng bộ công cụ phát triển chính cho "march of 9s" đối với các sản phẩm dựa trên LLM là 

- 1) Prompt Engineering, 
- 2) Retrieval-Augmented Generation (RAG), 
- 3) Fine-Tuning và 
- 4) Custom UI/UX. 

Trong thời gian ngắn, AI có thể hỗ trợ nhiều nhiệm vụ của con người trong nhiều ngành khác nhau bằng cách kết hợp LLM, prompting, RAG và fine-tuning workflows. Chúng tôi tin rằng các công ty "AI" thành công nhất sẽ tập trung vào các giải pháp được tùy chỉnh cao cho các ngành hoặc niches cụ thể và đóng góp nhiều dữ liệu và intelligence/experience dành riêng cho ngành vào cách sản phẩm được phát triển.

RAG bao gồm việc tăng cường LLM bằng dữ liệu cụ thể và yêu cầu mô hình sử dụng và trích dẫn dữ liệu này trong câu trả lời của nó thay vì dựa vào những gì nó có thể hoặc không thể ghi nhớ trong model weights. Chúng tôi thích RAG vì nó giúp:

- 1) Giảm hallucinations bằng cách giới hạn LLM trả lời dựa trên dữ liệu đã chọn hiện có.
- 2) Giúp explainability, error checking và các vấn đề về copyright bằng cách tham khảo rõ ràng các nguồn của nó cho mỗi nhận xét.
- 3) Cung cấp dữ liệu private/specific hoặc cập nhật hơn cho LLM.
- 4) Không dựa quá nhiều vào black box LLM training/fine-tuning cho những gì các mô hình biết và đã ghi nhớ.

Một cách khác để tăng hiệu suất LLM là thông qua good prompting. Nhiều kỹ thuật đã được tìm thấy để cải thiện hiệu suất mô hình. Các phương pháp này có thể đơn giản, chẳng hạn như đưa ra hướng dẫn chi tiết cho mô hình hoặc chia nhỏ các nhiệm vụ lớn thành các nhiệm vụ nhỏ hơn để mô hình dễ xử lý hơn. Một số kỹ thuật prompting là:

- 1) "Chain of Thought" prompting bao gồm việc yêu cầu mô hình suy nghĩ từng bước về một vấn đề trước khi đưa ra câu trả lời cuối cùng. Ý tưởng chính là mỗi token trong một language model có "processing bandwidth" hoặc "thinking capacity" hạn chế. LLM cần các token này để tìm ra mọi thứ. Bằng cách yêu cầu nó suy luận từng bước về một vấn đề, chúng ta sử dụng tổng capacity của mô hình để suy nghĩ và giúp nó đạt được câu trả lời chính xác.
- 2) "Few-Shot Prompting" là khi chúng ta cho mô hình xem các ví dụ về câu trả lời mà chúng ta tìm kiếm dựa trên một số câu hỏi tương tự như những câu hỏi mà chúng ta mong đợi mô hình nhận được. Nó giống như việc cho mô hình thấy một pattern về cách chúng ta muốn nó phản hồi.
- 3) "Self-Consistency" bao gồm việc hỏi cùng một câu hỏi cho nhiều phiên bản của mô hình và sau đó chọn câu trả lời xuất hiện thường xuyên nhất. Phương pháp này giúp có được câu trả lời đáng tin cậy hơn.

Nói tóm lại, good prompting là hướng dẫn mô hình bằng các hướng dẫn rõ ràng, chia nhỏ các nhiệm vụ thành các nhiệm vụ đơn giản hơn và sử dụng các phương pháp cụ thể để cải thiện hiệu suất. Về cơ bản, đó là các bước tương tự mà chúng ta phải làm khi bắt đầu các bài tập mới. Giáo sư giả định bạn biết các concepts và yêu cầu bạn áp dụng chúng một cách thông minh.

Mặt khác, fine-tuning giống như việc cho language model các bài học bổ sung để cải thiện đầu ra cho các nhiệm vụ cụ thể. Ví dụ: nếu bạn muốn mô hình biến các câu thông thường thành truy vấn cơ sở dữ liệu SQL, bạn có thể huấn luyện nó cụ thể cho nhiệm vụ đó. Hoặc, nếu bạn cần mô hình phản hồi bằng câu trả lời ở định dạng JSON—một loại dữ liệu có cấu trúc được sử dụng trong lập trình—bạn có thể fine-tune nó. Quá trình này cũng có thể giúp mô hình học các thông tin cụ thể về một lĩnh vực hoặc chủ đề nhất định. Tuy nhiên, nếu bạn muốn thêm kiến thức chuyên môn một cách nhanh chóng và hiệu quả hơn, Retrieval-Augmented Generation (RAG) thường là bước đầu tiên tốt hơn. Với RAG, bạn có nhiều quyền kiểm soát hơn đối với thông tin mà mô hình sử dụng để tạo phản hồi, giúp giai đoạn thử nghiệm nhanh hơn, minh bạch hơn và dễ quản lý hơn.

Các phần của bộ công cụ này sẽ được tích hợp một phần vào thế hệ foundation models tiếp theo, trong khi các phần sẽ được giải quyết thông qua các frameworks bổ sung như LlamaIndex và LangChain, đặc biệt là cho các RAG workflows. Tuy nhiên, các giải pháp tốt nhất sẽ cần điều chỉnh các công cụ này cho các ngành và ứng dụng cụ thể. Chúng tôi cũng tin rằng prompting, cùng với RAG, sẽ tồn tại lâu dài - theo thời gian, prompting sẽ giống như các kỹ năng cần thiết để giao tiếp và ủy quyền hiệu quả cho đồng nghiệp con người. Mặc dù nó sẽ tồn tại lâu dài, nhưng các libraries liên tục phát triển. Chúng tôi đã liên kết đến tài liệu của cả LlamaIndex và LangChain trên towardsai.net/book để có thông tin cập nhật nhất.

Tiềm năng của thế hệ AI models này vượt ra ngoài các nhiệm vụ xử lý ngôn ngữ tự nhiên (NLP) thông thường. Có vô số use cases, chẳng hạn như giải thích các algorithms phức tạp, xây dựng bots, hỗ trợ phát triển ứng dụng và giải thích các concepts học thuật. Các chương trình text-to-image như DALL-E, Stable Diffusion và Midjourney đang cách mạng hóa các lĩnh vực như hoạt hình, trò chơi, nghệ thuật, phim ảnh và kiến trúc. Ngoài ra, generative AI models đã thể hiện khả năng biến đổi trong phát triển phần mềm phức tạp với các công cụ như GitHub Copilot.

### The Current LLM Landscape

**Tình hình LLM hiện tại**

Những đột phá trong lĩnh vực Generative AI đã tạo ra một bối cảnh cực kỳ năng động và sôi động với nhiều bên tham gia. Điều này bao gồm: 
- 1) các nhà sản xuất phần cứng AI như Nvidia, 
- 2) các nền tảng đám mây AI như Azure, AWS và Google, 
- 3) các nền tảng mã nguồn mở để truy cập các mô hình đầy đủ, chẳng hạn như Hugging Face, 
- 4) truy cập vào các mô hình LLM thông qua API như OpenAI, Cohere và Anthropic, và 
- 5) truy cập vào LLM thông qua các sản phẩm tiêu dùng như ChatGPT, Perplexity và Bing.

Ngoài ra, nhiều đột phá khác đang diễn ra hàng tuần trong vũ trụ AI, chẳng hạn như việc phát hành các mô hình multimodal (có thể hiểu cả văn bản và hình ảnh), các kiến trúc mô hình mới (như Mixture of Experts), Agent Models (các mô hình có thể đặt nhiệm vụ và tương tác với nhau và các công cụ khác), v.v.


## Coding Environment and Packages

**Môi trường lập trình và các Packages**

Tất cả các code notebooks, Google Colabs, GitHub repos, research papers, documentation và các tài nguyên khác đều có thể truy cập tại towardsai.net/book.

Để theo dõi các phần coding của cuốn sách này, bạn cần đảm bảo rằng bạn đã chuẩn bị sẵn sàng môi trường lập trình phù hợp. Hãy đảm bảo sử dụng phiên bản Python bằng hoặc mới hơn 3.8.1. Bạn có thể thiết lập môi trường của mình bằng cách chọn một trong các tùy chọn sau:

* Có một code editor được cài đặt trên máy tính của bạn. Một môi trường lập trình phổ biến là Visual Studio Code, sử dụng Python virtual environments để quản lý các Python libraries.
* Sử dụng các Google Colab notebooks của chúng tôi.

### Run the code locally

Nếu bạn chọn tùy chọn đầu tiên, bạn sẽ cần các packages sau để thực thi thành công các sample codes trong mỗi phần. Bạn cũng sẽ cần một environment đã được thiết lập.

Python virtual environments cung cấp một giải pháp tuyệt vời để quản lý các Python libraries và tránh xung đột package. Chúng tạo ra các môi trường biệt lập để cài đặt packages, đảm bảo rằng các packages của bạn và các dependencies của chúng được chứa trong môi trường đó. Thiết lập này cung cấp các môi trường sạch và biệt lập cho các Python projects của bạn.

Thực thi lệnh python trong terminal của bạn để xác nhận rằng phiên bản Python bằng hoặc lớn hơn 3.8.1. Sau đó, hãy làm theo các bước sau để tạo một virtual environment:

1.  Tạo một virtual environment bằng lệnh: `python -m venv my_venv_name`
2.  Kích hoạt virtual environment: `source my_venv_name/bin/activate`
3.  Cài đặt các required libraries và chạy các code snippets từ các bài học trong virtual environment.

Chúng có thể được cài đặt bằng trình quản lý pip packages. Một liên kết đến tệp văn bản requirements này có thể truy cập tại towardsai.net/book.

```
deeplake==3.6.19
openai==0.27.8
tiktoken==0.4.0
transformers==4.32.0
torch==2.0.1
numpy==1.23.5
deepspeed==0.10.1
trl==0.7.1
peft==0.5.0
wandb==0.15.8
bitsandbytes==0.41.1
accelerate==0.22.0
tqdm==4.66.1
neural_compressor===2.2.1
onnx===1.14.1
pandas==2.0.3
scipy==1.11.2
```

Mặc dù chúng tôi đặc biệt khuyên bạn nên cài đặt các phiên bản mới nhất của các packages này, nhưng xin lưu ý rằng các mã đã được kiểm tra với các phiên bản được chỉ định trong dấu ngoặc đơn. Hơn nữa, các bài học cụ thể có thể yêu cầu cài đặt các packages bổ sung, sẽ được đề cập rõ ràng. Mã sau đây sẽ minh họa cách cài đặt một package bằng pip:

```
pip install deeplake
# Hoặc: (để cài đặt một phiên bản cụ thể)
# pip install deeplake==3.6.5
```

#### Google Colab

Google Colaboratory, thường được gọi là Google Colab, là một môi trường Jupyter notebook dựa trên đám mây miễn phí. Các Data scientists và engineers sử dụng rộng rãi nó để huấn luyện các mô hình machine learning và deep learning bằng CPU, GPU và TPU. Google Colab đi kèm với một loạt các tính năng, chẳng hạn như:

* Miễn phí truy cập vào GPU và TPU để huấn luyện mô hình được tăng tốc.
* Giao diện dựa trên web cho một dịch vụ chạy trên máy ảo, loại bỏ nhu cầu cài đặt phần mềm cục bộ.
* Tích hợp liền mạch với Google Drive và GitHub.

Bạn chỉ cần một tài khoản Google để sử dụng Google Colab. Bạn có thể chạy các terminal commands trực tiếp trong các notebook cells bằng cách thêm dấu chấm than (!) trước lệnh. Mọi notebook được tạo trong Google Colab đều được lưu trữ trong Google Drive của bạn để dễ dàng truy cập.

Một cách thuận tiện để sử dụng API keys trong Colab bao gồm:

1.  Lưu các API keys trong một tệp có tên .env trên Google Drive của bạn. Đây là cách tệp nên được định dạng để lưu Activeloop token và OpenAI API key:

    ```
    OPENAI_API_KEY=your_openai_key
    ```

2.  Mount Google Drive của bạn trên Colab instance.
3.  Load chúng làm environment variables bằng thư viện dotenv:

    ```python
    from dotenv import load_dotenv

    load_dotenv('/content/drive/MyDrive/path/to/.env')
    ```

## Learning Resources

Để hỗ trợ quá trình học tập của bạn, chúng tôi chia sẻ chatbot AI Tutor mã nguồn mở của mình (aitutor.towardsai.net) để hỗ trợ bạn khi cần thiết. Công cụ này được tạo ra bằng các công cụ chúng tôi dạy trong cuốn sách này. Chúng tôi xây dựng một hệ thống RAG (Retrieval-Augmented Generation) cung cấp cho LLM quyền truy cập vào tài liệu mới nhất từ tất cả các công cụ quan trọng, chẳng hạn như LangChain và LlamaIndex, bao gồm cả các khóa học miễn phí trước đây của chúng tôi. Nếu bạn có bất kỳ câu hỏi nào hoặc cần trợ giúp trong hành trình học AI của mình, cho dù là người mới bắt đầu hay chuyên gia trong lĩnh vực này, bạn có thể liên hệ với các thành viên cộng đồng của chúng tôi và các tác giả của cuốn sách này trong kênh (space) dành riêng cho cuốn sách này trong Cộng đồng Discord Learn AI Together của chúng tôi: discord.gg/learnaitogether.

## Chapter I: Introduction to LLMs

### What are Large Language Models

Đến thời điểm này, bạn có thể đã nghe nói về chúng. Large Language Models, thường được gọi là LLMs, là một loại neural network phức tạp. Các mô hình này đã khơi dậy nhiều đổi mới trong lĩnh vực xử lý ngôn ngữ tự nhiên (NLP) và được đặc trưng bởi số lượng lớn parameters, thường lên đến hàng tỷ, giúp chúng thành thạo trong việc xử lý và tạo văn bản. Chúng được huấn luyện trên dữ liệu văn bản rộng lớn, cho phép chúng nắm bắt các patterns và cấu trúc ngôn ngữ đa dạng. Mục tiêu chính của LLMs là diễn giải và tạo ra văn bản giống con người, nắm bắt được các sắc thái của ngôn ngữ tự nhiên, bao gồm syntax (cách sắp xếp từ) và semantics (ý nghĩa của từ).

Mục tiêu huấn luyện cốt lõi của LLMs tập trung vào việc dự đoán từ tiếp theo trong một câu. Mục tiêu đơn giản này dẫn đến sự phát triển của các khả năng mới nổi (emergent abilities). Ví dụ, chúng có thể thực hiện các phép tính số học, giải mã từ và thậm chí đã thể hiện sự thành thạo trong các kỳ thi chuyên nghiệp, chẳng hạn như vượt qua Kỳ thi Cấp phép Y tế Hoa Kỳ (US Medical Licensing Exam). Ngoài ra, các mô hình này đã đóng góp đáng kể vào nhiều nhiệm vụ NLP khác nhau, bao gồm machine translation, natural language generation, part-of-speech tagging, parsing, information retrieval và những nhiệm vụ khác, ngay cả khi không được huấn luyện trực tiếp hoặc fine-tuning trong các lĩnh vực cụ thể này.

Quá trình tạo văn bản trong Large Language Models là autoregressive, nghĩa là chúng tạo ra các tokens tiếp theo dựa trên chuỗi tokens đã được tạo ra. Attention mechanism là một thành phần quan trọng trong quá trình này; nó thiết lập các kết nối từ và đảm bảo văn bản mạch lạc và phù hợp với ngữ cảnh. Điều cần thiết là phải thiết lập các terminology và concepts cơ bản liên quan đến Large Language Models trước khi khám phá kiến trúc và các building blocks của nó (như attention mechanisms) một cách sâu sắc hơn. Hãy bắt đầu với tổng quan về kiến trúc cung cấp sức mạnh cho các mô hình này, tiếp theo là định nghĩa một vài terms, chẳng hạn như language modeling và tokenization.

### Key LLM Terminologies

**Transformer**

Nền tảng của một mô hình ngôn ngữ mạnh mẽ nằm ở kiến trúc của nó. Các Mạng Nơ-ron Tái phát (Recurrent Neural Networks - **RNNs**) thường được sử dụng cho xử lý văn bản do khả năng xử lý dữ liệu tuần tự. Chúng duy trì một trạng thái nội tại (internal state) lưu giữ thông tin từ các từ trước đó, tạo điều kiện cho sự hiểu biết tuần tự. Tuy nhiên, **RNNs** gặp phải những thách thức với các chuỗi dài, nơi chúng quên thông tin cũ để ưu tiên đầu vào được xử lý gần đây. Điều này chủ yếu là do vấn đề gradient biến mất (vanishing gradient problem), một hiện tượng mà các gradient, được sử dụng để cập nhật trọng số của mạng trong quá trình huấn luyện, trở nên nhỏ dần khi chúng được lan truyền ngược qua mỗi bước thời gian của chuỗi. Kết quả là, các trọng số liên quan đến đầu vào ban đầu thay đổi rất ít, cản trở khả năng học hỏi và ghi nhớ các phụ thuộc dài hạn trong dữ liệu của mạng.

Các mô hình dựa trên Transformer đã giải quyết những thách thức này và nổi lên như kiến trúc ưa thích cho các nhiệm vụ xử lý ngôn ngữ tự nhiên. Kiến trúc này, được giới thiệu trong bài báo có ảnh hưởng "Attention Is All You Need", là một đổi mới then chốt trong xử lý ngôn ngữ tự nhiên. Nó tạo thành nền tảng cho các mô hình tiên tiến như GPT-4, Claude và LLaMA. Kiến trúc này ban đầu được thiết kế như một khung encoder-decoder. Thiết lập này sử dụng một encoder để xử lý văn bản đầu vào, xác định các phần quan trọng và tạo ra một biểu diễn của đầu vào. Trong khi đó, decoder có khả năng biến đổi đầu ra của encoder, một vector có chiều cao, trở lại văn bản có thể đọc được cho con người. Các mạng này có thể hữu ích trong các nhiệm vụ như tóm tắt, nơi decoder tạo ra các bản tóm tắt có điều kiện dựa trên các bài báo được truyền cho encoder. Nó cung cấp sự linh hoạt bổ sung trên một loạt các nhiệm vụ vì các thành phần của kiến trúc này, encoder và decoder, có thể được sử dụng cùng nhau hoặc riêng biệt. Một số mô hình sử dụng phần encoder của mạng để biến đổi văn bản thành biểu diễn vector hoặc chỉ sử dụng khối decoder, là xương sống của các Mô hình Ngôn ngữ Lớn (Large Language Models - **LLMs**). Chương tiếp theo sẽ bao gồm từng thành phần này.

**Mô hình hóa Ngôn ngữ (Language Modeling)**

Với sự trỗi dậy của LLMs, mô hình hóa ngôn ngữ đã trở thành một phần thiết yếu của xử lý ngôn ngữ tự nhiên (natural language processing). Nó có nghĩa là học phân phối xác suất (probability distribution) của các từ trong một ngôn ngữ dựa trên một ngữ liệu lớn (large corpus). Quá trình học này thường liên quan đến việc dự đoán token tiếp theo trong một chuỗi bằng cách sử dụng các phương pháp thống kê cổ điển hoặc các kỹ thuật học sâu (deep learning) mới.

Các mô hình ngôn ngữ lớn được huấn luyện dựa trên cùng một mục tiêu là dự đoán từ, dấu chấm câu hoặc các thành phần khác tiếp theo dựa trên các token đã thấy trong một văn bản. Các mô hình này trở nên thành thạo bằng cách hiểu phân phối của các từ trong dữ liệu huấn luyện của chúng bằng cách đoán xác suất của từ tiếp theo dựa trên ngữ cảnh. Ví dụ: mô hình có thể hoàn thành một câu bắt đầu bằng "Tôi sống ở New" với một từ như "York" thay vì một từ không liên quan như "giày".

Trong thực tế, các mô hình làm việc với token, không phải từ hoàn chỉnh. Cách tiếp cận này cho phép dự đoán và tạo văn bản chính xác hơn bằng cách nắm bắt hiệu quả hơn sự phức tạp của ngôn ngữ con người.

**Tokenization (Phân tách Token)**

Tokenization là giai đoạn đầu tiên của việc tương tác với LLMs. Nó liên quan đến việc chia văn bản đầu vào thành các phần nhỏ hơn được gọi là token. Token có thể từ các ký tự đơn lẻ đến toàn bộ từ và kích thước của các token này có thể ảnh hưởng lớn đến hiệu suất của mô hình. Một số mô hình áp dụng subword tokenization, chia các từ thành các đoạn nhỏ hơn giữ lại các yếu tố ngôn ngữ có ý nghĩa.

Hãy xem xét câu sau: “The child’s coloring book.”

Nếu tokenization chia văn bản sau mỗi ký tự khoảng trắng. Kết quả sẽ là:

["The", "child's", “coloring”, "book."]

Trong cách tiếp cận này, bạn sẽ nhận thấy rằng dấu chấm câu vẫn được gắn vào các từ như “child’s” và “book.”

Ngoài ra, tokenization có thể được thực hiện bằng cách tách văn bản dựa trên cả khoảng trắng và dấu chấm câu; đầu ra sẽ là:

["The", "child", "'", "s", “coloring”, "book", "."]

Quá trình tokenization phụ thuộc vào mô hình. Điều quan trọng cần nhớ là các mô hình được phát hành dưới dạng một cặp pre-trained tokenizers và trọng số mô hình liên quan. Có những kỹ thuật tiên tiến hơn, như Byte-Pair encoding, được sử dụng bởi hầu hết các mô hình được phát hành gần đây. Như được minh họa trong ví dụ dưới đây, phương pháp này cũng chia một từ như “coloring” thành hai phần.

["The", "child", "'", "s", “color”, “ing”, "book", "."]

Subword tokenization tăng cường hơn nữa khả năng hiểu ngôn ngữ của mô hình bằng cách chia các từ thành các đoạn có ý nghĩa, như chia “coloring” thành “color” và “ing.” Điều này mở rộng vốn từ vựng của mô hình và cải thiện khả năng nắm bắt các sắc thái của cấu trúc và hình thái ngôn ngữ. Hiểu rằng phần “ing” của một từ cho biết thì hiện tại cho phép chúng ta đơn giản hóa cách chúng ta biểu diễn các từ ở các thì khác nhau. Chúng ta không còn cần giữ các mục riêng biệt cho dạng cơ bản của một từ, như “play,” và dạng thì hiện tại của nó, “playing.” Bằng cách kết hợp “play” với “ing,” chúng ta có thể diễn đạt “playing” mà không cần hai mục riêng biệt. Phương pháp này làm tăng số lượng token để biểu diễn một đoạn văn bản nhưng giảm đáng kể số lượng token chúng ta cần có trong từ điển.

Quá trình tokenization bao gồm việc quét toàn bộ văn bản để xác định các token duy nhất, sau đó được lập chỉ mục để tạo từ điển. Từ điển này gán một ID token duy nhất cho mỗi token, cho phép biểu diễn số hóa tiêu chuẩn của văn bản. Khi tương tác với các mô hình, việc chuyển đổi văn bản thành ID token này cho phép mô hình xử lý và hiểu đầu vào một cách hiệu quả, vì nó có thể nhanh chóng tham chiếu từ điển để giải mã ý nghĩa của mỗi token. Chúng ta sẽ thấy một ví dụ về quá trình này sau trong cuốn sách.

Sau khi có token, chúng ta có thể xử lý các hoạt động bên trong của transformers: embeddings.

**Embeddings (Nhúng)**

Bước tiếp theo sau tokenization là biến các token này thành thứ mà máy tính có thể hiểu và làm việc được — đó là lúc embeddings xuất hiện. Embeddings là một cách để dịch các token, là các từ hoặc các phần của từ, thành một ngôn ngữ số mà máy tính có thể nắm bắt. Chúng giúp mô hình hiểu các mối quan hệ và ngữ cảnh. Chúng cho phép mô hình nhìn thấy các kết nối giữa các từ và sử dụng các kết nối này để hiểu văn bản tốt hơn, chủ yếu thông qua quá trình attention, như chúng ta sẽ thấy.

Một embedding cung cấp cho mỗi token một ID số duy nhất nắm bắt ý nghĩa của nó. Dạng số này giúp máy tính thấy hai token giống nhau như thế nào, giống như biết rằng "happy" và "joyful" gần nhau về ý nghĩa, mặc dù chúng là những từ khác nhau.

Bước này rất cần thiết vì nó giúp mô hình hiểu ngôn ngữ theo cách số hóa, thu hẹp khoảng cách giữa ngôn ngữ con người và xử lý máy móc.

Ban đầu, mỗi token được gán một tập hợp số ngẫu nhiên làm embedding của nó. Khi mô hình được huấn luyện—nghĩa là khi nó đọc và học từ rất nhiều văn bản—nó điều chỉnh các số này. Mục tiêu là tinh chỉnh chúng sao cho các token có ý nghĩa tương tự kết thúc bằng các tập hợp số tương tự. Sự điều chỉnh này được thực hiện tự động bởi mô hình khi nó học từ các ngữ cảnh khác nhau mà các token xuất hiện.

Mặc dù khái niệm về các tập hợp số, hoặc vectors, có vẻ phức tạp, nhưng chúng chỉ là một cách để mô hình lưu trữ và xử lý thông tin về các token một cách hiệu quả. Chúng ta sử dụng vectors vì chúng là một phương pháp đơn giản để mô hình theo dõi các token liên quan đến nhau như thế nào. Về cơ bản, chúng chỉ là các danh sách số lớn.

Trong Chương 2, chúng ta sẽ khám phá thêm về cách các embeddings này được tạo và sử dụng trong kiến trúc transformer.

**Huấn luyện/Tinh chỉnh (Training/Fine-Tuning)**

LLMs được huấn luyện trên một ngữ liệu văn bản lớn (large corpus of text) với mục tiêu dự đoán chính xác token tiếp theo của một chuỗi. Như chúng ta đã học trong phần mô hình hóa ngôn ngữ (language modeling) trước đó, mục tiêu là điều chỉnh các tham số (parameters) của mô hình để tối đa hóa xác suất dự đoán chính xác dựa trên dữ liệu quan sát được. Thông thường, một mô hình được huấn luyện trên một tập dữ liệu mục đích chung (general-purpose dataset) khổng lồ gồm các văn bản từ Internet, chẳng hạn như The Pile hoặc CommonCrawl. Đôi khi, các tập dữ liệu cụ thể hơn, chẳng hạn như tập dữ liệu StackOverflow Posts, cũng là một ví dụ về việc thu thập kiến thức chuyên ngành (domain-specific knowledge). Giai đoạn này còn được gọi là giai đoạn tiền huấn luyện (pre-training stage), cho thấy rằng mô hình được huấn luyện để học khả năng hiểu ngôn ngữ và được chuẩn bị cho việc tinh chỉnh thêm.

Quá trình huấn luyện điều chỉnh trọng số (weights) của mô hình để tăng khả năng dự đoán token tiếp theo trong một chuỗi. Sự điều chỉnh này dựa trên dữ liệu huấn luyện, hướng dẫn mô hình đến các dự đoán token chính xác.

Sau khi tiền huấn luyện, mô hình thường trải qua quá trình tinh chỉnh (fine-tuning) cho một nhiệm vụ cụ thể. Giai đoạn này yêu cầu huấn luyện thêm trên một tập dữ liệu nhỏ hơn cho một nhiệm vụ (ví dụ: dịch văn bản) hoặc một lĩnh vực chuyên ngành (ví dụ: y sinh, tài chính, v.v.). Tinh chỉnh cho phép mô hình điều chỉnh kiến thức trước đó về nhiệm vụ hoặc lĩnh vực cụ thể, nâng cao hiệu suất của nó.

Quá trình tinh chỉnh có thể phức tạp, đặc biệt đối với các mô hình tiên tiến như GPT-4. Các mô hình này sử dụng các kỹ thuật tiên tiến và tận dụng khối lượng dữ liệu lớn để đạt được mức hiệu suất của chúng.

**Dự đoán (Prediction)**

Sau giai đoạn huấn luyện hoặc tinh chỉnh, mô hình có thể tạo ra văn bản bằng cách dự đoán các token tiếp theo trong một chuỗi. Điều này đạt được bằng cách đưa chuỗi vào mô hình, tạo ra một phân phối xác suất (probability distribution) trên các token tiếp theo tiềm năng, về cơ bản là gán điểm cho mọi từ trong từ vựng. Token tiếp theo được chọn theo điểm số của nó. Quá trình tạo sẽ được lặp lại trong một vòng lặp để dự đoán từng từ một, do đó có thể tạo ra các chuỗi có độ dài bất kỳ. Tuy nhiên, điều quan trọng là phải ghi nhớ kích thước ngữ cảnh hiệu quả (effective context size) của mô hình.

**Kích thước Ngữ cảnh (Context Size)**

Kích thước ngữ cảnh, hay cửa sổ ngữ cảnh (context window), là một khía cạnh quan trọng của LLMs. Nó đề cập đến số lượng token tối đa mà mô hình có thể xử lý trong một yêu cầu duy nhất. Kích thước ngữ cảnh ảnh hưởng đến độ dài văn bản mà mô hình có thể xử lý tại một thời điểm, ảnh hưởng trực tiếp đến hiệu suất của mô hình và kết quả mà nó tạo ra.

Các LLMs khác nhau được thiết kế với các kích thước ngữ cảnh khác nhau. Ví dụ, mô hình "gpt-3.5-turbo-16k" của OpenAI có cửa sổ ngữ cảnh có khả năng xử lý 16.000 token. Có một giới hạn vốn có đối với số lượng token mà một mô hình có thể tạo ra. Các mô hình nhỏ hơn có thể có dung lượng lên đến 1.000 token, trong khi các mô hình lớn hơn như GPT-4 có thể quản lý lên đến 32.000 token tại thời điểm chúng ta viết cuốn sách này.

**Quy luật Tỷ lệ (Scaling Laws)**

Quy luật tỷ lệ mô tả mối quan hệ giữa hiệu suất của mô hình ngôn ngữ và các yếu tố khác nhau, bao gồm số lượng tham số (parameters), kích thước tập dữ liệu huấn luyện (training dataset size), ngân sách tính toán (compute budget) và kiến trúc mạng (network architecture). Các quy luật này, được trình bày chi tiết trong bài báo Chinchilla, cung cấp những hiểu biết hữu ích về phân bổ tài nguyên để huấn luyện mô hình thành công. Chúng cũng là nguồn gốc của nhiều meme từ phía cộng đồng "scaling is all you need" trong lĩnh vực AI.

Các yếu tố sau đây xác định hiệu suất của mô hình ngôn ngữ:

* **Số lượng tham số (N):** Biểu thị khả năng học hỏi từ dữ liệu của mô hình. Số lượng tham số càng lớn, khả năng phát hiện các mẫu phức tạp trong dữ liệu càng cao.
* **Kích thước của Tập dữ liệu Huấn luyện (D):** Và số lượng token, từ các đoạn văn bản nhỏ đến các ký tự đơn lẻ, được tính.
* **FLOPs (Số phép tính dấu phẩy động mỗi giây):** Ước tính tài nguyên tính toán được sử dụng trong quá trình huấn luyện.

Trong nghiên cứu của mình, các tác giả đã huấn luyện mô hình Chinchilla, bao gồm 70 tỷ tham số, trên một tập dữ liệu gồm 1,4 nghìn tỷ token. Cách tiếp cận này phù hợp với quy luật tỷ lệ được đề xuất trong bài báo: đối với một mô hình có X tham số, việc huấn luyện tối ưu liên quan đến khoảng `X * 20` token. Ví dụ, một mô hình có 100 tỷ tham số lý tưởng sẽ được huấn luyện trên khoảng 2 nghìn tỷ token.

Với cách tiếp cận này, mặc dù có kích thước nhỏ hơn so với các LLMs khác, mô hình Chinchilla đã vượt trội hơn tất cả. Nó đã cải thiện mô hình hóa ngôn ngữ và hiệu suất cụ thể của nhiệm vụ bằng cách sử dụng ít bộ nhớ và sức mạnh tính toán hơn. Tìm bài báo "Training Compute-Optimal Large Language Models" tại towardsai.net/book.

**Khả năng Mới nổi trong LLMs (Emergent Abilities in LLMs)**

Khả năng mới nổi trong LLMs mô tả hiện tượng mà các kỹ năng mới xuất hiện bất ngờ khi kích thước mô hình tăng lên. Các khả năng này, bao gồm số học, trả lời câu hỏi, tóm tắt tài liệu và những khả năng khác, không được dạy rõ ràng cho mô hình trong suốt quá trình huấn luyện của nó. Thay vào đó, chúng xuất hiện một cách tự phát khi tỷ lệ của mô hình tăng lên, do đó có từ "mới nổi".

LLMs là các mô hình xác suất học các mẫu ngôn ngữ tự nhiên. Khi các mô hình này được mở rộng, khả năng nhận dạng mẫu của chúng được cải thiện về mặt định lượng đồng thời cũng thay đổi về mặt định tính.

Theo truyền thống, các mô hình yêu cầu tinh chỉnh cụ thể cho từng nhiệm vụ và điều chỉnh kiến trúc để thực hiện các nhiệm vụ cụ thể. Tuy nhiên, các mô hình được mở rộng có thể thực hiện các công việc này mà không cần thay đổi kiến trúc hoặc tinh chỉnh chuyên biệt. Chúng thực hiện điều này bằng cách diễn giải các nhiệm vụ bằng cách sử dụng xử lý ngôn ngữ tự nhiên. Khả năng thực hiện các chức năng khác nhau mà không cần tinh chỉnh rõ ràng của LLMs là một cột mốc quan trọng.

Điều đáng chú ý hơn là cách các khả năng này thể hiện bản thân. LLMs nhanh chóng và không thể đoán trước tiến triển từ gần bằng không đến đôi khi đạt hiệu suất tối ưu khi kích thước của chúng tăng lên. Hiện tượng này chỉ ra rằng các khả năng này phát sinh từ quy mô của mô hình chứ không phải được lập trình rõ ràng vào mô hình.

Sự tăng trưởng về kích thước mô hình và việc mở rộng tập dữ liệu huấn luyện, cùng với sự gia tăng đáng kể về chi phí tính toán, đã mở đường cho sự xuất hiện của các Mô hình Ngôn ngữ Lớn ngày nay. Ví dụ về các mô hình như vậy bao gồm Cohere Command, GPT-4 và LLaMA, mỗi mô hình đại diện cho những cột mốc quan trọng trong quá trình phát triển của mô hình hóa ngôn ngữ.

**Prompts (Lời nhắc)**

Văn bản (hoặc hình ảnh, số, bảng...) chúng ta cung cấp cho LLMs (Large Language Models - Mô hình ngôn ngữ lớn) như hướng dẫn thường được gọi là **prompts**. **Prompts** là các chỉ dẫn được đưa ra cho các hệ thống AI như GPT-3 và GPT-4 của OpenAI, cung cấp ngữ cảnh để tạo ra văn bản giống như con người—**prompt** càng chi tiết, đầu ra của mô hình càng tốt.

**Concise (ngắn gọn), descriptive (mô tả) và short (ngắn) prompts** (tùy thuộc vào nhiệm vụ) thường dẫn đến kết quả hiệu quả hơn, cho phép sự sáng tạo của LLM đồng thời hướng dẫn nó đến đầu ra mong muốn. Sử dụng các từ hoặc cụm từ cụ thể có thể giúp tập trung mô hình vào việc tạo ra nội dung liên quan. Việc tạo ra các **prompts** hiệu quả đòi hỏi mục đích rõ ràng, giữ mọi thứ đơn giản, sử dụng từ khóa một cách chiến lược và đảm bảo tính khả thi (**actionability**). Kiểm tra **prompts** trước khi sử dụng cuối cùng là rất quan trọng để đảm bảo đầu ra liên quan và không có lỗi. Dưới đây là một số mẹo về **prompting**:

* **Use Precise Language (Sử dụng ngôn ngữ chính xác):** Sự chính xác trong **prompt** của bạn có thể cải thiện đáng kể độ chính xác của đầu ra.
    * **Less Precise (Kém chính xác):** “Write about dog food.” (Viết về thức ăn cho chó.)
    * **More Precise (Chính xác hơn):** “Write a 500-word informative article about the dietary needs of adult Golden Retrievers.” (Viết một bài báo thông tin 500 từ về nhu cầu dinh dưỡng của chó Golden Retriever trưởng thành.)
* **Provide Sufficient Context (Cung cấp đủ ngữ cảnh):** Ngữ cảnh giúp mô hình hiểu đầu ra mong đợi:
    * **Less Contextual (Ít ngữ cảnh):** “Write a story.” (Viết một câu chuyện.)
    * **More Contextual (Nhiều ngữ cảnh hơn):** “Write a short story set in Victorian England featuring a young detective solving his first major case.” (Viết một truyện ngắn lấy bối cảnh nước Anh thời Victoria với một thám tử trẻ giải quyết vụ án lớn đầu tiên.)
* **Test Variations (Kiểm tra các biến thể):** Thử nghiệm với các kiểu **prompt** khác nhau để tìm ra cách tiếp cận hiệu quả nhất:
    * **Initial (Ban đầu):** “Write a blog post about the benefits of yoga.” (Viết một bài đăng trên blog về lợi ích của yoga.)
    * **Variation 1 (Biến thể 1):** “Compose a 1000-word blog post detailing the physical and mental benefits of regular yoga practice.” (Soạn một bài đăng trên blog dài 1000 từ chi tiết về lợi ích thể chất và tinh thần của việc tập yoga thường xuyên.)
    * **Variation 2 (Biến thể 2):** “Create an engaging blog post that highlights the top 10 benefits of incorporating yoga into a daily routine.” (Tạo một bài đăng trên blog hấp dẫn làm nổi bật 10 lợi ích hàng đầu của việc kết hợp yoga vào thói quen hàng ngày.)
* **Review Outputs (Xem xét đầu ra):** Luôn kiểm tra kỹ đầu ra tự động về độ chính xác và mức độ liên quan trước khi xuất bản.
    * **Before Review (Trước khi xem xét):** “Yoga is a great way to improve your flexibility and strength. It can also help reduce stress and improve mental clarity. However, it’s important to remember that all yoga poses are suitable for everyone.” (Yoga là một cách tuyệt vời để cải thiện sự linh hoạt và sức mạnh của bạn. Nó cũng có thể giúp giảm căng thẳng và cải thiện sự minh mẫn tinh thần. Tuy nhiên, điều quan trọng cần nhớ là không phải tất cả các tư thế yoga đều phù hợp với tất cả mọi người.)
    * **After Review (corrected) (Sau khi xem xét (đã sửa)):** “Yoga is a great way to improve your flexibility and strength. It can also help reduce stress and improve mental clarity. However, it’s important to remember that not all yoga poses are suitable for everyone. Always consult with a healthcare professional before starting any new exercise regimen.” (Yoga là một cách tuyệt vời để cải thiện sự linh hoạt và sức mạnh của bạn. Nó cũng có thể giúp giảm căng thẳng và cải thiện sự minh mẫn tinh thần. Tuy nhiên, điều quan trọng cần nhớ là không phải tất cả các tư thế yoga đều phù hợp với tất cả mọi người. Luôn tham khảo ý kiến của chuyên gia chăm sóc sức khỏe trước khi bắt đầu bất kỳ chế độ tập luyện mới nào.)

**Hallucinations (Ảo giác) và Biases (Thiên kiến) trong LLMs**

**Hallucinations** trong các hệ thống AI đề cập đến các trường hợp mà các hệ thống này tạo ra đầu ra, chẳng hạn như văn bản hoặc hình ảnh, không nhất quán với sự thật hoặc các đầu vào có sẵn. Một ví dụ là nếu ChatGPT cung cấp một câu trả lời thuyết phục nhưng sai sự thật cho một câu hỏi. Những **hallucinations** này cho thấy sự không khớp giữa đầu ra của AI và kiến thức hoặc ngữ cảnh thế giới thực.

Trong LLMs, **hallucinations** xảy ra khi mô hình tạo ra đầu ra không tương ứng với sự thật hoặc ngữ cảnh thế giới thực. Điều này có thể dẫn đến việc lan truyền thông tin sai lệch, đặc biệt là trong các ngành quan trọng như chăm sóc sức khỏe và giáo dục, nơi độ chính xác của thông tin là rất quan trọng. **Bias** trong LLMs cũng có thể dẫn đến kết quả ưu tiên các quan điểm cụ thể hơn những quan điểm khác, có khả năng củng cố các định kiến và phân biệt đối xử có hại.

Một ví dụ về **hallucination** có thể là nếu người dùng hỏi, "Ai đã vô địch World Series năm 2025?" và LLM trả lời với một người chiến thắng cụ thể. Tính đến ngày hiện tại (tháng 1 năm 2024), sự kiện này vẫn chưa diễn ra, khiến mọi phản hồi đều mang tính suy đoán và không chính xác.

Ngoài ra, **Bias** trong AI và LLMs là một vấn đề quan trọng khác. Nó đề cập đến xu hướng của các mô hình này trong việc ưu tiên các đầu ra hoặc quyết định cụ thể dựa trên dữ liệu huấn luyện của chúng. Nếu dữ liệu huấn luyện chủ yếu xuất phát từ một khu vực cụ thể, mô hình có thể bị thiên vị đối với ngôn ngữ, văn hóa hoặc quan điểm của khu vực đó. Trong trường hợp dữ liệu huấn luyện bao gồm các **biases**, chẳng hạn như giới tính hoặc chủng tộc, đầu ra kết quả từ hệ thống AI có thể bị thiên vị hoặc phân biệt đối xử.

Ví dụ, nếu người dùng hỏi một LLM, "Ai là y tá?" và nó trả lời, "Cô ấy là một chuyên gia chăm sóc sức khỏe, người chăm sóc bệnh nhân trong bệnh viện," điều này thể hiện một **gender bias** (thiên kiến giới tính). Mô hình này vốn liên kết nghề y tá với phụ nữ, điều này không phản ánh đầy đủ thực tế rằng cả nam và nữ đều có thể là y tá.

Việc giảm thiểu **hallucinations** và **bias** trong các hệ thống AI bao gồm việc tinh chỉnh quá trình huấn luyện mô hình, sử dụng các kỹ thuật xác minh và đảm bảo dữ liệu huấn luyện đa dạng và mang tính đại diện. Việc tìm kiếm sự cân bằng giữa việc tối đa hóa tiềm năng của mô hình và tránh những vấn đề này vẫn là một thách thức.

Đáng ngạc nhiên là, những " **hallucinations**" này có thể có lợi trong các lĩnh vực sáng tạo như viết tiểu thuyết, cho phép tạo ra nội dung mới và độc đáo. Mục tiêu cuối cùng là tạo ra các LLMs mạnh mẽ, hiệu quả nhưng cũng đáng tin cậy, công bằng và đáng tin cậy. Chúng ta có thể tối đa hóa tiềm năng của LLMs đồng thời giảm thiểu rủi ro của chúng, đảm bảo rằng lợi ích của công nghệ này có sẵn cho tất cả mọi người.

**Translation with LLMs (GPT-3.5 API) (Dịch thuật với LLMs (API GPT-3.5))**

Giờ đây, chúng ta có thể kết hợp tất cả những gì đã học để minh họa cách tương tác với LLM độc quyền của OpenAI thông qua API của họ, hướng dẫn mô hình thực hiện dịch thuật. Để tạo văn bản bằng LLMs như những LLMs được cung cấp bởi OpenAI, trước tiên bạn cần một **API key** cho môi trường Python của mình. Dưới đây là hướng dẫn từng bước để tạo **key** này:

1.  Tạo và đăng nhập vào tài khoản OpenAI của bạn.
2.  Sau khi đăng nhập, hãy chọn ‘Personal’ từ menu trên cùng bên phải và nhấp vào “View API keys”.
3.  Bạn sẽ tìm thấy nút “Create new secret key” trên trang **API keys**. Nhấp vào nút đó để tạo một **secret key** mới. Hãy nhớ lưu trữ **key** này một cách an toàn, vì nó sẽ được sử dụng sau này.
4.  Sau khi tạo **API key**, bạn có thể lưu trữ nó một cách an toàn trong tệp .env bằng định dạng sau:
    `OPENAI_API_KEY="<YOUR-OPENAI-API-KEY>"`
    Mỗi khi bạn khởi tạo một tập lệnh Python bao gồm các dòng sau, **API key** của bạn sẽ tự động được tải vào một biến môi trường có tên là `OPENAI_API_KEY`. Thư viện `openai` sau đó sử dụng biến này cho các tác vụ tạo văn bản. Tệp .env phải nằm trong cùng thư mục với tập lệnh Python.

```python
from dotenv import load_dotenv

load_dotenv()
```

Giờ đây, mô hình đã sẵn sàng để tương tác! Dưới đây là một ví dụ về việc sử dụng mô hình cho dịch thuật ngôn ngữ từ tiếng Anh sang tiếng Pháp. Đoạn mã bên dưới gửi **prompt** dưới dạng tin nhắn với vai trò người dùng, sử dụng gói Python OpenAI để gửi và truy xuất yêu cầu từ API. Bạn không cần lo lắng nếu bạn không hiểu tất cả các chi tiết, vì chúng ta sẽ sử dụng OpenAI API kỹ lưỡng hơn trong Chương 5. Tốt nhất bạn nên tập trung vào đối số `messages` ngay bây giờ, đối số này nhận **prompt** hướng dẫn mô hình thực hiện tác vụ dịch thuật.

```python
from dotenv import load_dotenv
load_dotenv()
import os
import openai

# English text to translate
english_text = "Hello, how are you?"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f'''Translate the following English text to French: "{english_text}"'''}
  ],
)

print(response['choices'][0]['message']['content'])
```

Đầu ra:

```
Bonjour, comment ça va?
```

💡 Bạn có thể lưu trữ an toàn thông tin nhạy cảm, chẳng hạn như **API keys**, trong một tệp riêng biệt với `dotenv` và tránh vô tình tiết lộ nó trong mã của bạn. Điều này đặc biệt quan trọng khi làm việc với các dự án mã nguồn mở hoặc chia sẻ mã của bạn với người khác, vì nó đảm bảo tính bảo mật của thông tin nhạy cảm.

**Kiểm soát đầu ra của LLMs bằng cách cung cấp các ví dụ**

**Few-shot learning**, một trong những khả năng mới nổi của **LLMs**, có nghĩa là cung cấp cho mô hình một số lượng nhỏ các ví dụ trước khi đưa ra dự đoán. Những ví dụ này phục vụ mục đích kép: chúng "dạy" mô hình trong quá trình suy luận và hoạt động như "bộ lọc", giúp mô hình xác định các mẫu liên quan trong tập dữ liệu của nó. **Few-shot learning** cho phép điều chỉnh mô hình cho các nhiệm vụ mới. Mặc dù **LLMs** như GPT-3 thể hiện sự thành thạo trong các nhiệm vụ mô hình hóa ngôn ngữ như dịch máy, hiệu suất của chúng có thể thay đổi đối với các nhiệm vụ đòi hỏi khả năng suy luận phức tạp hơn.

Trong **few-shot learning**, các ví dụ được trình bày cho mô hình giúp khám phá các mẫu liên quan trong tập dữ liệu. Các tập dữ liệu được mã hóa hiệu quả vào trọng số của mô hình trong quá trình đào tạo, vì vậy mô hình tìm kiếm các mẫu kết nối đáng kể với các mẫu được cung cấp và sử dụng chúng để tạo ra đầu ra của nó. Kết quả là, độ chính xác của mô hình được cải thiện bằng cách thêm nhiều ví dụ hơn, cho phép phản hồi có mục tiêu và phù hợp hơn.

Dưới đây là một ví dụ về **few-shot learning**, nơi chúng ta cung cấp các ví dụ thông qua các loại tin nhắn khác nhau về cách mô tả phim bằng biểu tượng cảm xúc cho mô hình. (Chúng ta sẽ đề cập đến các loại tin nhắn khác nhau sau trong cuốn sách.) Ví dụ: phim "Titanic" có thể được trình bày bằng cách sử dụng biểu tượng cảm xúc cho tàu du lịch, sóng, trái tim, v.v., hoặc cách biểu diễn phim "The Matrix". Mô hình nắm bắt các mẫu này và quản lý để mô tả chính xác bộ phim "Toy Story" bằng cách sử dụng biểu tượng cảm xúc của đồ chơi.

```python
from dotenv import load_dotenv
load_dotenv()
import os
import openai

# Prompt for summarization
prompt = """
Describe the following movie using emojis.

{movie}: """

examples = [
    { "input": "Titanic", "output": "🛳️🌊❤️🧊🎶🔥🚢💔👫💑" },
    { "input": "The Matrix", "output": "🕶️💊💥👾🔮🌃👨🏻‍💻🔁🔓💪" }
]

movie = "Toy Story"
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt.format(movie=examples[0]["input"])},
        {"role": "assistant", "content": examples[0]["output"]},
        {"role": "user", "content": prompt.format(movie=examples[1]["input"])},
        {"role": "assistant", "content": examples[1]["output"]},
        {"role": "user", "content": prompt.format(movie=movie)},
  ]
)

print(response['choices'][0]['message']['content'])
```

```
🧸🤠👦🧒🎢🌈🌟👫🚁👽🐶🚀
```

Thật thú vị khi mô hình, chỉ với hai ví dụ, có thể xác định một mẫu phức tạp, chẳng hạn như liên kết tiêu đề phim với một chuỗi biểu tượng cảm xúc. Khả năng này chỉ có thể đạt được với một mô hình có sự hiểu biết sâu sắc về câu chuyện của bộ phim và ý nghĩa của các biểu tượng cảm xúc, cho phép nó hợp nhất cả hai và trả lời các câu hỏi dựa trên cách giải thích của riêng mình.

### From Language Models to Large Language Models

Sự **evolution** (tiến hóa) của các **language models** (mô hình ngôn ngữ) đã chứng kiến một sự thay đổi mô hình từ các **pre-trained language models (LMs)** (mô hình ngôn ngữ được huấn luyện trước) đến việc tạo ra các **Large Language Models (LLMs)** (mô hình ngôn ngữ lớn). Các LMs, như ELMo và BERT, ban đầu nắm bắt các **context-aware word representations** (biểu diễn từ nhận biết ngữ cảnh) thông qua **pre-training** (huấn luyện trước) và **fine-tuning** (tinh chỉnh) cho các nhiệm vụ cụ thể. Tuy nhiên, sự ra đời của các LLMs, như được thể hiện bởi GPT-3 và PaLM, đã chứng minh rằng việc mở rộng quy mô mô hình và dữ liệu có thể mở khóa các kỹ năng mới nổi trội hơn so với các mô hình nhỏ hơn. Thông qua **in-context learning** (học trong ngữ cảnh), các LLMs này có thể xử lý các nhiệm vụ phức tạp hơn.

#### Emergent Abilities in LLMs

**Khả năng Xuất hiện (Emergent Abilities) trong LLMs**

Như chúng ta đã thảo luận, một khả năng được coi là *emergent* khi các mô hình lớn hơn thể hiện nó, nhưng nó lại vắng mặt ở các mô hình nhỏ hơn—một yếu tố quan trọng góp phần vào thành công của Large Language Models (LLMs). *Emergent abilities* trong Large Language Models (LLMs) là hiện tượng thực nghiệm xảy ra khi kích thước của các mô hình ngôn ngữ vượt quá các ngưỡng cụ thể. Khi chúng ta tăng kích thước của mô hình, *emergent abilities* trở nên rõ ràng hơn, bị ảnh hưởng bởi các khía cạnh như sức mạnh tính toán được sử dụng trong quá trình huấn luyện và các *parameters* của mô hình.

**Emergent Abilities là gì?**

Hiện tượng này chỉ ra rằng các mô hình đang học và tổng quát hóa vượt ra ngoài quá trình *pre-training* của chúng theo những cách không được lập trình hoặc dự đoán rõ ràng. Một mô hình riêng biệt xuất hiện khi những khả năng này được mô tả trên đường cong *scaling*. Ban đầu, hiệu suất của mô hình gần như ngẫu nhiên, nhưng nó cải thiện đáng kể khi đạt đến một ngưỡng quy mô nhất định. Hiện tượng này được gọi là *phase transition*, thể hiện sự thay đổi hành vi đáng kể mà không thể thấy rõ khi kiểm tra các hệ thống quy mô nhỏ hơn.

Việc *scaling* các mô hình ngôn ngữ chủ yếu tập trung vào việc tăng lượng tính toán, mở rộng các *model parameters* và tăng kích thước tập dữ liệu huấn luyện. Các khả năng mới đôi khi có thể xuất hiện với lượng tính toán huấn luyện giảm hoặc ít *model parameters* hơn, đặc biệt khi các mô hình được huấn luyện trên dữ liệu chất lượng cao hơn. Ngoài ra, sự xuất hiện của *emergent abilities* bị ảnh hưởng bởi các yếu tố như khối lượng và chất lượng của dữ liệu và số lượng *parameters* của mô hình. *Emergent abilities* trong Large Language Models xuất hiện khi các mô hình được *scaled up* và không thể dự đoán được bằng cách đơn thuần mở rộng các xu hướng quan sát được trong các mô hình nhỏ hơn.

**Các Benchmark Đánh giá Emergent Abilities**

Một số *benchmarks* được sử dụng để đánh giá *emergent abilities* của các mô hình ngôn ngữ, chẳng hạn như BIG-Bench, TruthfulQA, Massive Multi-task Language Understanding (MMLU) *benchmark* và Word in Context (WiC) *benchmark*. Các *benchmarks* chính bao gồm:

* **BIG-Bench suite:** bao gồm hơn 200 *benchmarks* kiểm tra một loạt các nhiệm vụ, chẳng hạn như các phép toán số học (ví dụ: "Q: 132 cộng 762 bằng bao nhiêu? A: 894"), chuyển tự từ Bảng chữ cái ngữ âm quốc tế (IPA) và giải mã từ. Những nhiệm vụ này đánh giá khả năng của mô hình trong việc thực hiện các phép tính, thao tác và sử dụng các từ hiếm và làm việc với bảng chữ cái. (ví dụ: "English: The 1931 Malay census was an alarm bell. IPA: ðə 1931 ˈmeɪleɪ ˈsɛnsəs wɑz ən əˈlɑrm bɛl."). Hiệu suất của các mô hình như GPT-3 và LaMDA trên các nhiệm vụ này thường bắt đầu gần bằng không nhưng cho thấy sự gia tăng đáng kể trên mức ngẫu nhiên ở một quy mô nhất định, cho thấy *emergent abilities*. Chi tiết hơn về các *benchmarks* này có thể được tìm thấy trong kho lưu trữ Github.
* **TruthfulQA benchmark:** đánh giá khả năng cung cấp câu trả lời trung thực của mô hình. Nó bao gồm hai nhiệm vụ: tạo câu trả lời, trong đó mô hình trả lời một câu hỏi trong một hoặc hai câu, và trắc nghiệm, trong đó mô hình chọn câu trả lời đúng từ bốn lựa chọn hoặc câu đúng/sai. Khi mô hình Gopher được *scaled* đến kích thước lớn nhất của nó, hiệu suất của nó cải thiện đáng kể, vượt quá kết quả ngẫu nhiên hơn 20%, điều này biểu thị sự xuất hiện của khả năng này.
* **Massive Multi-task Language Understanding (MMLU):** đánh giá kiến thức thế giới và kỹ năng giải quyết vấn đề của mô hình trên 57 nhiệm vụ đa dạng, bao gồm toán học cơ bản, lịch sử Hoa Kỳ và khoa học máy tính. Mặc dù các mô hình GPTs, Gopher và Chinchilla ở một quy mô nhất định không vượt trội hơn mức đoán ngẫu nhiên trung bình trên tất cả các chủ đề, nhưng một mô hình kích thước lớn hơn cho thấy hiệu suất được cải thiện, cho thấy sự xuất hiện của khả năng này.
* **The Word in Context (WiC) benchmark:** tập trung vào sự hiểu biết ngữ nghĩa và liên quan đến một nhiệm vụ phân loại nhị phân cho các *word embeddings* nhạy cảm theo ngữ cảnh. Nó yêu cầu xác định xem các từ mục tiêu (động từ hoặc danh từ) trong hai ngữ cảnh có cùng nghĩa hay không. Các mô hình như Chinchilla ban đầu không vượt qua hiệu suất ngẫu nhiên trong các nhiệm vụ *one-shot*, ngay cả ở quy mô lớn. Tuy nhiên, khi các mô hình như PaLM được *scaled* đến một kích thước lớn hơn nhiều, hiệu suất trên mức ngẫu nhiên xuất hiện, cho thấy sự xuất hiện của khả năng này ở quy mô lớn hơn.

**Các yếu tố dẫn đến Emergent Abilities**

* **Multi-step reasoning:** liên quan đến việc hướng dẫn mô hình thực hiện một loạt các bước trung gian trước khi đưa ra kết quả cuối cùng. Phương pháp này, được gọi là *chain-of-thought prompting*, chỉ trở nên hiệu quả hơn *standard prompting* khi được áp dụng cho các mô hình đủ lớn.
* Một chiến lược khác là *fine-tuning* một mô hình trên nhiều nhiệm vụ được trình bày dưới dạng *Instruction Following*. Phương pháp này cho thấy hiệu suất được cải thiện chỉ với các mô hình có kích thước nhất định, nhấn mạnh tầm quan trọng của quy mô trong việc đạt được các khả năng tiên tiến.

**Rủi ro với Emergent Abilities**

Khi các mô hình ngôn ngữ được *scaled up*, các rủi ro *emergent* cũng trở thành mối quan tâm. Chúng bao gồm các thách thức xã hội liên quan đến độ chính xác, thiên vị và độc hại. Việc áp dụng các chiến lược khuyến khích các mô hình "hữu ích, vô hại và trung thực" có thể giảm thiểu những rủi ro này.

Ví dụ, *benchmark* WinoGender, đánh giá sự thiên vị giới tính trong bối cảnh nghề nghiệp, đã chỉ ra rằng mặc dù *scaling* có thể nâng cao hiệu suất của mô hình, nhưng nó cũng có thể khuếch đại sự thiên vị, đặc biệt là trong các tình huống mơ hồ. Các mô hình lớn hơn có xu hướng ghi nhớ dữ liệu huấn luyện nhiều hơn, nhưng các phương pháp như *deduplication* có thể giảm thiểu rủi ro này.

Các rủi ro khác liên quan đến các lỗ hổng tiềm ẩn hoặc tổng hợp nội dung có hại có thể phổ biến hơn trong các mô hình ngôn ngữ trong tương lai hoặc vẫn chưa được mô tả trong các mô hình hiện tại.

**Sự thay đổi hướng tới các mô hình mục đích chung (General-Purpose Models)**

Sự xuất hiện của các khả năng mới đã thay đổi quan điểm và việc sử dụng các mô hình này của cộng đồng NLP. Trong khi NLP truyền thống tập trung vào các mô hình dành riêng cho từng nhiệm vụ, việc *scaling* các mô hình đã thúc đẩy nghiên cứu về các mô hình "mục đích chung" có khả năng xử lý một loạt các nhiệm vụ không được đưa vào huấn luyện một cách rõ ràng.

Sự thay đổi này thể hiện rõ trong các trường hợp mà các mô hình mục đích chung được *scaled*, *few-shot prompted* đã vượt trội hơn các mô hình dành riêng cho từng nhiệm vụ được *fine-tuned*. Ví dụ bao gồm GPT-3 thiết lập các *benchmarks* mới trong TriviaQA và PiQA, PaLM xuất sắc trong suy luận số học và mô hình đa phương thức Flamingo đạt hiệu suất hàng đầu trong trả lời câu hỏi hình ảnh. Hơn nữa, khả năng thực hiện các nhiệm vụ của các mô hình mục đích chung với số lượng ví dụ tối thiểu đã mở rộng ứng dụng của chúng vượt ra ngoài nghiên cứu NLP truyền thống. Chúng bao gồm dịch hướng dẫn ngôn ngữ tự nhiên để thực hiện robot, tương tác người dùng và suy luận đa phương thức.

#### Expanding the Context Window

**Tầm quan trọng của Độ dài Ngữ cảnh (Context Length)**

*Context window* trong các mô hình ngôn ngữ đại diện cho số lượng *input tokens* mà mô hình có thể xử lý đồng thời. Trong các mô hình như GPT-4, hiện tại nó ở mức khoảng 32K hoặc khoảng 50 trang văn bản. Tuy nhiên, những tiến bộ gần đây đã mở rộng con số này lên đến 100K *tokens* ấn tượng hoặc khoảng 156 trang, như được thấy trong Claude của Anthropic.

*Context length* chủ yếu cho phép mô hình xử lý và hiểu các tập dữ liệu lớn hơn đồng thời, mang lại sự hiểu biết sâu sắc hơn về ngữ cảnh. Tính năng này đặc biệt có lợi khi nhập một lượng lớn dữ liệu cụ thể vào mô hình ngôn ngữ và đặt câu hỏi liên quan đến dữ liệu này. Ví dụ: khi phân tích một tài liệu dài về một công ty hoặc vấn đề cụ thể, *context window* lớn hơn cho phép mô hình ngôn ngữ xem xét và ghi nhớ nhiều thông tin độc đáo này hơn, dẫn đến các phản hồi chính xác và phù hợp hơn.

**Hạn chế của Kiến trúc Transformer Gốc**

Mặc dù có những điểm mạnh, kiến trúc *transformer* gốc phải đối mặt với những thách thức trong việc xử lý độ dài ngữ cảnh rộng lớn. Cụ thể, các hoạt động của lớp *attention* trong *transformer* có độ phức tạp thời gian và không gian bậc hai (biểu thị bằng ) liên quan đến số lượng *input tokens*, . Khi *context length* mở rộng, tài nguyên tính toán cần thiết cho quá trình huấn luyện và suy luận tăng lên đáng kể.

Để hiểu rõ hơn điều này, hãy xem xét độ phức tạp tính toán của kiến trúc *transformer*. Độ phức tạp của lớp *attention* trong mô hình *transformer* là , trong đó là *context length* (số lượng *input tokens*) và là kích thước nhúng (embedding size).

Độ phức tạp này xuất phát từ hai hoạt động chính trong lớp *attention*: phép chiếu tuyến tính để tạo ma trận Query, Key và Value (độ phức tạp ~ ) và phép nhân các ma trận này (độ phức tạp ~ ). Khi *context length* hoặc *embedding size* tăng lên, độ phức tạp tính toán cũng tăng lên theo bậc hai, gây ra thách thức cho việc xử lý *context lengths* lớn hơn.

**Các Kỹ thuật Tối ưu hóa để Mở rộng Context Window**

Bất chấp những thách thức tính toán liên quan đến kiến trúc *transformer* gốc, các nhà nghiên cứu đã phát triển một loạt các kỹ thuật tối ưu hóa để nâng cao hiệu quả của *transformer* và tăng khả năng *context length* lên 100K *tokens*:

* **ALiBi Positional Encoding:** *transformer* gốc sử dụng *Positional Sinusoidal Encoding*, gặp khó khăn trong việc suy luận *context lengths* lớn hơn. Mặt khác, ALiBi (Attention with Linear Biases) là một giải pháp có khả năng mở rộng tốt hơn. Kỹ thuật mã hóa vị trí này cho phép mô hình được huấn luyện trong các ngữ cảnh nhỏ hơn và sau đó được *fine-tuned* trong các ngữ cảnh lớn hơn, giúp nó thích ứng tốt hơn với các kích thước ngữ cảnh khác nhau.
* **Sparse Attention:** *Sparse Attention* giải quyết thách thức tính toán bằng cách tập trung điểm *attention* vào một tập hợp con của *tokens*. Phương pháp này giảm đáng kể độ phức tạp tính toán xuống thang tuyến tính theo số lượng *tokens* n, dẫn đến việc giảm đáng kể nhu cầu tính toán tổng thể.
* **FlashAttention:** *FlashAttention* tái cấu trúc tính toán lớp *attention* để tối ưu hóa hiệu quả GPU. Nó chia ma trận đầu vào thành các khối và sau đó xử lý đầu ra *attention* liên quan đến các khối này, tối ưu hóa việc sử dụng bộ nhớ GPU và tăng hiệu quả xử lý.
* **Multi-Query Attention (MQA):** MQA giảm mức tiêu thụ bộ nhớ trong bộ đệm giải mã *key/value* bằng cách tổng hợp trọng số trên tất cả các đầu *attention* trong quá trình chiếu tuyến tính của ma trận Key và Value. Sự hợp nhất này dẫn đến việc sử dụng bộ nhớ hiệu quả hơn.


#### FlashAttention-2

**FlashAttention-2** nổi lên như một bước tiến so với FlashAttention ban đầu, tập trung vào việc tối ưu hóa tốc độ và hiệu quả bộ nhớ của lớp *attention* trong các mô hình *transformer*. Phiên bản nâng cấp này được phát triển lại từ đầu bằng cách sử dụng các nguyên thủy mới của Nvidia. Nó thực hiện nhanh hơn khoảng 2 lần so với phiên bản tiền nhiệm, đạt tới 230 TFLOPs trên GPU A100.

FlashAttention-2 cải thiện FlashAttention ban đầu theo nhiều cách:

* Thay đổi thuật toán để dành nhiều thời gian hơn cho *matmul FLOPs* nhằm giảm thiểu số lượng *non-matmul FLOPs*, vốn đắt hơn *matmul FLOPs* 16 lần.
* Tối ưu hóa tính song song trên các kích thước *batch size*, *headcount* và *sequence length*, dẫn đến sự tăng tốc đáng kể, đặc biệt đối với các chuỗi dài.
* Nâng cao việc phân vùng tác vụ trong mỗi khối luồng để giảm sự đồng bộ hóa và giao tiếp giữa các *warps*, dẫn đến ít lần đọc/ghi bộ nhớ dùng chung hơn.
* Thêm các tính năng như hỗ trợ kích thước đầu *attention* lên đến 256 và *multi-query attention (MQA)*, tiếp tục mở rộng *context window*.

Với những cải tiến này, FlashAttention-2 là một bước thành công hướng tới việc mở rộng *context window* (trong khi vẫn giữ lại các hạn chế cơ bản của kiến trúc *transformer* gốc).


#### LongNet: A Leap Towards Billion-Token Context Window

**LongNet: Mở Rộng Context Window Lên 1 Tỷ Tokens**

LongNet đại diện cho một bước tiến mang tính chuyển đổi trong lĩnh vực tối ưu hóa *transformer*, như được trình bày chi tiết trong bài báo "LONGNET: Scaling Transformers to 1,000,000,000 Tokens". Phương pháp sáng tạo này được thiết lập để mở rộng *context window* của các mô hình ngôn ngữ lên đến 1 tỷ *tokens* chưa từng có, tăng cường đáng kể khả năng xử lý và phân tích khối lượng dữ liệu lớn của chúng.

**Dilated Attention: Cơ Chế Attention Đột Phá**

Tiến bộ chính trong LongNet là việc triển khai "dilated attention" (attention giãn nở). Cơ chế *attention* sáng tạo này cho phép tăng trưởng theo cấp số nhân của trường *attention* khi khoảng cách giữa các *tokens* rộng hơn, đồng thời giảm tính toán *attention* khi khoảng cách giữa các *tokens* tăng lên (vì mỗi *token* sẽ chú ý đến một số lượng *tokens* nhỏ hơn). Cách tiếp cận thiết kế này cân bằng tài nguyên *attention* hạn chế và nhu cầu truy cập mọi *token* trong chuỗi.

**Độ Phức Tạp Tuyến Tính: Cải Tiến So Với Transformer Truyền Thống**

Cơ chế *dilated attention* của LongNet có độ phức tạp tính toán tuyến tính, một cải tiến lớn so với độ phức tạp bậc hai của *transformer* thông thường. Điều này đồng nghĩa với việc LongNet có thể xử lý các chuỗi dữ liệu cực dài một cách hiệu quả hơn nhiều so với các mô hình *transformer* truyền thống.

**Tóm Tắt Các Điểm Chính:**

* **Mở rộng Context Window:** LongNet có khả năng xử lý *context window* lên đến 1 tỷ *tokens*, mở ra khả năng xử lý dữ liệu cực lớn.
* **Dilated Attention:** Cơ chế *attention* giãn nở giúp cân bằng hiệu quả giữa việc truy cập toàn bộ chuỗi và giảm tải tính toán.
* **Độ Phức Tạp Tuyến Tính:** Cải thiện đáng kể hiệu quả tính toán so với *transformer* truyền thống, cho phép xử lý chuỗi dữ liệu dài hơn.

LongNet đánh dấu một bước tiến quan trọng trong việc xử lý dữ liệu chuỗi dài, mở ra những khả năng mới cho các ứng dụng như phân tích văn bản dài, xử lý dữ liệu gen và nhiều lĩnh vực khác.


#### A Timeline of the Most Popular LLMs

Dưới đây là dòng thời gian của một số LLMs phổ biến nhất trong 5 năm qua:

**2018:**

* **GPT-1 (OpenAI):** Đặt nền móng cho dòng GPT với kiến trúc *transformer* chỉ giải mã, tạo sinh. Tiên phong kết hợp *unsupervised pretraining* và *supervised fine-tuning* cho dự đoán văn bản ngôn ngữ tự nhiên.

**2019:**

* **GPT-2 (OpenAI):** Mở rộng kích thước mô hình lên 1.5 tỷ *parameters*, thể hiện tính linh hoạt của mô hình trên nhiều nhiệm vụ bằng cách sử dụng định dạng thống nhất cho đầu vào, đầu ra và thông tin nhiệm vụ.

**2020:**

* **GPT-3 (OpenAI):** Bước nhảy vọt với 175 tỷ *parameters*, giới thiệu *in-context learning (ICL)*. Thể hiện hiệu suất vượt trội trong các nhiệm vụ NLP khác nhau, bao gồm lập luận và thích ứng miền, làm nổi bật tiềm năng của việc mở rộng quy mô mô hình.

**2021:**

* **Codex (OpenAI):** Biến thể GPT-3 được *fine-tuned* trên tập dữ liệu mã GitHub, thể hiện khả năng lập trình và giải quyết vấn đề toán học nâng cao.
* **LaMDA (DeepMind):** Tập trung vào các ứng dụng hội thoại, với 137 tỷ *parameters*. Nhằm mục đích nâng cao tạo sinh hội thoại và AI đàm thoại.
* **Gopher (DeepMind):** Với 280 tỷ *parameters*, đạt hiệu suất gần bằng con người trên *benchmark* MMLU nhưng đối mặt với những thách thức như thiên vị và thông tin sai lệch.

**2022:**

* **InstructGPT (OpenAI):** Cải tiến GPT-3, sử dụng *reinforcement learning from human feedback* để cải thiện tuân theo hướng dẫn và an toàn nội dung.
* **Chinchilla (DeepMind):** Với 70 tỷ *parameters*, tối ưu hóa việc sử dụng tài nguyên tính toán dựa trên *scaling laws*, đạt được những cải thiện đáng kể về độ chính xác trên các *benchmark*.
* **PaLM (Google Research):** Với 540 tỷ *parameters*, thể hiện hiệu suất *few-shot* vượt trội, hưởng lợi từ hệ thống Pathways của Google cho tính toán phân tán.
* **ChatGPT (OpenAI):** Dựa trên GPT-3.5 và GPT-4, được thiết kế riêng cho AI đàm thoại và thể hiện khả năng giao tiếp và lập luận giống con người.

**2023:**

* **LLaMA (Meta AI):** Giới thiệu một họ các mô hình ngôn ngữ lớn với *parameters* từ 7 tỷ đến 65 tỷ. Phá vỡ truyền thống truy cập hạn chế bằng cách cung cấp trọng số mô hình cho cộng đồng khoa học theo giấy phép phi thương mại.
* **GPT-4 (OpenAI):** Mở rộng khả năng sang đầu vào đa phương thức, vượt trội so với các phiên bản tiền nhiệm trong các nhiệm vụ khác nhau.

**2024:**

* **Gemini 1.5 (Google):** Nâng cấp đáng kể với kiến trúc Mixture-of-Experts mới và khả năng đa phương thức (Gemini 1.5 Pro), hỗ trợ hiểu biết ngữ cảnh dài và *context window* lên đến 1 triệu *tokens*.
* **Gemma (Google):** Hai phiên bản với 2 tỷ và 7 tỷ *parameters*, được phát triển trong giai đoạn huấn luyện Gemini và hiện có thể truy cập công khai.
* **Claude 3 Opus (Anthropic):** Đạt điểm số tương đương hoặc vượt GPT-4 trên các *benchmark* khác nhau. Với *context window* 200K *tokens*, được quảng cáo về khả năng ghi nhớ vượt trội.
* **Mistral:** Mô hình *open-source* tốt nhất hiện có thể truy cập để sử dụng, dựa trên kiến trúc Mixture of Experts.
* **Infinite Attention (Google):** Nghiên cứu khám phá các kỹ thuật có thể mở rộng vô hạn kích thước *context window* của mô hình.

Để tìm hiểu sâu hơn về các mô hình này, bạn nên đọc bài báo "A Survey of Large Language Models".

### History of NLP/LLMs

Đây là hành trình xuyên suốt sự phát triển của các mô hình ngôn ngữ (language modeling models), từ những mô hình thống kê ban đầu đến sự ra đời của các Mô hình Ngôn ngữ Lớn (Large Language Models - LLMs) đầu tiên. Thay vì một nghiên cứu kỹ thuật chuyên sâu, chương này trình bày một khám phá theo kiểu câu chuyện về việc xây dựng mô hình. Đừng lo lắng nếu một số chi tiết cụ thể của mô hình có vẻ phức tạp.

**Sự Tiến Hóa của Mô Hình Ngôn Ngữ (The Evolution of Language Modeling)**

Sự tiến hóa của các mô hình xử lý ngôn ngữ tự nhiên (natural language processing - NLP) là một câu chuyện về sự phát minh và cải tiến không ngừng. Mô hình "Túi Từ" (Bag of Words - BOW), một phương pháp đơn giản để đếm số lần xuất hiện của từ trong tài liệu, bắt đầu vào năm 1954. Sau đó, vào năm 1972, TF-IDF xuất hiện, cải tiến chiến lược này bằng cách điều chỉnh số lượng từ dựa trên độ hiếm hoặc tần suất. Sự ra đời của Word2Vec vào năm 2013 đánh dấu một bước đột phá quan trọng. Mô hình này sử dụng "nhúng từ" (word embeddings) để nắm bắt các liên kết ngữ nghĩa tinh tế giữa các từ mà các mô hình trước đó không thể.

Tiếp theo đó, Mạng Nơ-ron Tái Phát (Recurrent Neural Networks - RNNs) được giới thiệu. RNNs có khả năng học các mẫu trong chuỗi, cho phép chúng xử lý hiệu quả các tài liệu có độ dài khác nhau.

Sự ra mắt của kiến trúc Transformer vào năm 2017 đánh dấu một sự thay đổi mô hình trong lĩnh vực này. Cơ chế "chú ý" (attention mechanism) của mô hình cho phép nó tập trung vào các phần tử liên quan nhất của đầu vào một cách chọn lọc trong quá trình tạo đầu ra. Bước đột phá này đã mở đường cho BERT vào năm 2018. BERT sử dụng Transformer hai chiều (bidirectional transformer), tăng đáng kể hiệu suất trong nhiều công việc NLP truyền thống.

Những năm tiếp theo chứng kiến sự gia tăng trong sự phát triển của mô hình. Mỗi mô hình mới, chẳng hạn như RoBERTa, XLM, ALBERT và ELECTRA, đều giới thiệu các cải tiến và tối ưu hóa bổ sung, đẩy mạnh giới hạn của những gì có thể thực hiện được trong NLP.

**Dòng Thời Gian của Mô Hình (Model’s Timeline)**

* [1954] Túi Từ (Bag of Words - BOW):
    * Mô hình "Túi Từ" là một phương pháp cơ bản đếm số lần xuất hiện của từ trong bản thảo. Mặc dù đơn giản, nó không thể xem xét thứ tự hoặc ngữ cảnh của từ.
* [1972] TF-IDF:
    * TF-IDF mở rộng trên BOW bằng cách tăng trọng lượng cho các từ hiếm và giảm trọng lượng cho các thuật ngữ phổ biến, cải thiện khả năng của mô hình trong việc phát hiện mức độ liên quan của tài liệu. Tuy nhiên, nó không đề cập đến ngữ cảnh từ.
* [2013] Word2Vec:
    * "Nhúng từ" (word embeddings) là các vectơ đa chiều gói gọn các liên kết ngữ nghĩa, như được mô tả bởi Word2Vec. Đây là một bước tiến đáng kể trong việc nắm bắt ngữ nghĩa văn bản.
* [2014] RNNs trong kiến trúc Encoder-Decoder:
    * RNNs là một bước tiến quan trọng, có khả năng tính toán "nhúng tài liệu" (document embeddings) và thêm ngữ cảnh từ. Chúng phát triển bao gồm LSTM (1997) cho các phụ thuộc dài hạn và RNN hai chiều (Bidirectional RNN) (1997) để hiểu ngữ cảnh. Encoder-Decoder RNNs (2014) cải thiện phương pháp này.
* [2017] Transformer:
    * Transformer, với cơ chế "chú ý" (attention mechanisms), đã cải thiện đáng kể việc tính toán "nhúng" (embedding computation) và sự căn chỉnh giữa đầu vào và đầu ra, cách mạng hóa các tác vụ NLP.
* [2018] BERT:
    * BERT, một Transformer hai chiều (bidirectional transformer), đạt được kết quả NLP ấn tượng bằng cách sử dụng "chú ý toàn cục" (global attention) và kết hợp các mục tiêu đào tạo.
* [2018] GPT:
    * Kiến trúc Transformer đã được sử dụng để tạo ra mô hình tự hồi quy (autoregressive model) đầu tiên, GPT. Sau đó, nó phát triển thành GPT-2 [2019], một phiên bản lớn hơn và được tối ưu hóa hơn của GPT được đào tạo trước trên WebText, và GPT-3 [2020], một phiên bản lớn hơn và được tối ưu hóa hơn của GPT-2 được đào tạo trước trên Common Crawl.
* [2019] CTRL:
    * CTRL, tương tự như GPT, giới thiệu các mã điều khiển cho phép tạo văn bản có điều kiện. Tính năng này tăng cường khả năng kiểm soát nội dung và phong cách của văn bản được tạo ra.
* [2019] Transformer-XL:
    * Transformer-XL đổi mới bằng cách tái sử dụng các trạng thái ẩn (hidden states) đã được tính toán trước đó, cho phép mô hình duy trì bộ nhớ ngữ cảnh dài hơn. Sự cải tiến này cải thiện đáng kể khả năng của mô hình trong việc xử lý các chuỗi văn bản mở rộng.
* [2019] ALBERT:
    * ALBERT cung cấp một phiên bản hiệu quả hơn của BERT bằng cách triển khai Dự đoán Thứ tự Câu (Sentence Order Prediction) thay vì Dự đoán Câu Tiếp theo (Next Sentence Prediction) và sử dụng các kỹ thuật giảm tham số. Những thay đổi này dẫn đến việc sử dụng bộ nhớ thấp hơn và đào tạo nhanh hơn.
* [2019] RoBERTa:
    * RoBERTa cải thiện BERT bằng cách giới thiệu Mô hình Ngôn ngữ Mặt nạ Động (dynamic Masked Language Modeling), bỏ qua Dự đoán Câu Tiếp theo (Next Sentence Prediction), sử dụng bộ mã hóa BPE (BPE tokenizer) và sử dụng các siêu tham số tốt hơn để tăng cường hiệu suất.
* [2019] XLM:
    * XLM là một Transformer đa ngôn ngữ, được đào tạo trước bằng nhiều mục tiêu khác nhau, bao gồm Mô hình Ngôn ngữ Nhân quả (Causal Language Modeling), Mô hình Ngôn ngữ Mặt nạ (Masked Language Modeling) và Mô hình Ngôn ngữ Dịch (Translation Language Modeling), phục vụ cho các tác vụ NLP đa ngôn ngữ.
* [2019] XLNet:
    * XLNet kết hợp các điểm mạnh của Transformer-XL với phương pháp đào tạo trước tự hồi quy tổng quát, cho phép học các phụ thuộc hai chiều và cung cấp hiệu suất được cải thiện so với các mô hình đơn hướng truyền thống.
* [2019] PEGASUS:
    * PEGASUS có bộ mã hóa hai chiều và bộ giải mã từ trái sang phải, được đào tạo trước bằng các mục tiêu như Mô hình Ngôn ngữ Mặt nạ (Masked Language Modeling) và Tạo Câu Khoảng trống (Gap Sentence Generation), tối ưu hóa nó cho các tác vụ tóm tắt.
* [2019] DistilBERT:
    * DistilBERT giới thiệu một phiên bản nhỏ hơn, nhanh hơn của BERT, giữ lại hơn 95% hiệu suất của nó. Mô hình này được đào tạo bằng các kỹ thuật chưng cất để nén mô hình BERT được đào tạo trước.
* [2019] XLM-RoBERTa:
    * XLM-RoBERTa là một bản chuyển thể đa ngôn ngữ của RoBERTa, được đào tạo trên một tập hợp đa ngôn ngữ đa dạng, chủ yếu sử dụng mục tiêu Mô hình Ngôn ngữ Mặt nạ (Masked Language Modeling), tăng cường khả năng đa ngôn ngữ của nó.
* [2019] BART:
    * BART, với bộ mã hóa hai chiều và bộ giải mã từ trái sang phải, được đào tạo bằng cách cố ý làm hỏng văn bản và sau đó học cách xây dựng lại bản gốc, làm cho nó thực tế cho một loạt các tác vụ tạo và hiểu.
* [2019] ConvBERT:
    * ConvBERT đổi mới bằng cách thay thế các khối tự chú ý truyền thống bằng các mô-đun kết hợp tích chập, cho phép xử lý hiệu quả hơn các ngữ cảnh toàn cục và cục bộ trong văn bản.
* [2020] Funnel Transformer:
    * Funnel Transformer đổi mới bằng cách nén dần chuỗi trạng thái ẩn thành một chuỗi ngắn hơn, giảm chi phí tính toán một cách hiệu quả trong khi vẫn duy trì hiệu suất.
* [2020] Reformer:
    * Reformer cung cấp một phiên bản hiệu quả hơn của Transformer. Nó sử dụng băm nhạy cảm cục


## Chapter II: LLM Architectures and Landscape