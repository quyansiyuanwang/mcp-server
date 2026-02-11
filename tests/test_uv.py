#!/usr/bin/env python3
"""Test python_format_code"""

import sys
import json
from pathlib import Path
from typing import Any, Callable, Dict

sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.tools import python


class MockMCP:
    def __init__(self) -> None:
        self.tools: Dict[str, Callable[..., Any]] = {}

    def tool(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.tools[func.__name__] = func
            return func

        return decorator


def test_format_code() -> None:
    print("=" * 60)
    print("Testing python_format_code")
    print("=" * 60)

    mcp = MockMCP()
    python.register_tools(mcp)

    # Test with unformatted code
    code = """
def hello(  x,y  ):
    return x+y
"""

    print("\nOriginal code:")
    print(code)

    print("\nTesting black formatter...")
    result = mcp.tools["python_format_code"](code, style="black")
    data = json.loads(result)

    if "error" in data:
        print(f"   Error: {data['error']}")
    elif "warning" in data:
        print(f"   Warning: {data['warning']}")
        print("   (black not installed, returned original code)")
    else:
        print("   Formatted code:")
        print(data.get("formatted_code", ""))


if __name__ == "__main__":
    test_format_code()
