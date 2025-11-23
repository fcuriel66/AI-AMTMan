import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from openai import embeddings

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")


def setup_rag_components():
    # Offline Phase

    # 1. Load
    loader = TextLoader("ADM_AMM_1285_TREE.xml")
    #loader = PyPDFLoader("100-MPP1285-INTRODUCTION.PDF")
    docs = loader.load()
    print(f"Loaded {len(docs)} documents!")

    # 2. Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    print(f"Document split into {len(chunks)} chunks!")

    # 3. Embed & 4. Store
    print("Creating vector store")
    vectorstore = FAISS.from_documents(documents=chunks,
                                       embedding=OpenAIEmbeddings(model="text-embedding-3-small", api_key=API_KEY))
    print("Vector store created successfully")

    model = ChatOpenAI(api_key=API_KEY, model="gpt-5-mini")

    # setup retriever
    retriever = vectorstore.as_retriever()

    return retriever, model


if __name__ == "__main__":
    # Offline
    retriever, model = setup_rag_components()

    # Online
    while True:
        user_question = input("\nPlease briefly describe the symptoms of the failure or problem: ")

        print("Thinking...")

        # 1. Retrieve
        retrieved_docs = retriever.invoke(user_question)

        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        # 2. Augment
        prompt_template = f"""You are an experienced E145 aircraft technician.
        Print the ATA Chapters and its description contained in this context document. 
        You will be presented with symptoms of an aircraft failure as a user question. Use 
        your knowledge and the context document to determine which 
        systems and components are the most likely involved. List them as a table. Maximum 2
        systems and 2 components:

        {context}

        Aircraft Failure Symptoms: {user_question}. 
        Suggest possible course of action but be brief and advise to always use the official 
        and updated manufacturer's maintenance manual.
        """

        # 3. Generate
        response = model.invoke(prompt_template)

        print("\nAnswer:\n", response.content)