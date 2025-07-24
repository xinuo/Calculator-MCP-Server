#!/usr/bin/env python3
"""
Calculator MCP Server using FastMCP with streamable HTTP transport
Provides tools for basic arithmetic, YoY/MoM calculations, and percentage calculations
"""

from fastmcp import FastMCP
from typing import Union, Optional
import json

# Initialize FastMCP server with streamable HTTP transport
mcp = FastMCP(
    "Calculator Server"
)

@mcp.tool()
def calculate(
    operation: str,
    a: float,
    b: float
) -> dict:
    """
    Perform basic arithmetic operations (add, subtract, multiply, divide)
    
    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'
        a: First number
        b: Second number
    
    Returns:
        Dictionary with result and operation details
    """
    operation = operation.lower()
    
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            return {"error": "Division by zero is not allowed"}
        result = a / b
    else:
        return {"error": f"Unsupported operation: {operation}"}
    
    return {
        "operation": operation,
        "a": a,
        "b": b,
        "result": result,
        "formatted": f"{a} {get_operator_symbol(operation)} {b} = {result}"
    }

def get_operator_symbol(operation: str) -> str:
    """Get the symbol for the operation"""
    symbols = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    }
    return symbols.get(operation, operation)

@mcp.tool()
def calculate_yoy(
    current_value: float,
    previous_year_value: float,
    as_percentage: bool = True
) -> dict:
    """
    Calculate Year-over-Year (YoY) growth
    
    Args:
        current_value: Current period value
        previous_year_value: Previous year value
        as_percentage: Return result as percentage (default: True)
    
    Returns:
        Dictionary with YoY calculation results
    """
    if previous_year_value == 0:
        return {"error": "Previous year value cannot be zero"}
    
    yoy_change = current_value - previous_year_value
    yoy_growth = (yoy_change / abs(previous_year_value)) * 100
    
    if not as_percentage:
        yoy_growth = yoy_growth / 100
    
    return {
        "current_value": current_value,
        "previous_year_value": previous_year_value,
        "absolute_change": yoy_change,
        "yoy_growth": round(yoy_growth, 2) if as_percentage else yoy_growth,
        "formatted": f"YoY: {yoy_growth:.2f}{'%' if as_percentage else ''}",
        "direction": "increase" if yoy_change > 0 else "decrease" if yoy_change < 0 else "no change"
    }

@mcp.tool()
def calculate_mom(
    current_value: float,
    previous_month_value: float,
    as_percentage: bool = True
) -> dict:
    """
    Calculate Month-over-Month (MoM) growth
    
    Args:
        current_value: Current month value
        previous_month_value: Previous month value
        as_percentage: Return result as percentage (default: True)
    
    Returns:
        Dictionary with MoM calculation results
    """
    if previous_month_value == 0:
        return {"error": "Previous month value cannot be zero"}
    
    mom_change = current_value - previous_month_value
    mom_growth = (mom_change / abs(previous_month_value)) * 100
    
    if not as_percentage:
        mom_growth = mom_growth / 100
    
    return {
        "current_value": current_value,
        "previous_month_value": previous_month_value,
        "absolute_change": mom_change,
        "mom_growth": round(mom_growth, 2) if as_percentage else mom_growth,
        "formatted": f"MoM: {mom_growth:.2f}{'%' if as_percentage else ''}",
        "direction": "increase" if mom_change > 0 else "decrease" if mom_change < 0 else "no change"
    }

@mcp.tool()
def calculate_percentage(
    part: float,
    whole: float,
    as_percentage: bool = True
) -> dict:
    """
    Calculate percentage (part of whole)
    
    Args:
        part: The part value
        whole: The whole/total value
        as_percentage: Return result as percentage (default: True)
    
    Returns:
        Dictionary with percentage calculation results
    """
    if whole == 0:
        return {"error": "Whole value cannot be zero"}
    
    percentage = (part / abs(whole)) * 100
    
    if not as_percentage:
        percentage = percentage / 100
    
    return {
        "part": part,
        "whole": whole,
        "percentage": round(percentage, 2) if as_percentage else percentage,
        "formatted": f"{percentage:.2f}{'%' if as_percentage else ''}",
        "ratio": part / whole
    }

@mcp.tool()
def calculate_proportion(
    values: list[float],
    normalize: bool = False
) -> dict:
    """
    Calculate proportions for a list of values
    
    Args:
        values: List of numeric values
        normalize: Whether to normalize proportions to sum to 1 (default: False)
    
    Returns:
        Dictionary with proportion calculations
    """
    if not values:
        return {"error": "Values list cannot be empty"}
    
    total = sum(values)
    if total == 0:
        return {"error": "Sum of values cannot be zero"}
    
    proportions = [value / total for value in values]
    
    if normalize:
        proportions = [prop / sum(proportions) for prop in proportions]
    
    percentages = [prop * 100 for prop in proportions]
    
    return {
        "values": values,
        "total": total,
        "proportions": [round(p, 4) for p in proportions],
        "percentages": [round(p, 2) for p in percentages],
        "formatted": [
            f"Value {i+1}: {val} ({pct:.2f}%)"
            for i, (val, pct) in enumerate(zip(values, percentages))
        ]
    }

@mcp.tool()
def batch_calculate(
    calculations: list[dict]
) -> dict:
    """
    Perform multiple calculations in a single request
    
    Args:
        calculations: List of calculation specifications
    
    Returns:
        Dictionary with results for all calculations
    """
    results = []
    
    for calc in calculations:
        calc_type = calc.get("type")
        
        try:
            if calc_type == "arithmetic":
                result = calculate(
                    operation=calc["operation"],
                    a=calc["a"],
                    b=calc["b"]
                )
            elif calc_type == "yoy":
                result = calculate_yoy(
                    current_value=calc["current_value"],
                    previous_year_value=calc["previous_year_value"],
                    as_percentage=calc.get("as_percentage", True)
                )
            elif calc_type == "mom":
                result = calculate_mom(
                    current_value=calc["current_value"],
                    previous_month_value=calc["previous_month_value"],
                    as_percentage=calc.get("as_percentage", True)
                )
            elif calc_type == "percentage":
                result = calculate_percentage(
                    part=calc["part"],
                    whole=calc["whole"],
                    as_percentage=calc.get("as_percentage", True)
                )
            elif calc_type == "proportion":
                result = calculate_proportion(
                    values=calc["values"],
                    normalize=calc.get("normalize", False)
                )
            else:
                result = {"error": f"Unknown calculation type: {calc_type}"}
            
            results.append({
                "calculation": calc,
                "result": result
            })
            
        except Exception as e:
            results.append({
                "calculation": calc,
                "error": str(e)
            })
    
    return {
        "total_calculations": len(calculations),
        "successful": len([r for r in results if "error" not in r.get("result", {})]),
        "results": results
    }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(
    transport="http",
    port=8000)
