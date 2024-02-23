from llama_index.core import VectorStoreIndex,StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.core import StorageContext,load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore
import os,faiss

os.environ['OPENAI_API_KEY'] = "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"


# dimensions of text-ada-embedding-002
d = 1536
faiss_index = faiss.IndexFlatL2(d)

# vector
# documents = SimpleDirectoryReader("./data/train_data").load_data()
# vector_store = FaissVectorStore(faiss_index=faiss_index)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context
# )
# index.storage_context.persist()

# load index from disk
vector_store = FaissVectorStore.from_persist_dir("./storage")
storage_context = StorageContext.from_defaults(
    vector_store=vector_store, persist_dir="./storage"
)
index = load_index_from_storage(storage_context=storage_context)

# Classification codes:
codes = {1: "digestive system diseases",
2 : "cardiovascular diseases",
3 : "neoplasms",
4 : "nervous system diseases",
5 : "general pathological conditions"}

import re

def extract_numbers(text):
    pattern = r'\d+'
    numbers = re.findall(pattern, text)
    numbers = [int(num) for num in numbers]
    return numbers[0]

def get_disease_classification(input_condition):
    question = f"""Return the classification for given patient condition {input_condition}"""
    chat_engine = index.as_chat_engine()
    response = chat_engine.chat(question)
    return codes.get(extract_numbers(response.response)[0])