# 网络搜索工具升级说明

## 更新内容

### 1. 添加 Bing 搜索支持

为了解决 DuckDuckGo 搜索可能遇到的速率限制和搜索结果不足的问题，我们添加了 Bing 搜索作为备选方案。

### 2. 智能故障转移机制

当 DuckDuckGo 搜索失败或返回空结果时，系统会自动切换到 Bing 搜索，确保搜索服务的可用性。

### 3. 改进的错误处理

新版本提供更详细的错误信息和搜索引擎使用情况反馈。

## 主要变更

### web_search 函数

**之前：**

- 仅支持 DuckDuckGo 搜索
- 遇到速率限制时直接失败
- 错误信息不够详细

**现在：**

- 优先使用 DuckDuckGo 搜索
- 自动降级到 Bing 搜索
- 返回使用的搜索引擎信息
- 提供详细的错误和警告信息

**返回格式：**

```json
{
  "results": [
    {
      "title": "搜索结果标题",
      "link": "https://example.com",
      "snippet": "搜索结果摘要"
    }
  ],
  "count": 10,
  "query": "搜索关键词",
  "search_engine": "DuckDuckGo" // 或 "Bing"
}
```

### web_search_news 函数

**之前：**

- 仅支持 DuckDuckGo News
- 遇到速率限制时直接失败

**现在：**

- 优先使用 DuckDuckGo News
- 自动降级到 Bing News
- 返回更详细的新闻信息

**返回格式：**

```json
{
  "results": [
    {
      "title": "新闻标题",
      "link": "https://news.example.com",
      "snippet": "新闻摘要",
      "date": "发布日期",
      "source": "新闻来源"
    }
  ],
  "count": 10,
  "query": "搜索关键词",
  "type": "news",
  "search_engine": "DuckDuckGo News" // 或 "Bing News"
}
```

## 技术实现

### 1. Bing RSS Feed

使用 Bing 的 RSS feed 格式来获取搜索结果：

- 普通搜索：`https://www.bing.com/search?q={query}&format=rss`
- 新闻搜索：`https://www.bing.com/news/search?q={query}&format=rss`

### 2. 辅助函数

新增 `_bing_search()` 辅助函数：

```python
def _bing_search(query: str, max_results: int = 10, is_news: bool = False) -> list[dict[str, Any]]:
    """Helper function to search using Bing (fallback option)."""
    # 使用 Bing RSS feed 获取搜索结果
    # 支持普通搜索和新闻搜索
    # 返回统一格式的结果列表
```

### 3. 搜索流程

```
        开始搜索
            ↓
        尝试 DuckDuckGo 搜索
            ↓
        成功？
    ↙ 是    ↘ 否
返回结果   尝试 Bing 搜索
               ↓
              成功？
            ↙ 是    ↘ 否
        返回结果  返回错误信息
```

## 优势

1. **提高可靠性**：双重搜索引擎保障
2. **更好的用户体验**：无需手动切换搜索引擎
3. **透明度**：明确告知使用了哪个搜索引擎
4. **容错性**：详细的错误信息帮助诊断问题

## 依赖项

无需额外依赖，继续使用现有的：

- `requests` - HTTP 请求
- `beautifulsoup4` - HTML/XML 解析
- `ddgs` - DuckDuckGo 搜索（可选，原 duckduckgo-search 已改名）
- `lxml` - XML 解析器

**注意**：如果你之前安装了 `duckduckgo-search`，请更新到 `ddgs`：

```bash
pip uninstall duckduckgo-search
pip install ddgs
```

## 使用示例

### Python 代码示例

```python
from mcp_server.tools.web import register_tools
import json

# 注册工具
class MCP:
    def tool(self):
        def decorator(func):
            return func
        return decorator

mcp = MCP()
register_tools(mcp)

# 使用 web_search
result = web_search("Python programming", max_results=5)
data = json.loads(result)

print(f"使用的搜索引擎: {data['search_engine']}")
for item in data['results']:
    print(f"- {item['title']}: {item['link']}")

# 使用 web_search_news
news_result = web_search_news("AI technology", max_results=5)
news_data = json.loads(news_result)

print(f"\n使用的搜索引擎: {news_data['search_engine']}")
for item in news_data['results']:
    print(f"- [{item['source']}] {item['title']}")
    print(f"  {item['date']}")
```

## 测试

运行测试脚本：

```bash
python test_search.py
```

这将测试：

1. 普通搜索功能
2. 新闻搜索功能
3. 故障转移机制
4. 错误处理

## 注意事项

1. **速率限制**：虽然添加了 Bing 备选，但频繁请求仍可能触发限制
2. **网络依赖**：需要稳定的网络连接
3. **结果差异**：不同搜索引擎返回的结果可能有差异
4. **性能**：故障转移会增加响应时间

## 兼容性

- ✅ 完全向后兼容
- ✅ 不影响现有代码
- ✅ 可选的 DuckDuckGo 依赖
- ✅ 无需配置即可使用

## 未来改进

- [ ] 添加其他搜索引擎支持（Google, Baidu 等）
- [ ] 实现智能缓存减少请求
- [ ] 添加搜索结果去重
- [ ] 支持高级搜索选项
- [ ] 实现请求限流保护
