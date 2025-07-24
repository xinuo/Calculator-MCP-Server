# Calculator MCP Server

A Python-based MCP server using FastMCP that provides comprehensive calculation tools including basic arithmetic, year-over-year/month-over-month comparisons, and percentage calculations.

## Features

- **Basic Arithmetic**: Addition, subtraction, multiplication, division
- **YoY Calculations**: Year-over-year growth analysis
- **MoM Calculations**: Month-over-month growth analysis
- **Percentage Calculations**: Part-to-whole percentage calculations
- **Proportion Analysis**: Calculate proportions for multiple values
- **Batch Processing**: Perform multiple calculations in a single request

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python calculator_mcp_server.py
```

The server will start on port 8000 with streamable HTTP transport.

## Available Tools

### 1. Basic Arithmetic (`calculate`)
Perform basic arithmetic operations.

**Parameters:**
- `operation`: "add", "subtract", "multiply", or "divide"
- `a`: First number
- `b`: Second number

**Example:**
```json
{
  "operation": "add",
  "a": 10,
  "b": 5
}
```

### 2. Year-over-Year Growth (`calculate_yoy`)
Calculate YoY growth percentage.

**Parameters:**
- `current_value`: Current period value
- `previous_year_value`: Previous year value
- `as_percentage`: Return as percentage (default: true)

**Example:**
```json
{
  "current_value": 120,
  "previous_year_value": 100
}
```

### 3. Month-over-Month Growth (`calculate_mom`)
Calculate MoM growth percentage.

**Parameters:**
- `current_value`: Current month value
- `previous_month_value`: Previous month value
- `as_percentage`: Return as percentage (default: true)

**Example:**
```json
{
  "current_value": 110,
  "previous_month_value": 100
}
```

### 4. Percentage Calculation (`calculate_percentage`)
Calculate what percentage a part is of a whole.

**Parameters:**
- `part`: The part value
- `whole`: The whole/total value
- `as_percentage`: Return as percentage (default: true)

**Example:**
```json
{
  "part": 25,
  "whole": 100
}
```

### 5. Proportion Analysis (`calculate_proportion`)
Calculate proportions for a list of values.

**Parameters:**
- `values`: List of numeric values
- `normalize`: Whether to normalize proportions (default: false)

**Example:**
```json
{
  "values": [10, 20, 30, 40]
}
```

### 6. Batch Calculations (`batch_calculate`)
Perform multiple calculations in a single request.

**Example:**
```json
{
  "calculations": [
    {
      "type": "arithmetic",
      "operation": "multiply",
      "a": 5,
      "b": 3
    },
    {
      "type": "yoy",
      "current_value": 150,
      "previous_year_value": 100
    }
  ]
}
```

## Usage Examples

### Starting the Server
```bash
python calculator_mcp_server.py
```

### Testing with curl
```bash
# Basic addition
curl -X POST http://localhost:8000/tools/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'

# YoY calculation
curl -X POST http://localhost:8000/tools/calculate_yoy \
  -H "Content-Type: application/json" \
  -d '{"current_value": 120, "previous_year_value": 100}'

# Percentage calculation
curl -X POST http://localhost:8000/tools/calculate_percentage \
  -H "Content-Type: application/json" \
  -d '{"part": 25, "whole": 200}'
```

## API Endpoints

The server exposes the following endpoints:
- `GET /`: Server information
- `GET /tools`: List available tools
- `POST /tools/{tool_name}`: Execute specific tool
- `GET /docs`: API documentation

## Error Handling

All tools include comprehensive error handling:
- Division by zero protection
- Empty value validation
- Type checking and conversion
- Clear error messages in responses

## Development

To extend the server, add new tools using the `@mcp.tool()` decorator:

```python
@mcp.tool()
def your_new_tool(param1: type, param2: type) -> dict:
    """Tool description"""
    # Implementation
    return {"result": "your result"}
