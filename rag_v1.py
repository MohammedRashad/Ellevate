from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import ServiceContext, VectorStoreIndex, StorageContext,load_index_from_storage
# from llama_index.core.node_parser import SentenceSplitter, CodeSplitter, SemanticSplitterNodeParser, TokenTextSplitter
from llama_index.core.node_parser.file import SimpleFileNodeParser
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.replicate import Replicate
import qdrant_client
import replicate
import os
from literalai import LiteralClient
from llama_index.core.callbacks import CallbackManager
from llama_index.core import Settings

from config import * 
from utils import *

def rag_pipeline(setup_mode=False, collection_name="sampledata", files=[]):
    """
    The `rag_pipeline` function sets up a pipeline for using RAG (Retrieval-Augmented Generation) model
    for querying and answering questions.
    
    :param setup_mode: The `setup_mode` parameter in the `rag_pipeline` function is a boolean parameter
    that determines whether the pipeline is being set up in setup mode or not. When `setup_mode` is set
    to `True`, the function will create a new vector index from the provided documents and persist it to
    a, defaults to False (optional)
    :return: The `rag_pipeline` function returns three objects: `query_engine`, `llm`, and
    `vector_index`.
    """

    literal_client = LiteralClient(api_key=LITERAL_API_KEY)
    Settings.callback_manager = CallbackManager([literal_client.llama_index_callback()])

    print("Setting up RAG pipeline")

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
    llm = Replicate(model= REPLICATE_MODEL)
    print("-- Replicate model loaded")

    embed_model = HuggingFaceEmbedding(model_name=HF_EMBEDDING_MODEL)
    print("-- HuggingFace model loaded")

    client = qdrant_client.QdrantClient(url=QDRANT_URL,api_key=QDRANT_API_KEY)
    node_parser = SimpleFileNodeParser()
    vector_store = QdrantVectorStore(client=client, collection_name="q"+collection_name.replace("-", ""))
    print("-- Qdrant client loaded")


    if vector_store is not None:
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
    else:
        storage_context = None

    print("-- Storage context loaded")

    service_context = ServiceContext.from_defaults(llm=llm,  embed_model=embed_model)

    if setup_mode:
        print(files)
        reader = SimpleDirectoryReader(input_files = files)  #list_files(DATA_DIRECTORY_PATH)
        documents = reader.load_data()
        print("-- Data loaded")
        print(f"-- Loaded {len(documents)} docs")

        vector_index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context, service_context=service_context, show_progress=True)

        if storage_context:
            vector_index.storage_context.persist(persist_dir='persist_dir')
    else:
        vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)

    print("-- Vector index loaded")

    query_engine = vector_index.as_query_engine(response_mode=RESPONSE_MODE, verbose=True)

    print("\n\n RAG pipeline setup complete")

    return query_engine, llm ,vector_index
