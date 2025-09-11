#  Demo MCP Server

This project is a **Minimal Model Context Protocol (MCP) Server** built with [FastMCP](https://pypi.org/project/mcp/).  
It demonstrates how to create simple MCP tools that can be used by MCP-compatible clients (such as ChatGPT, Claude Desktop, or custom clients).  

The server exposes two tools:  
- **Add Tool** → adds two integers.  
- **Weather Tool** → fetches current weather data for a given city from [wttr.in](https://wttr.in/).  

---

##  Requirements

- Python **3.9+**  
- `pip` (Python package manager)  

Install dependencies:

```bash
pip install -r requirements.txt
```

# ⚙️ Project Structure
```.
├── main.py          # MCP server implementation
├── requirements.txt # Dependencies
└── README.md        # Project documentation
```


# Usage
1. Start the MCP Server

Run:
```
python main.py
```

You should see logs like:

```
INFO:root:Starting MCP server 'Demo'...
```

 #  Dependencies

Key libraries used:

fastapi & starlette → for server framework

mcp → Model Context Protocol implementation

requests → to fetch weather data

uvicorn → ASGI server

Full list is available in requirements.txt.

 #  Notes

Weather data is fetched from wttr.in, which may have rate limits.

The add tool is just a demonstration of how to register tools in MCP.

# Future Improvements

Add more tools (currency conversion, news, etc.).

Replace wttr.in with OpenWeatherMap or other robust APIs.

Add .env support for API keys and configuration.

Dockerize for easy deployment.
