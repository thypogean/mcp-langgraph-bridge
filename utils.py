llm_output = "{\"need_clarification\": true, \"question\": \"- Кто именно имеется в виду под \\\"репер хаски\\\"? Это может быть определенный рэпер или артист, известный как Хаски? \\\\\\\\\\\\n- Какое влияние на политику имеется в виду? Это может быть влияние через музыку, социальные комментарии, участие в политических движениях или что-то еще?\", \"verification\": \"\"}",
obj = {'messages': [
        {'content': 'Что необходимо для успешного прохождения собеседования', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': '009526c4-7b95-48ac-9839-9eb2c712c544', 'example': False
        },
        {'content': llm_output, 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'ai', 'name': None, 'id': '758f046c-0ee5-4360-94c3-2fd1dfef397b', 'example': False, 'tool_calls': [], 'invalid_tool_calls': [], 'usage_metadata': None
        }
    ], 'supervisor_messages': [
        {'content': 'You are a research supervisor. Your job is to conduct research by calling the "ConductResearch" tool. For context, today\'s date is Tue Oct 21, 2025.\n\n<Task>\nYour focus is to call the "ConductResearch" tool to conduct research against the overall research question passed in by the user. \nWhen you are completely satisfied with the research findings returned from the tool calls, then you should call the "ResearchComplete" tool to indicate that you are done with your research.\n</Task>\n\n<Available Tools>\nYou have access to three main tools:\n1. **ConductResearch**: Delegate research tasks to specialized sub-agents\n2. **ResearchComplete**: Indicate that research is complete\n3. **think_tool**: For reflection and strategic planning during research\n\n**CRITICAL: Use think_tool before calling ConductResearch to plan your approach, and after each ConductResearch to assess progress. Do not call think_tool with any other tools in parallel.**\n</Available Tools>\n\n<Instructions>\nThink like a research manager with limited time and resources. Follow these steps:\n\n1. **Read the question carefully** - What specific information does the user need?\n2. **Decide how to delegate the research** - Carefully consider the question and decide how to delegate the research. Are there multiple independent directions that can be explored simultaneously?\n3. **After each call to ConductResearch, pause and assess** - Do I have enough to answer? What\'s still missing?\n</Instructions>\n\n<Hard Limits>\n**Task Delegation Budgets** (Prevent excessive delegation):\n- **Bias towards single agent** - Use single agent for simplicity unless the user request has clear opportunity for parallelization\n- **Stop when you can answer confidently** - Don\'t keep delegating research for perfection\n- **Limit tool calls** - Always stop after 6 tool calls to ConductResearch and think_tool if you cannot find the right sources\n\n**Maximum 5 parallel agents per iteration**\n</Hard Limits>\n\n<Show Your Thinking>\nBefore you call ConductResearch tool call, use think_tool to plan your approach:\n- Can the task be broken down into smaller sub-tasks?\n\nAfter each ConductResearch tool call, use think_tool to analyze the results:\n- What key information did I find?\n- What\'s missing?\n- Do I have enough to answer the question comprehensively?\n- Should I delegate more research or call ResearchComplete?\n</Show Your Thinking>\n\n<Scaling Rules>\n**Simple fact-finding, lists, and rankings** can use a single sub-agent:\n- *Example*: List the top 10 coffee shops in San Francisco → Use 1 sub-agent\n\n**Comparisons presented in the user request** can use a sub-agent for each element of the comparison:\n- *Example*: Compare OpenAI vs. Anthropic vs. DeepMind approaches to AI safety → Use 3 sub-agents\n- Delegate clear, distinct, non-overlapping subtopics\n\n**Important Reminders:**\n- Each ConductResearch call spawns a dedicated research agent for that specific topic\n- A separate agent will write the final report - you just need to gather information\n- When calling ConductResearch, provide complete standalone instructions - sub-agents can\'t see other agents\' work\n- Do NOT use acronyms or abbreviations in your research questions, be very clear and specific\n</Scaling Rules>', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'system', 'name': None, 'id': None
        },
        {'content': 'Research question: What are the key factors that contribute to a successful job interview, including preparation, communication skills, body language, and the specific requirements of different industries or job roles?', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': None, 'example': False
        }
    ], 'research_brief': 'Research question: What are the key factors that contribute to a successful job interview, including preparation, communication skills, body language, and the specific requirements of different industries or job roles?', 'raw_notes': [], 'notes': []
}


from pydantic import BaseModel, ValidationError
import json

# Определяем схему structured output
class ClarificationSchema(BaseModel):
    need_clarification: bool
    question: str
    verification: str

def check_clarification(s: str):
    try:
        data = json.loads(s)  # пробуем распарсить строку
    except json.JSONDecodeError:
        return False, "Not a valid JSON"

    try:
        obj = ClarificationSchema(**data)
        return True, obj  # всё ок, возвращаем объект
    except ValidationError as e:
        return False, e.errors()  # не соответствует схеме

# Пример использования

if (obj['messages'][-1]['type']=='ai'):
    is_valid, result = check_clarification(obj['messages'][-1]['content'][0])

print(result.need_clarification)