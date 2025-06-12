import os

from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever

from app.vectorstore.chroma import get_chroma_client

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

document_store = get_chroma_client()

# Prompt builder
prompt_builder = PromptBuilder(template="""
You are a helpful assistant having a conversation with a user. Here is the chat history and the latest user question.

{% if chat_history %}
Chat history:
{% for turn in chat_history %}
User: {{ turn.user }}
Assistant: {{ turn.assistant }}
{% endfor %}
{% endif %}

Now answer the latest question.

{% for doc in documents %}
[{{ doc.meta['created_at'] }} | {{ doc.meta['id'] }} ]
{{ doc.content }}

{% endfor %}

Question: {{ query }}
Answer (based on the most recent and relevant document only, and prioritize the statements of the most recent documents and bigger ids):
""",required_variables=["query", "documents", "chat_history"])

generator = OpenAIGenerator(api_key=Secret.from_token(OPENAI_API_KEY), model="gpt-3.5-turbo")
rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", ChromaQueryTextRetriever(document_store))
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", generator)
rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")

chat_history = []

def ask_question(query: str) -> str:
    result = rag_pipeline.run(
        {
            "prompt_builder": {
                "query": query,
                "chat_history": chat_history
            },
            "retriever": {
                "query": query,
                "top_k": 3
            }
        })
    answer = result["llm"]["replies"][0]
    chat_history.append({"user": query, "assistant": answer})
    return answer