import os
import requests
import logging
import json
from dotenv import load_dotenv
from tools_todo import tools_todo
from todo_service import get_tasks, add_task, update_task, delete_task

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv('OPENAI_KEY')
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


def execute_function(function_name: str, arguments: dict):
    if function_name == "get_tasks":
        return get_tasks()
    elif function_name == "add_task":
        return add_task(**arguments)
    elif function_name == "update_task":
        return update_task(**arguments)
    elif function_name == "delete_task":
        return delete_task(**arguments)
    else:
        return {"error": "Unknown function"}


async def agent_query(message: str):
    messages = [{"role": "user", "content": message}]

    try:
        response = requests.post(url, headers=headers, json={
            "model": "gpt-4o-mini",
            "messages": messages,
            "tools": tools_todo
        })
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": str(http_err)}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}

    completion = response.json()
    
    if 'choices' not in completion or not completion['choices']:
        logger.error(f"Invalid response: {completion}")
        return {"error": "Invalid response from OpenAI"}
    
    assistant_message = completion['choices'][0]['message']
    
    if not assistant_message.get('tool_calls'):
        return completion

    logger.info(assistant_message)
    
    messages.append(assistant_message)
    
    for tool_call in assistant_message['tool_calls']:
        function_name = tool_call['function']['name']
        args = json.loads(tool_call['function']['arguments'])
        
        result = execute_function(function_name, args)
        
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call['id'],
            "content": json.dumps(result, ensure_ascii=False)
        })

    logger.info(messages)

    try:
        response2 = requests.post(url, headers=headers, json={
            "model": "gpt-4o-mini",
            "messages": messages,
            "tools": tools_todo
        })
        response2.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": str(http_err)}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}

    return response2.json()
