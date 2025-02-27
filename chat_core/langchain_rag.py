from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
)

def vector_db_creator(textfile_name):
    textfile = textfile_name
    database_given = textfile.strip(".txt")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "documents", textfile)
    vectordb_directory = os.path.join(current_dir, "db", database_given)

    if not os.path.exists(vectordb_directory):
        print("db directory doesn't exist, intializing it")

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"The file {file_path} does not exist. Please check the path."
            )

        document_loader = TextLoader(file_path)
        document = document_loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=750, chunk_overlap=50)
        splits = text_splitter.split_documents(document)

        print("\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(splits)}")
        print(f"Sample chunk:\n{splits[0].page_content}\n")

        print("\n--- Creating embeddings ---")
        db = Chroma.from_documents(splits, embeddings, persist_directory=vectordb_directory)
        print("\n--- Finished creating vector store ---")


def response_generator(query_prompt, textfile_name):
    textfile = textfile_name
    database_given = textfile.strip(".txt")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vectordb_directory = os.path.join(current_dir, "db", database_given)

    db = Chroma(persist_directory=vectordb_directory, embedding_function=embeddings)
    
    query = query_prompt
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 5, "score_threshold": 0.4},
    )
    relevant_docs = retriever.invoke(query)

    llm = OllamaLLM(model="llama3.2")
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "you are in a rag, i'll provide you matching chunks of data. Answer the questions accordingly",
            ),
            (
                "human",
                "here are the related chunks of data for the query : {chunks}... \n and here is the query: {query}",
            ),
        ]
    )

    result_getter = prompt.invoke({"chunks": relevant_docs, "query": query})
    result = llm.invoke(result_getter)
    return result
