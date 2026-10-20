
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

load_dotenv()

# 1. Connect to the Apex model
llm = ChatOpenAI(
    model="free/glm-5.3-flash",
    base_url="https://api.apinex.bond/v1",
    api_key=os.environ["APEX_API_KEY"],
    temperature=0.3,
    max_tokens=300,
)

# 2. Define the prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a friendly programming teacher. "
        "Answer clearly and use practical examples."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# 3. Create the chain
chain = prompt | llm

# 4. Get persistent history from SQLite
def get_session_history(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///chat_history.db",
    )

# 5. Automatically load and save conversation messages
chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# Keep this ID the same when reopening the app
session_id = "my-learning-chat"

print("AI Learning Assistant")
print("History is stored in chat_history.db")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    try:
        response = chatbot.invoke(
            {"question": question},
            config={
                "configurable": {
                    "session_id": session_id
                }
            },
        )

        print("\nAI:", response.content, "\n")

    except Exception as error:
        print(f"\nRequest failed: {error}\n")
