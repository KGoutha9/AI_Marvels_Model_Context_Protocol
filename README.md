# AI Marvels - Model Context Protocol (MCP) Demo

A comprehensive demonstration of the Model Context Protocol (MCP) implementation showcasing how to build scalable, modular AI agent systems with multiple tool servers. This project compares traditional custom tool approaches with the modern MCP architecture, demonstrating the benefits of service-oriented AI tool development.

## 🌟 Overview

This project demonstrates the power of the Model Context Protocol (MCP) by implementing a multi-server agent architecture that can seamlessly interact with different specialized tool servers. The implementation showcases how MCP enables better separation of concerns, scalability, and maintainability in AI agent systems.

### Key Features

- **Multi-Server Architecture**: Connect to multiple MCP servers simultaneously
- **Specialized Tool Servers**: Separate servers for different domains (OS operations, HR/Employee data)
- **Azure OpenAI Integration**: Powered by Azure's GPT-4 model
- **Before/After Comparison**: Complete examples showing traditional vs MCP approaches
- **WebSocket Support**: Real-time agent interaction through WebSocket endpoints
- **Jupyter Notebooks**: Interactive demonstrations and tutorials

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent Client  │    │  OS Tool Server │    │ HR Tool Server  │
│   (Port 8004)   │────│   (Port 8003)   │    │   (Port 8002)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Multi-Server    │
                    │ MCP Client      │
                    └─────────────────┘
```

## 📁 Project Structure

```
├── agent_server.py          # WebSocket-based agent server with MCP integration
├── HR_tool_server.py        # Employee information MCP tool server
├── os_tool_server.py        # Operating system operations MCP tool server
├── before_mcp.ipynb        # Traditional approach without MCP
├── after_mcp.ipynb         # Modern MCP-based implementation
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Azure OpenAI account and API credentials
- Required Python packages (see requirements.txt)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KGoutha9/AI_Marvels_Model_Context_Protocol.git
   cd AI_Marvels_Model_Context_Protocol
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   Create a `.env` file in the project root:
   ```env
   AZURE_API_VERSION_ENV=your_api_version
   AZURE_ENDPOINT_ENV=your_azure_endpoint
   AZURE_API_KEY_ENV=your_api_key
   ```

### Running the MCP Servers

Start each server in separate terminal windows:

1. **HR Tool Server (Employee Information)**
   ```bash
   python HR_tool_server.py
   ```
   Server will start on `http://localhost:8002`

2. **OS Tool Server (File Operations)**
   ```bash
   python os_tool_server.py
   ```
   Server will start on `http://localhost:8003`

3. **Agent Server (WebSocket Interface)**
   ```bash
   python agent_server.py
   ```
   Server will start on `http://localhost:8004`

## 🔧 Tool Servers

### HR Tool Server (Port 8002)
Provides employee-related information tools:
- `get_employee_supervisor(employee_ID)`: Get supervisor for an employee
- `get_employee_location(employee_name)`: Get employee location
- `get_employee_ID(employee_name)`: Get employee ID by name
- `get_employee_skill_set(employee_ID)`: Get employee skills

### OS Tool Server (Port 8003)
Provides file system operation tools:
- `get_absolute_path(folder_name, file_name)`: Search for files/folders
- `list_directory_contents(list_of_folder_paths)`: List directory contents
- `get_file_info(file_path)`: Get file content information
- `get_summary_of_file(file_content)`: Generate file content summary

## 📚 Usage Examples

### Jupyter Notebooks

#### Before MCP (`before_mcp.ipynb`)
Demonstrates the traditional approach with custom tools defined directly in the notebook:
- Custom tool definitions using `@tool` decorator
- Direct tool integration with LangChain agents
- Shows limitations of tight coupling

#### After MCP (`after_mcp.ipynb`)
Showcases the modern MCP approach:
- Multi-server connection setup
- Cross-server tool usage
- Scalable architecture benefits

### WebSocket Client Example

```python
import asyncio
import websockets
import json

async def query_agent():
    uri = "ws://localhost:8004/ws"
    async with websockets.connect(uri) as websocket:
        query = {
            "query": "Who is the supervisor of David?",
            "id": "session_001"
        }
        await websocket.send(json.dumps(query))
        response = await websocket.recv()
        print(json.loads(response))

asyncio.run(query_agent())
```

### Direct MCP Client Usage

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async with MultiServerMCPClient({
    "os_tool_server": {
        "url": "http://localhost:8003/sse",
        "transport": "sse",
    },
    "hr_tool_server": {
        "url": "http://localhost:8002/sse", 
        "transport": "sse",
    }
}) as client:
    agent = create_react_agent(model, client.get_tools())
    response = await agent.ainvoke({
        "messages": "What files are in the wellness folder?"
    })
```

## 🎯 Key Benefits of MCP Architecture

### 1. **Modular Development**
- Each tool server can be developed independently
- Different teams can maintain different services
- Easy to add new tool servers without modifying existing code

### 2. **Scalability**
- Tool servers can be deployed on different machines
- Independent scaling of different services
- Load balancing capabilities

### 3. **Maintainability**
- Clear separation of concerns
- Updates to tools don't require agent changes
- Version management for individual services

### 4. **Performance Isolation**
- Issues in one tool server don't affect others
- Independent performance optimization
- Better error handling and recovery

## 🔍 Comparison: Before vs After MCP

| Aspect | Before MCP | After MCP |
|--------|------------|-----------|
| **Tool Definition** | In-notebook custom functions | Dedicated MCP servers |
| **Scalability** | Limited, monolithic | Highly scalable, microservices |
| **Maintenance** | Requires notebook changes | Independent server updates |
| **Performance** | Single point of failure | Isolated performance |
| **Deployment** | All-in-one | Distributed services |
| **Team Collaboration** | Centralized development | Distributed team development |

## 🧪 Testing

### Manual Testing
1. Start all MCP servers
2. Open and run the Jupyter notebooks
3. Test WebSocket connections using the agent server

### Sample Queries
- **File Operations**: "What are the contents of Wellness.txt?"
- **Employee Queries**: "Who is the supervisor of David?"
- **Cross-Server**: "Find employee files in the documents folder"

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📖 References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)




---

**Note**: This is a demonstration project, do not use for Production. 
For production use, implement proper security measures, error handling, and monitoring.
