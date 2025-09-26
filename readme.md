[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/thedev05-itsm-agent-badge.png)](https://mseep.ai/app/thedev05-itsm-agent)

# ITSM Agent

This project implements an **intelligent ITSM assistant** using **LangGraph**, **LangChain**, **MCP**, **Redis**, **Guardrails** and **Streamlit**.

It supports **hybrid workflows** with:
- **Local tools** → session handling, memory, RAG knowledge retrieval
- **MCP tools** → ServiceNow ticket creation & retrieval via MCP server
- **LangGraph Store Interface** → saving & fetching frequent memories
- **Persistence & Checkpointer Memory** → conversations survive restarts
- **Guardrails** → restricts responses to ITSM-only queries, restrict all unusual QnA
- **Redis** → user context (`sys_id`) and state management

---

## Setup

### 1️. Clone the repository

```bash
git clone https://github.com/thedev05/itsm-agent.git
cd itsm-agent
```

### 2️. Install dependencies

```bash
pip install -r requirements.txt
```

### 3️. Configure environment

Create a `.env` file in the project root:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=<your-azure-api-key>
AZURE_OPENAI_ENDPOINT=https://<your-azure-resource-name>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
AZURE_OPENAI_API_VERSION=2024-05-01-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# ServiceNow
SERVICENOW_URL=https://<your-instance>.service-now.com
SERVICENOW_USER=<your-servicenow-username>
SERVICENOW_PASS=<your-servicenow-password>

# Redis (Cloud)
REDIS_HOST=<your-redis-host>
REDIS_PORT=<your-redis-port>
REDIS_USERNAME=<your-redis-username>
REDIS_PASSWORD=<your-redis-password>

```

### Run MCP Server

Expose all MCP-based ServiceNow tools (ticket creation, ticket fetching, etc.):

```bash
cd MCP
python servicenow.py
```

### Run Streamlit Chat Interface

Start the interactive ITSM agent UI:

```bash
streamlit run main.py
```

## How It Works

**Steps:**

1. **Enter your Name and Email** → Agent will use this to creates session, validate users, generates `sys_id`, stores in Redis
2. **Ask queries** like "Not able to start VPNs" or "Create a ticket for wifi issue" or "Fetch my open incidents tickets"
3. **The LangGraph agent orchestrates:**
   - MCP tools (ServiceNow API)
   - Store interface (frequent memory, persistence, checkpoint recovery)
   - RAG retriever (FAQ/DOC answers)
   - Guardrails (ensure ITSM-only replies)

---

## Architecture

This ITSM agent combines multiple cutting-edge technologies:

- **LangGraph**: Orchestrates complex multi-step workflows
- **MCP Integration**: Secure ServiceNow API connectivity
- **Redis Storage**: Fast session and state management
- **RAG Knowledge Base**: Context-aware responses from documentation
- **Streamlit Interface**: User-friendly chat experience

- **Memory Persistence**: Conversations survive application restarts
