import os
from dotenv import load_dotenv
from langchain import HuggingFaceHub, OpenAI, PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents import initialize_agent, load_tools

# Load environment variables from .env file
load_dotenv()

api_key1 = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_key1

api_key2 = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key2


llm1 = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature": 0.5})
llm2 = OpenAI(temperature=0.5, model_name="gpt-3.5-turbo")

query = "Can George Washington meet Barrack Obama?"

print("\nQuestion: ", query)

# messages = [
#     SystemMessage(content="You are a helpful assistant."),
#     HumanMessage(content=query),
# ]

response1 = llm1(query)
# response2 = llm2(messages).content

print("\nHuggingFaceHub google/flan-t5-xl:\n ", response1)
# print("\nOpenAI gpt-3.5-turbo:\n ", response2)

# PromptTemplate
template = """Question: {question}
Let's explain to a 5 year old.
Answer: """


prompt = PromptTemplate(template=template, input_variables=["question"])
prompt.format(question=query)

llm_chain = LLMChain(prompt=prompt, llm=llm1)

formatted_query = prompt.format(question=query)
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content=formatted_query),
]

response1 = llm_chain.run(query)
# response2 = llm2(messages).content

print("\nUsing PromptTemplate:\n")
print("\nHuggingFaceHub google/flan-t5-xl:\n ", response1)
# print("\nOpenAI gpt-3.5-turbo:\n ", response2)

tools = load_tools(["wikipedia", "llm-math"], llm=llm2)
agent = initialize_agent(
    tools, llm=llm2, agent="zero-shot-react-description", verbose=True
)

response2 = agent.run(
    "What year did Malaysia gain independence? And the year to the power of 3"
)

print("Using Agent: ", response2)
