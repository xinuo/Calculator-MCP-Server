#!/bin/bash
# Script to run the Calculator MCP Server with HTTP transport

echo "Starting Calculator MCP Server with HTTP transport..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the server with HTTP transport
python calculator_mcp_server.py serve
