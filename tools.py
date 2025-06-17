import json
import os
import matplotlib.pyplot as plt
from bson.json_util import dumps
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient
import yaml 
from typing import Optional, Dict, Any, List

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

class Tools:

    def __init__(self):
        self.mongo_client: Optional[MongoClient] = None 
        self.db = None

    def create_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_table_list",
                    "description": "Fetches the current table definitions",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_table_scheme",
                    "description": "Fetches the table scheme details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "table_name": {
                                "type": "string",
                                "description": "The table name (e.g., 'mhCollectBg')"
                            }
                        },
                        "required": ["table_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_records",
                    "description": "Find records by query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "db_name": {
                                "type": "string",
                                "description": "The database name (e.g., 'mhCollect')"
                            },
                            "table_name": {
                                "type": "string",
                                "description": "The collection name (e.g., 'mhCollectBg')"
                            },
                            "query": {
                                "type": "string",
                                "description": "MongoDB query as JSON string (e.g., \"{ \\\"appUserId\\\": 4 }\")"
                            }
                        },
                        "required": ["db_name", "table_name", "query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "plot_chart",
                    "description": "Draw a 2-D chart from x and y data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The graph title"
                            },
                            "xlabel": {
                                "type": "string",
                                "description": "The label of x axis"
                            },
                            
                            "ylabel": {
                                "type": "string",
                                "description": "The label of y axis"
                            },
                            "x": {
                                "type": "array",
                                "description": "x datas (ex list , pandas Series)",
                                 "items": { "type": "number" }
                            },
                             "y": {
                                "type": "array",
                                "description": "y datas (ex list , pandas Series)",
                                 "items": { "type": "number" }
                            },
                        },
                        "required": ["title", "xlabel", "ylabel", "x", "y"] 
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ask_user_for_clarification",
                    "description": "Poses a question to the user and returns their response",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question_to_user": {
                                "type": "string",
                                "description": "The question to ask the user"
                            }
                        },
                        "required": ["question_to_user"]
                    }
                }
            }
        ]

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if tool_name == "get_table_list":
            return self.get_table_list() 
        elif tool_name == "get_table_scheme":
            return self.get_table_scheme(arguments["table_name"])
        elif tool_name == "find_records":
            return self.find_records(arguments["db_name"], arguments["table_name"], arguments["query"])
        elif tool_name == "plot_chart":
            return self.plot_chart(arguments["title"], arguments["xlabel"], arguments["ylabel"], arguments["x"], arguments["y"])
        elif tool_name == "ask_user_for_clarification":
            return self.ask_user_for_clarification(arguments["question_to_user"])
        else:
            return None
        
    def read_table_scheme_details(self, table_name) -> Optional[str]:
        base_dir  = Path(__file__).resolve().parent
        file_path = base_dir / "scheme" / f"{table_name}.yaml"

        if not file_path.is_file():
            print(f"❌ File not found: {file_path}")
            return None

        try:
            with file_path.open(encoding="utf-8") as f:
                data: Dict[str, Any] = yaml.safe_load(f)

            return json.dumps(data, ensure_ascii=False, indent=2)
        
        except yaml.YAMLError as e:
            print(f"❌ YAML parsing error: {e}")
            return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


    def read_table_txt(self) -> Optional[str]:
        print("read text...")        
        base_dir  = Path(__file__).resolve().parent
        file_path = base_dir / "scheme" / "tables.yaml"

        if not file_path.is_file():
            print(f"❌ File not found.: {file_path}")
            return None

        try:  
            with file_path.open(encoding="utf-8") as f:
                data: Dict[str, Any] = yaml.safe_load(f)

            return json.dumps(data, ensure_ascii=False, indent=2)
        
        except yaml.YAMLError as e:
            print(f"❌ YAML parsing error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
        
    def get_cluster(self) -> MongoClient:
        if self.mongo_client:
            return self.mongo_client
        try:
            print("get_cluster: obtaining URI …")
            mongo_uri = MONGODB_URL

            print("get_cluster: connecting …")
            self.mongo_client   = MongoClient(mongo_uri, serverSelectionTimeoutMS=10_000)
            self.mongo_client.admin.command("ping")   # 接続確認

            print("✅ Connected to MongoDB cluster")
            return self.mongo_client

        except Exception as exc:
            print("❌ MongoDB Connection Error:", exc)
            raise

    def get_table_list(self) -> Optional[str]:
        print("get table list...")
        try:
            table_txt = self.read_table_txt()
            if table_txt:
                return table_txt
            return None
        
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None
        
    def get_table_scheme(self, table_name) -> Optional[str]:
        print("get_table_scheme...")
        print(table_name)
        try:
            table_txt = self.read_table_scheme_details(table_name=table_name)
            if table_txt:
                return table_txt
            return None
        
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None
        
    def find_records(self, db_name, table_name, query) -> Optional[str]:
        print("find_records")
        print(table_name)
        print(db_name)
        print(query)
        try:
            if isinstance(query, str):
                query_dict = json.loads(query)
            elif isinstance(query, dict):
                query_dict = query
            else:
                raise TypeError("The query must be either a dict or a JSON string.")

            limit = 10
            indent = 0

            cluster = self.get_cluster()
            collection = cluster[db_name][table_name]

            cursor   = collection.find(query_dict).limit(limit) if limit else collection.find(query)
            records  = list(cursor)

            if not records:
                print("⚠️ No matching records.")
                return None

            # BSON 型(ObjectId など)も含めて安全に文字列化
            return dumps(records, ensure_ascii=False, indent=indent)


        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None
    

    def plot_chart(self,title, xlabel, ylabel, x, y):
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)

        plt.show()    

    def ask_user_for_clarification(self, question_to_user: str) -> str:
        print(f"\nAgent needs clarification: {question_to_user}")
        response = input("Your response: ")
        return response
    