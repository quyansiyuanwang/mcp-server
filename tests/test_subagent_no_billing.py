"""
测试 Subagent 移除计费功能后的基本功能
"""

import os
from unittest.mock import Mock, patch

import pytest

from mcp_server.tools.subagent.handlers import SubagentManager, SubagentOrchestrator


def test_subagent_call_response_structure():
    """测试 subagent_call 返回的结构不包含 cost 字段"""
    # Mock API 响应
    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [{"message": {"role": "assistant", "content": "Test response"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
    }
    mock_response.raise_for_status = Mock()

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch("requests.post", return_value=mock_response):
            manager = SubagentManager()
            result = manager.call_ai(
                provider="openai",
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
            )

            # 验证返回结构
            assert "result" in result
            assert "usage" in result
            assert "model" in result
            assert "provider" in result
            assert "status" in result
            assert "elapsed_time" in result

            # 确保没有 cost 字段
            assert "cost" not in result


def test_parallel_execution_no_cost():
    """测试并行执行不包含 cost 统计"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [{"message": {"role": "assistant", "content": "Test"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
    }
    mock_response.raise_for_status = Mock()

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch("requests.post", return_value=mock_response):
            manager = SubagentManager()
            orchestrator = SubagentOrchestrator(manager)
            tasks = [
                {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Task 1"}],
                },
                {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Task 2"}],
                },
            ]

            result = orchestrator.execute_parallel(tasks)

            # 验证摘要不包含 total_cost
            assert "summary" in result
            assert "total_tasks" in result["summary"]
            assert "total_input_tokens" in result["summary"]
            assert "total_output_tokens" in result["summary"]
            assert "total_tokens" in result["summary"]
            assert "total_cost" not in result["summary"]

            # 验证每个任务结果不包含 cost
            for task_result in result["results"]:
                if task_result["status"] == "success":
                    assert "cost" not in task_result


def test_custom_model_support():
    """测试支持自定义模型名称"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [{"message": {"role": "assistant", "content": "Custom model response"}}],
        "usage": {"prompt_tokens": 15, "completion_tokens": 25, "total_tokens": 40},
    }
    mock_response.raise_for_status = Mock()

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch("requests.post", return_value=mock_response):
            manager = SubagentManager()

            # 使用一个自定义模型名称
            result = manager.call_ai(
                provider="openai",
                model="custom-model-v1",
                messages=[{"role": "user", "content": "Test custom model"}],
            )

            # 应该能成功调用
            assert result["status"] == "success"
            assert result["model"] == "custom-model-v1"
            assert "cost" not in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
