from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
import json
import csv


embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
)


def vector_db_creator(textfile_path):
    """Creates a vector database for a given text, JSON, or CSV file."""

    if not os.path.exists(textfile_path):
        raise FileNotFoundError(f"The file {textfile_path} does not exist. Please check the path.")

    # Extract filename and extension
    base_name, ext = os.path.splitext(os.path.basename(textfile_path))
    vectordb_directory = os.path.join("chat_core", "db", base_name)

    if os.path.exists(vectordb_directory):
        print(f"Vector database already exists at: {vectordb_directory}")
        return vectordb_directory

    print(f"Creating vector database at: {vectordb_directory}")

    # Load file content based on extension
    if ext == ".txt":
        with open(textfile_path, "r", encoding="utf-8") as file:
            content = file.read()

    elif ext == ".json":
        with open(textfile_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            content = json.dumps(json_data, indent=2)  # Convert JSON to string

    elif ext == ".csv":
        with open(textfile_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            content = "\n".join([", ".join(row) for row in csv_reader])  # Convert CSV rows to text

    else:
        raise ValueError("Unsupported file type. Only .txt, .json, and .csv are allowed.")

    # Split content into chunks
    text_splitter = CharacterTextSplitter(chunk_size=750, chunk_overlap=50)
    splits = text_splitter.split_text(content)  # Use split_text() instead of split_documents()

    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(splits)}")
    print(f"Sample chunk:\n{splits[0]}\n")

    # Convert chunks into document format
    documents = [{"page_content": chunk} for chunk in splits]

    # Create and store vector database
    db = Chroma.from_documents(documents, embeddings, persist_directory=vectordb_directory)

    print("\n--- Finished creating vector store ---")
    return vectordb_directory



def response_generator(query_prompt, vectordb_path_name):
    # textfile = textfile_name
    # database_given = textfile.strip(".txt")
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # vectordb_directory = os.path.join(current_dir, "db", database_given)
    vectordb_directory = vectordb_path_name

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
            "You are a helpful and knowledgeable assistant. Answer user queries concisely and naturally. If relevant data is provided, use it. If not, rely on your own knowledge, but never fabricate information. If unsure, politely say you don't know.",
        ),
        (
            "human",
            "{query}" if "{chunks}" == "" else "Based on this information: {chunks}, here is the answer: \n {query}",
        ),
    ]
)


    result_getter = prompt.invoke({"chunks": relevant_docs, "query": query})
    result = llm.invoke(result_getter)
    return result
