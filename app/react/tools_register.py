import inspect
import functools

import json

from typing import Dict, Any, Callable, List, Type, Union, get_type_hints, get_origin, get_args
from datetime import datetime, date
from flask import jsonify, Response
from app.utils.logging import logger
from app.models.base import BaseModel
from playhouse.shortcuts import model_to_dict

class ToolExecutionError(Exception):
    """Exception raised when a tool execution fails."""
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

# Tool registry
tools = {}

def create_tool_executor(func: Callable) -> Callable:
    """Create a function that executes a service method with JSON/Dict parameters.
    
    Args:
        func: The function to execute
        
    Returns:
        A function that accepts JSON/Dict and calls the service method
    
    Raises:
        ToolExecutionError: If the function raises an exception
    """
    def executor(params: Dict[str, Any]) -> Any:
        # Call the method
        try:
            results = func(**params)
            # 如果返回的是BaseModel，则转换为字典
            if isinstance(results, BaseModel):
                return model_to_dict(results)
            # 如果返回的是列表，则转换为字典列表
            elif isinstance(results, list):
                return [model_to_dict(result) for result in results]
            # 如果返回的是其他类型，则直接返回
            return results
        except Exception as e:
            logger.exception(f"Error executing {func.__name__}")
            raise ToolExecutionError(f"Error executing {func.__name__}: {str(e)}", original_error=e)
    
    return executor


def register_as_tool(func):
    """Register a function as a tool for the ReAct agent."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Extract signature and docstring
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func) or ""
    
    # Get the actual function from staticmethod
    actual_func = func.__func__ if isinstance(func, staticmethod) else func

    # Register the tool with metadata
    tools[func.__name__] = {
        "function": create_tool_executor(actual_func),
        "description": docstring,
        "parameters": {
            name: {
                "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty else "any",
                "description": "" # You might want to parse docstring for param descriptions
            }
            for name, param in signature.parameters.items() if name != 'self'
        }
    }
    logger.info(f"tool registered: {func.__name__}")
    return wrapper
