# MongoDB Assistant Agent

A command-line agent that lets you chat in natural language, run MongoDB queries, and even draw quick charts—all powered by the OpenAI function-calling API.

---

## ✨ Features

| Capability | Description |
|------------|-------------|
| **Schema lookup** | Lists available collections and shows YAML-based column definitions. |
| **Ad-hoc queries** | Accepts plain-language requests (e.g. “Show diaries uploaded on 2025-05-01”) and turns them into `find()` queries. |
| **Clarification loop** | Automatically asks follow-up questions when the request is ambiguous. |
| **Quick plotting** | Generates simple matplotlib charts (line / bar) from queried data. |
| **Tool plug-in system** | All capabilities are defined in **`tools.py`** and exposed through OpenAI function calling. |

---

## 🗂 Project layout
```text
├── agent.py # Chat loop & OpenAI orchestration
├── tools.py # All tool implementations (DB, YAML, charts)
├── scheme/ # YAML table definitions
│ ├── tables.yaml
│ └── <table>.yaml
├── requirements.txt
└── README.md
```
---

## ⚙️ Prerequisites

* Python **3.9+**
* A running MongoDB cluster (Atlas or self-hosted)
* OpenAI API access (GPT-4-Turbo or higher)

---

## 🔧 Setup

```bash
# 1. Clone & enter the repo
git clone https://github.com/your-org/mongodb-assistant.git
cd mongodb-assistant

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```
---

## Environment variables
Create a .env file (or export variables):

OPENAI_API_KEY=sk-******************************

MONGODB_URL=mongodb+srv://user:pass@cluster0.xxxx.mongodb.net/?retryWrites=true&w=majority

---

## 🚀 Running the agent

```
python agent.py
```

You’ll see:
```
MongoDB assistant Agent
Ask me about data questions!
Type 'quit' to exit.

You:
```

Example session:
```
You: Show step counts for user 4 in April 2025
Executing tool: find_records ...
Agent: Here are the records … Would you like a line chart?
You: Yes, plot it
```

---

## 📝 Writing table schemas

- scheme/tables.yaml – master list of collections
- scheme/<collection>.yaml – column definitions

Column YAML snippet:
```
columns:
  - no: 1
    logical_name: "User ID"
    physical_name: appUserId
    data_type: int
    not_null: true
    default: null
    note: ""
```

---

## Extending
- Add a new tool
Implement the function in tools.py, register it in create_tool_definitions(), and map it in execute().

- Add more chart types
Return base64-encoded PNGs instead of calling plt.show() if you plan to integrate with a web UI.

- Swap databases
Replace MongoClient with any driver; only get_cluster() and query helpers need updates.

---

## License
MIT © 2025 Naoya Enokida