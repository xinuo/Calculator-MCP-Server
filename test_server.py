#!/usr/bin/env python3
"""
Test script for the Calculator MCP Server
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_basic_arithmetic():
    """Test basic arithmetic operations"""
    print("=== Testing Basic Arithmetic ===")
    
    operations = [
        {"operation": "add", "a": 10, "b": 5},
        {"operation": "subtract", "a": 10, "b": 5},
        {"operation": "multiply", "a": 10, "b": 5},
        {"operation": "divide", "a": 10, "b": 5},
    ]
    
    for op in operations:
        response = requests.post(
            f"{BASE_URL}/tools/calculate",
            json=op,
            headers={"Content-Type": "application/json"}
        )
        print(f"{op['operation']}: {response.json()}")

def test_yoy_mom():
    """Test YoY and MoM calculations"""
    print("\n=== Testing YoY/MoM Calculations ===")
    
    # YoY test
    yoy_data = {"current_value": 120, "previous_year_value": 100}
    response = requests.post(
        f"{BASE_URL}/tools/calculate_yoy",
        json=yoy_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"YoY: {response.json()}")
    
    # MoM test
    mom_data = {"current_value": 110, "previous_month_value": 100}
    response = requests.post(
        f"{BASE_URL}/tools/calculate_mom",
        json=mom_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"MoM: {response.json()}")

def test_percentage():
    """Test percentage calculations"""
    print("\n=== Testing Percentage Calculations ===")
    
    percentage_data = {"part": 25, "whole": 100}
    response = requests.post(
        f"{BASE_URL}/tools/calculate_percentage",
        json=percentage_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Percentage: {response.json()}")

def test_proportion():
    """Test proportion calculations"""
    print("\n=== Testing Proportion Calculations ===")
    
    proportion_data = {"values": [10, 20, 30, 40]}
    response = requests.post(
        f"{BASE_URL}/tools/calculate_proportion",
        json=proportion_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Proportion: {response.json()}")

def test_batch_calculations():
    """Test batch calculations"""
    print("\n=== Testing Batch Calculations ===")
    
    batch_data = {
        "calculations": [
            {"type": "arithmetic", "operation": "multiply", "a": 5, "b": 3},
            {"type": "yoy", "current_value": 150, "previous_year_value": 100},
            {"type": "percentage", "part": 75, "whole": 300},
            {"type": "proportion", "values": [1, 2, 3, 4]}
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/tools/batch_calculate",
        json=batch_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Batch: {json.dumps(response.json(), indent=2)}")

def test_error_handling():
    """Test error handling"""
    print("\n=== Testing Error Handling ===")
    
    # Division by zero
    response = requests.post(
        f"{BASE_URL}/tools/calculate",
        json={"operation": "divide", "a": 10, "b": 0},
        headers={"Content-Type": "application/json"}
    )
    print(f"Division by zero: {response.json()}")
    
    # Zero whole in percentage
    response = requests.post(
        f"{BASE_URL}/tools/calculate_percentage",
        json={"part": 10, "whole": 0},
        headers={"Content-Type": "application/json"}
    )
    print(f"Zero whole: {response.json()}")

def main():
    """Run all tests"""
    try:
        # Test server availability
        response = requests.get(f"{BASE_URL}/")
        print(f"Server info: {response.json()}")
        
        test_basic_arithmetic()
        test_yoy_mom()
        test_percentage()
        test_proportion()
        test_batch_calculations()
        test_error_handling()
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server. Make sure the server is running on port 8000")
        print("Start the server with: python calculator_mcp_server.py")

if __name__ == "__main__":
    main()
