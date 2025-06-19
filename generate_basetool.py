from typing import Callable, Type, Literal
from pydantic import BaseModel
from langchain_core.tools import BaseTool, tool

def create_tool(
    func: Callable,
    args_schema: Type[BaseModel],
    name: str,
    description: str,
    return_format: Literal["content", "content_and_artifact"] = "content"
) -> BaseTool:
    """
    Dynamically creates a LangChain BaseTool with customizable return format.
    """

    def wrapped_func(*args, **kwargs):
        """
        Internal wrapped function to standardize output format (content or content + artifact).
        """
        result = func(*args, **kwargs)

        if return_format == "content_and_artifact":
            if isinstance(result, tuple) and len(result) == 2:
                return result
            return str(result), {"message": str(result)}

        return result[0] if isinstance(result, tuple) else str(result)

    tool_instance: BaseTool = tool(wrapped_func)
    tool_instance.name = name
    tool_instance.description = description
    tool_instance.args_schema = args_schema
    return tool_instance

