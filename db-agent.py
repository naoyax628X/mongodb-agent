import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import Tools

# Load environment variables
load_dotenv()

class DBAgent:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history = []
        self.tools = Tools()

    def process_user_query(self, user_query: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_query})
        
        system_prompt = """You are a helpful MongoDB query assistant. You have access to tools that can:
                        1. Get table difinition
                        2. Find records by query
                        3. Ask users for clarification when needed
                        4. Draw chart

                        Use these tools to help answer user questions. If information is ambiguous, ask for clarification."""
        
        while True:
            messages = [
                {"role": "system", "content": system_prompt},
                *self.conversation_history
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                tools=self.tools.create_tool_definitions(),
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            if not response_message.tool_calls:
                self.conversation_history.append({"role": "assistant", "content": response_message.content})
                return response_message.content
            
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"\nExecuting tool: {function_name} with args: {function_args}")
            
            result = self.tools.execute(function_name, function_args)
            
            self.conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": function_name,
                        "arguments": json.dumps(function_args)
                    }
                }]
            })
            
            self.conversation_history.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(result) if result is not None else "No result found"
            })
    
    def chat(self):
        print("MongoDB assistant Agent")
        print("Type 'quit' to exit.\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            try:
                response = self.process_user_query(user_input)
                print(f"\nAgent: {response}\n")
            except Exception as e:
                print(f"\nError: {e}\n")

if __name__ == "__main__":
    agent = DBAgent()
    agent.chat()