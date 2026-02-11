# Subagent 持久化配置更新说明

## 📋 更新概述

为 Subagent AI 编排系统添加了完整的持久化配置管理功能，解决了每次启动都需要重新设置 API 密钥的问题。

## ✨ 新增功能

### 1. 配置管理类 (SubagentConfig)

新增 `subagent_config.py` 模块，提供:

- **持久化存储**: 配置自动保存到 `~/.subagent_config.json`
- **优先级系统**: 环境变量 > 配置文件 > 默认值
- **安全保护**: Unix/Linux/macOS 自动设置文件权限为 600
- **数据脱敏**: 所有密钥显示自动脱敏
- **多项目支持**: 可指定自定义配置文件路径

### 2. 三个新 MCP 工具

#### `subagent_config_set`

保存 API 密钥和端点到配置文件

```python
subagent_config_set("openai", "sk-proj-xxxxxxxxxxxx")
subagent_config_set("openai", "sk-xxx", "https://custom-api.com/v1")
```

#### `subagent_config_get`

查询指定提供商的配置（密钥已脱敏）

```python
config = subagent_config_get("openai")
# Returns: {"provider": "openai", "api_key": "sk-proj-...xxxx", ...}
```

#### `subagent_config_list`

列出所有已配置的提供商

```python
providers = subagent_config_list()
# Returns: {"providers": {...}, "total_configured": 3, ...}
```

### 3. 集成更新

所有 AI 客户端类已更新以使用配置管理器:

- `OpenAIClient`
- `AnthropicClient`
- `ZhipuAIClient`

优先级逻辑:

1. 环境变量（最高优先级）
2. 配置文件
3. 默认 API 端点

## 📚 新文档

### `docs/SUBAGENT_CONFIG.md` - 完整配置指南

- 配置文件位置和格式
- 配置优先级说明
- 6 个工具的详细用法
- 8 个实用示例
- 安全最佳实践
- 常见问题解答

### `examples/subagent_config_example.py` - 示例代码

- 8 个完整示例演示所有配置功能
- 包含集成测试和优先级演示

## 🔄 更新内容

### 代码更新

**新文件:**

- `src/mcp_server/tools/subagent_config.py` (292 行)
- `docs/SUBAGENT_CONFIG.md` (359 行)
- `examples/subagent_config_example.py` (422 行)

**修改文件:**

- `src/mcp_server/tools/subagent.py` - 添加配置管理器集成和 3 个新 MCP 工具
- `docs/SUBAGENT_GUIDE.md` - 添加持久化配置说明
- `README.md` - 更新工具数量和配置说明
- `CHANGELOG.md` - 添加版本 0.1.1 更新日志

### 工具数量更新

- Subagent 工具: 3 → **6**
- 总工具数: 74+ → **77+**

## ✅ 测试验证

所有功能已经过完整测试:

1. ✅ 配置保存和读取
2. ✅ 环境变量优先级
3. ✅ 多提供商管理
4. ✅ 自定义配置文件路径
5. ✅ 配置导出和脱敏
6. ✅ 与 AI 客户端集成
7. ✅ MCP 服务器加载
8. ✅ 示例代码运行

## 🚀 使用方式

### 方式 1: 持久化配置（推荐）

```python
# 一次配置，永久生效
subagent_config_set("openai", "sk-proj-xxxxxxxxxxxx")
subagent_config_set("zhipuai", "your-api-key.xxxxxxxxxx")

# 查看配置
subagent_config_list()

# 使用配置的密钥
subagent_call(provider="openai", model="gpt-4", messages=...)
```

### 方式 2: 环境变量（临时）

```bash
export OPENAI_API_KEY="sk-..."
export ZHIPUAI_API_KEY="your-key"
```

### 方式 3: 混合使用

```python
# 配置文件中设置常用密钥
subagent_config_set("openai", "sk-personal-key")

# 临时使用环境变量覆盖
export OPENAI_API_KEY="sk-work-key"  # 自动优先使用此密钥
```

## 🔒 安全特性

1. **文件权限**: Unix/Linux/macOS 自动设置为 600（仅所有者可读写）
2. **数据脱敏**: 所有查询和日志中的密钥自动脱敏
3. **配置隔离**: 支持不同项目使用不同配置文件
4. **环境变量优先**: CI/CD 中可用环境变量覆盖配置文件

## 📖 相关文档

- [Subagent 使用指南](docs/SUBAGENT_GUIDE.md)
- [配置管理指南](docs/SUBAGENT_CONFIG.md)
- [ZhipuAI 集成指南](docs/ZHIPUAI_GUIDE.md)

## 🎯 优势

1. **便捷性**: 一次配置，永久生效
2. **安全性**: 自动文件权限和数据脱敏
3. **灵活性**: 支持环境变量覆盖和多项目配置
4. **透明性**: 清晰显示配置来源和状态
5. **兼容性**: 完全向后兼容，现有用户无需修改代码

---

**版本**: 0.1.1  
**日期**: 2026-02-11  
**状态**: ✅ 已测试，生产就绪
