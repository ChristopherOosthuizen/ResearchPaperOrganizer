from openai import OpenAI
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

def generate_text(system_prompt, prompt):
    key = open("openaikey","r").read()
    os.environ["OPENAI_API_KEY"] = key
    messages = messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message.content

def summarization(doc):
    key = open("openaikey","r").read()
    os.environ["OPENAI_API_KEY"] = key
    documents = SimpleDirectoryReader(doc).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    return query_engine.query("Create me a indepth summerization of the doucment in about 250 words.").response