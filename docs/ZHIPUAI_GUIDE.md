# ZhipuAI (智谱AI) 集成使用指南

## 简介

Subagent MCP 现已支持智谱AI的 GLM 系列模型，包括 GLM-4、GLM-4-Plus、GLM-4-Air 等。智谱AI 是国内领先的大语言模型提供商，特别擅长中文理解和生成。

## 快速开始

### 1. 获取 API 密钥

访问 [智谱AI 开放平台](https://open.bigmodel.cn/) 注册并获取 API 密钥。

### 2. 配置环境变量

```bash
# Linux/macOS
export ZHIPUAI_API_KEY="your-api-key.xxxx"

# Windows PowerShell
$env:ZHIPUAI_API_KEY = "your-api-key.xxxx"
```

### 3. 使用工具

在 MCP 客户端（如 Claude Desktop）中调用：

```python
import json

messages = [{"role": "user", "content": "请用一句话介绍人工智能"}]

result = subagent_call(
    provider="zhipuai",
    model="glm-4",
    messages=json.dumps(messages),
    max_tokens=100
)
```

## 支持的模型

| 模型          | 价格     | 上下文 | 说明                   |
| ------------- | -------- | ------ | ---------------------- |
| `glm-4-flash` | 免费     | 128K   | 免费试用，适合开发测试 |
| `glm-4-air`   | ¥0.01/1K | 128K   | 最经济，适合大批量处理 |
| `glm-4`       | ¥0.1/1K  | 128K   | 性能与成本平衡         |
| `glm-4-airx`  | ¥0.1/1K  | 8K     | 快速响应               |
| `glm-4-plus`  | ¥0.5/1K  | 128K   | 最强性能，复杂任务     |

## 使用示例

### 示例 1: 基础问答

```python
messages = [
    {"role": "system", "content": "你是一个有帮助的AI助手"},
    {"role": "user", "content": "解释什么是量子计算"}
]

result = subagent_call(
    provider="zhipuai",
    model="glm-4",
    messages=json.dumps(messages),
    max_tokens=500,
    temperature=0.7
)

# 返回：
# {
#   "result": "量子计算是...",
#   "usage": {"prompt_tokens": 20, "completion_tokens": 100, ...},
#   "cost": {"total_cost": 0.001716},
#   "model": "glm-4",
#   "provider": "zhipuai",
#   "status": "success"
# }
```

### 示例 2: 中文文本处理

```python
document = """
人工智能正在改变世界。机器学习算法使计算机能够从数据中学习。
深度学习是机器学习的一个子集，使用多层神经网络。
"""

tasks = [
    {
        "name": "summarize",
        "provider": "zhipuai",
        "model": "glm-4",
        "messages": [{"role": "user", "content": f"总结这段文字：{document}"}],
        "max_tokens": 100
    },
    {
        "name": "extract_keywords",
        "provider": "zhipuai",
        "model": "glm-4-air",  # 使用更便宜的模型
        "messages": [{"role": "user", "content": f"提取关键词：{document}"}],
        "max_tokens": 50
    }
]

result = subagent_parallel(
    tasks=json.dumps(tasks),
    max_workers=2
)

# 返回包含两个任务结果和总成本
```

### 示例 3: 混合使用多个提供商

利用不同提供商的优势：

```python
tasks = [
    {
        "name": "chinese_analysis",
        "provider": "zhipuai",
        "model": "glm-4",
        "messages": [{"role": "user", "content": "分析这段中文文本的情感..."}]
    },
    {
        "name": "english_translation",
        "provider": "openai",
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Translate to English..."}]
    },
    {
        "name": "summary",
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "messages": [{"role": "user", "content": "Summarize..."}]
    }
]

result = subagent_parallel(tasks=json.dumps(tasks), max_workers=3)

# 同时使用三个不同的 AI 提供商并行处理
```

### 示例 4: 成本优化策略

根据任务复杂度选择合适的模型：

```python
# 简单任务使用免费的 glm-4-flash
simple_task = {
    "provider": "zhipuai",
    "model": "glm-4-flash",
    "messages": [{"role": "user", "content": "今天天气怎么样？"}]
}

# 复杂任务使用 glm-4-plus
complex_task = {
    "provider": "zhipuai",
    "model": "glm-4-plus",
    "messages": [{"role": "user", "content": "详细分析这个商业计划..."}]
}

# 使用条件分支自动选择模型
condition_task = {
    "provider": "zhipuai",
    "model": "glm-4",
    "messages": [{
        "role": "user",
        "content": "这个问题是否需要深入分析？回答 true 或 false"
    }]
}

result = subagent_conditional(
    condition_task=json.dumps(condition_task),
    true_task=json.dumps(complex_task),
    false_task=json.dumps(simple_task)
)
```

## 成本计算

所有调用都会返回详细的成本信息：

```python
result = subagent_call(
    provider="zhipuai",
    model="glm-4",
    messages=json.dumps(messages)
)

cost = result["cost"]
# {
#   "input_cost": 0.000143,   # 输入成本 (USD)
#   "output_cost": 0.000286,  # 输出成本 (USD)
#   "total_cost": 0.000429    # 总成本 (USD)
# }
```

**注意**：智谱AI 官方以人民币计价，系统按 1 USD ≈ 7 CNY 换算显示。

## 自定义 API 端点

如果使用私有部署或其他端点：

```bash
export ZHIPUAI_API_BASE="https://your-custom-endpoint.com/api/paas/v4"
```

## 常见问题

### Q: 如何获取 API 密钥？

A: 访问 https://open.bigmodel.cn/ 注册账号并在控制台创建 API 密钥。

### Q: glm-4-flash 是真的免费吗？

A: 是的，glm-4-flash 提供免费调用，适合开发和测试。

### Q: 哪个模型最适合中文任务？

A: 所有 GLM-4 系列模型都针对中文优化。对于一般任务推荐 `glm-4`，复杂任务推荐 `glm-4-plus`。

### Q: 可以和其他提供商混用吗？

A: 可以！使用 `subagent_parallel` 可以同时调用 OpenAI、Anthropic 和 ZhipuAI。

### Q: API 调用限制是什么？

A: 速率限制取决于您的智谱AI账户等级，详见官方文档。

## 最佳实践

1. **选择合适的模型**
   - 开发测试：使用 `glm-4-flash`（免费）
   - 日常任务：使用 `glm-4` 或 `glm-4-air`
   - 关键任务：使用 `glm-4-plus`

2. **中文优先**
   - GLM 模型在中文理解上表现优异，中文任务优先考虑 ZhipuAI

3. **成本控制**
   - 设置合理的 `max_tokens` 限制
   - 使用免费的 glm-4-flash 进行原型开发
   - 批量任务使用 glm-4-air

4. **并行处理**
   - 利用 `subagent_parallel` 提高处理效率
   - 混合使用不同提供商发挥各自优势

## 更多资源

- [智谱AI 官网](https://open.bigmodel.cn/)
- [API 文档](https://open.bigmodel.cn/dev/api)
- [Subagent 完整指南](SUBAGENT_GUIDE.md)

---

**示例测试结果**：

```
测试 ZhipuAI API 调用...
状态: success
结果: 人工智能是让机器模拟人类智能，以实现学习、推理、解决问题和创造等复杂任务的技术。
Token 使用: {'prompt_tokens': 14, 'completion_tokens': 23, 'total_tokens': 37}
成本: $0.000529
耗时: 0.73秒

✅ ZhipuAI 集成测试完成!
```
