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

service_registry = {}

def register_service(name: str, service_instance: Any) -> None:
    """Register a service instance with a name.
    
    Args:
        name: The name to register the service under
        service_instance: The service instance to register
    """
    service_registry[name] = service_instance
    print(f"Registered service instance: {name}")

def create_tool_executor(service_name: str, method_name: str) -> Callable:
    """Create a function that executes a service method with JSON parameters.
    
    Args:
        service_name: The name of the service in the registry
        method_name: The name of the method to call on the service
        
    Returns:
        A function that accepts JSON and calls the service method
    """
    def executor(json_params: Dict[str, Any]) -> Any:
        # Get the service instance
        if service_name not in service_registry:
            raise ToolExecutionError(f"Service '{service_name}' not registered")
            
        service = service_registry[service_name]
        
        # Get the method
        if not hasattr(service, method_name):
            raise ToolExecutionError(f"Method '{method_name}' not found on service '{service_name}'")
            
        method = getattr(service, method_name)
        
        # Get parameter information
        sig = inspect.signature(method)
        type_hints = get_type_hints(method)
        
        # Prepare parameters
        kwargs = {}
        
        for param_name, param in sig.parameters.items():
            # Skip 'self' parameter
            if param_name == 'self':
                continue
                
            # Check if parameter is in the JSON
            if param_name in json_params:
                param_value = json_params[param_name]
                kwargs[param_name] = param_value

                # temporarily disable type checking
                '''# Get the expected type
                param_type = type_hints.get(param_name, Any)
                
                # Convert the value to the expected type
                try:
                    converted_value = convert_param_value(param_value, param_type)
                    kwargs[param_name] = converted_value
                except ValueError as e:
                    raise ToolExecutionError(f"Invalid parameter '{param_name}': {str(e)}")'''
            elif param.default == inspect.Parameter.empty:
                # Required parameter missing
                raise ToolExecutionError(f"Required parameter '{param_name}' missing")
        
        # Call the method
        try:
            results = method(**kwargs)
            if isinstance(results, BaseModel):
                return model_to_dict(results)
            elif isinstance(results, list):
                return [model_to_dict(result) for result in results]
            return results
        except Exception as e:
            logger.exception(f"Error executing {service_name}.{method_name}")
            raise ToolExecutionError(f"Error executing {service_name}.{method_name}: {str(e)}", original_error=e)
    
    return executor



def register_as_tool(func):
    """Register a function as a tool for the ReAct agent."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Extract signature and docstring
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func) or ""
    
    # Get the service name from the function's module
    service_name = func.__module__.split('.')[-1]
    print("service_name", service_name)
    # Register the tool with metadata
    print(f"registering tool {func.__name__} from service {service_name}")
    tools[func.__name__] = {
        "function": create_tool_executor(service_name, func.__name__),
        "description": docstring,
        "parameters": {
            name: {
                "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty else "any",
                "description": "" # You might want to parse docstring for param descriptions
            }
            for name, param in signature.parameters.items() if name != 'self'
        }
    }
    print("tool registered", func.__name__)
    return wrapper

# Apply to your service methods
'''@register_as_tool
def get_product(product_id: int):
    """Get details for a specific product.
    
    Args:
        product_id: The ID of the product to retrieve
        
    Returns:
        Product details dictionary
    """
    # Implementation
    return {"id": product_id, "name": "Example Product", "price": 99.99}'''

# Now you can use the registered tools with your agent
def format_tools_for_agent():
    """Convert the registered tools into a format suitable for the agent."""
    return [
        {
            "name": name,
            "description": info["description"],
            "function": info["function"]
        }
        for name, info in tools.items()
    ]

# Create an initialization function instead of importing at the module level
def initialize_services():
    """Initialize and register all services.
    
    This function should be called from the application's main startup code
    after all services have been defined.
    """
    from app.services.analytics_service import AnalyticsService
    from app.services.assignment_service import AssignmentService
    from app.services.course_service import CourseService
    from app.services.knowledge_base_service import KnowledgeBaseService
    from app.services.knowledge_point_service import KnowledgePointService
    from app.services.user_service import UserService

    analytics_service = AnalyticsService()
    assignment_service = AssignmentService()
    course_service = CourseService()
    knowledge_base_service = KnowledgeBaseService()
    knowledge_point_service = KnowledgePointService()
    user_service = UserService()

    register_service("analytics_service", analytics_service)
    register_service("assignment_service", assignment_service)
    register_service("course_service", course_service)
    register_service("knowledge_base_service", knowledge_base_service)
    register_service("knowledge_point_service", knowledge_point_service)
    register_service("user_service", user_service)
    
    return {
        "analytics": analytics_service,
        "assignment": assignment_service,
        "course": course_service,
        "knowledge_base": knowledge_base_service,
        "knowledge_point": knowledge_point_service,
        "user": user_service
    }