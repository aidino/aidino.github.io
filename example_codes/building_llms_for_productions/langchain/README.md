## Setup Environment

**OpenAI**

```python
# Setup environment
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True, dotenv_path="../.env")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
prompt = PromptTemplate.from_template("Liệt kê 5 món ăn ngon ở {place}")
chain = prompt | llm | StrOutputParser()

answer = chain.invoke("Hà Nội")
print(answer)
```

**Local ``VLLM``**

- Install `vllm`: https://docs.vllm.ai/en/latest/getting_started/installation/index.html

- Run `OpenAI-Compatible Server`

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct --dtype auto --api-key token-abc123
```

```python
from langchain_community.llms import VLLMOpenAI

llm = VLLMOpenAI(
    model="Qwen/Qwen2.5-0.5B-Instruct", openai_api_key="token-abc123", openai_api_base="http://localhost:8000/v1"
)
chain = prompt | llm | StrOutputParser()
```