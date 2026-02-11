#!/usr/bin/env python3
"""Improved test suite for new MCP tools - No hardcoding"""

import sys
import json
import random
from pathlib import Path
from typing import Any, Callable, Dict

sys.path.insert(0, str(Path(__file__).parent))
from mcp_server.tools import compression, data, file, utility, text


class MockMCP:
    """Mock MCP server for testing"""

    def __init__(self) -> None:
        self.tools: Dict[str, Callable[..., Any]] = {}

    def tool(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.tools[func.__name__] = func
            return func

        return decorator


def test_compression_tools(config: Any) -> None:
    """Test compression tools with dynamic data"""
    print("=" * 60)
    print("Testing Compression Tools")
    print("=" * 60)

    mcp = MockMCP()
    compression.register_tools(mcp)

    # Create test files with random content
    test_files = []
    for i in range(2):
        file_path = config.get_temp_file(".txt")
        file_path.write_text(config.generate_random_text())
        test_files.append(str(file_path))

    # Test compress_zip
    zip_path = str(config.get_temp_file(".zip"))
    print(f"\n1. Testing compress_zip with {len(test_files)} files")
    result = mcp.tools["compress_zip"](test_files, zip_path, 6)
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Files: {data.get('file_count')}")

    # Test list_archive_contents
    print("\n2. Testing list_archive_contents")
    result = mcp.tools["list_archive_contents"](zip_path)
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Files: {data.get('file_count')}")

    # Test extract_zip
    extract_dir = str(config.get_temp_file("_extracted"))
    print("\n3. Testing extract_zip")
    result = mcp.tools["extract_zip"](zip_path, extract_dir)
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Extracted: {data.get('file_count')} files")

    print("\n[OK] Compression tools test completed")


def test_config_tools(config: Any) -> None:
    """Test configuration file tools with dynamic data"""
    print("\n" + "=" * 60)
    print("Testing Configuration File Tools")
    print("=" * 60)

    mcp = MockMCP()
    data.register_tools(mcp)

    # Generate dynamic YAML content
    yaml_content = f"""
project:
  name: test-project-{config.timestamp}
  version: {random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}
settings:
  debug: {random.choice(['true', 'false'])}
  port: {random.randint(8000, 9000)}
"""

    print("\n1. Testing parse_yaml")
    result = mcp.tools["parse_yaml"](yaml_content)
    parsed_data = json.loads(result)
    print(f"   Success: {'project' in parsed_data}")

    print("\n2. Testing yaml_to_json")
    result = mcp.tools["yaml_to_json"](yaml_content, 2)
    print(f"   Success: {len(result) > 0}")

    # Generate dynamic JSON content
    json_content = json.dumps(
        {
            "name": f"test-{config.timestamp}",
            "value": random.randint(1, 100),
            "items": [random.randint(1, 10) for _ in range(3)],
        }
    )

    print("\n3. Testing json_to_yaml")
    result = mcp.tools["json_to_yaml"](json_content)
    print(f"   Success: {len(result) > 0}")

    print("\n[OK] Configuration file tools test completed")


def test_file_diff_tools(config: Any) -> None:
    """Test file comparison tools with dynamic data"""
    print("\n" + "=" * 60)
    print("Testing File Comparison Tools")
    print("=" * 60)

    mcp = MockMCP()
    file.register_tools(mcp)

    # Create two files with slight differences
    base_text = config.generate_random_text(50)
    words = base_text.split()
    modified_text = " ".join(words[: len(words) // 2] + ["MODIFIED"] + words[len(words) // 2 + 1 :])

    file1 = config.get_temp_file(".txt")
    file2 = config.get_temp_file(".txt")
    file1.write_text(base_text)
    file2.write_text(modified_text)

    print("\n1. Testing diff_files")
    result = mcp.tools["diff_files"](str(file1), str(file2), 3, "unified")
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Changes: {data.get('total_changes')}")

    print("\n2. Testing diff_text")
    result = mcp.tools["diff_text"](base_text, modified_text, "unified")
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Changes: {data.get('total_changes')}")

    print("\n[OK] File comparison tools test completed")


def test_security_tools(config: Any) -> None:
    """Test security tools with dynamic parameters"""
    print("\n" + "=" * 60)
    print("Testing Security Tools")
    print("=" * 60)

    mcp = MockMCP()
    utility.register_tools(mcp)

    # Test with random password length
    password_length = random.randint(12, 24)
    print(f"\n1. Testing generate_password (length: {password_length})")
    result = mcp.tools["generate_password"](password_length, True, True, True)
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Strength: {data.get('strength_score')}")

    # Test with generated password
    test_password = data.get("password", "")
    print("\n2. Testing check_password_strength")
    result = mcp.tools["check_password_strength"](test_password)
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Level: {data.get('strength_level')}")

    print("\n[OK] Security tools test completed")


def test_text_similarity(config: Any) -> None:
    """Test text similarity with dynamic data"""
    print("\n" + "=" * 60)
    print("Testing Text Similarity Tool")
    print("=" * 60)

    mcp = MockMCP()
    text.register_tools(mcp)

    # Generate similar texts
    base_text = config.generate_random_text(30)
    words = base_text.split()
    similar_text = " ".join(words[: len(words) // 2] + words[len(words) // 2 + 2 :])

    print("\n1. Testing calculate_text_similarity (Levenshtein)")
    result = mcp.tools["calculate_text_similarity"](base_text, similar_text, "levenshtein")
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Similarity: {data.get('similarity')}")

    print("\n2. Testing calculate_text_similarity (Jaccard)")
    result = mcp.tools["calculate_text_similarity"](base_text, similar_text, "jaccard")
    data = json.loads(result)
    print(f"   Success: {data.get('success')}, Similarity: {data.get('similarity')}")

    print("\n[OK] Text similarity tool test completed")
