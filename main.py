import os

from fastapi import FastAPI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

from models.AnswerModel import Answer
from models.QuestionModel import Question

os.environ["OPENAI_API_KEY"] = 'API-KEY'

# save to disk and reuse the model (repeated queries on the same data)
PERSIST = False

query = None

# can be used to start app with question param -> main.py 'This is my question'
# if len(sys.argv) > 1:
#    query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    loader = DirectoryLoader("data/")
    if PERSIST:
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []
#
# CLI input Prompts without fastApi
#
# while True:
#  if not query:
#    query = input("Prompt: ")
#  if query in ['quit', 'q', 'exit']:
#    sys.exit()
#  result = chain({"question": query, "chat_history": chat_history})
#  print(result['answer'])
#
#  chat_history.append((query, result['answer']))
#  query = None

app = FastAPI()


@app.post("/question")
async def question(q: Question):
    print("Question: " + q.text)
    result = chain({"question": q.text, "chat_history": chat_history})
    print("Answer: " + result['answer'])

    chat_history.append((q.text, result['answer']))
    return Answer(result['answer'])
