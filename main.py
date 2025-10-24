from fastmcp import FastMCP, Context
import httpx
from langgraph_sdk import get_client
import logging
from dotenv import load_dotenv
# If you're using a remote server, initialize the client with `get_client(url=REMOTE_URL)`
load_dotenv()
logging.basicConfig(level=logging.INFO,filename='logs.log')
logger = logging.getLogger()
app = FastMCP("LangGraphMCP")

LANGGRAPH_API = "http://127.0.0.1:2024"



@app.tool()
async def interactive_research(topic: str, 
                               ctx: Context
                               ):
    client = get_client(url=LANGGRAPH_API)
    assistants = await client.assistants.search()
    agent = assistants[0]
    thread = await client.threads.create()
    research_result = None
    input = {"messages": [{"role": "human", "content": topic}]}
    while research_result ==  None:
        async for chunk in client.runs.stream(thread['thread_id'], agent['assistant_id'], input=input, stream_mode="custom"):
            logger.info(chunk.event)
            logger.info(chunk.data)
            print(chunk._fields)
            print(type(chunk))
            print(chunk.event)
            print(chunk.data)
            if chunk.event == 'clarification':
                clarification_result = ctx.elicit(chunk.data['question'], response_type=str)
                input = {"messages": [{"role": "human", "content": clarification_result.data}]}
                continue
            if chunk.event == 'final':
                research_result = chunk.data['final_report']
    
    return research_result


if __name__ == "__main__":
    app.run(transport='http')