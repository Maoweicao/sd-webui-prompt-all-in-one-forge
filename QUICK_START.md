# 快速开始指南

## 安装依赖

首先确保已安装 `openai` 包：

```bash
pip install openai
```

## 配置 AI 翻译平台

### 1. 使用 Deepseek

1. 访问 [Deepseek 官网](https://platform.deepseek.com/) 获取 API Key
2. 在扩展设置中配置：
   - **API Base:** `https://api.deepseek.com/v1`
   - **API Key:** 你的 Deepseek API Key
   - **Model:** `deepseek-chat` 或 `deepseek-reasoner`

### 2. 使用 CherryIn

1. 访问 [CherryIn 官网](https://open.cherryin.ai/) 获取 API Key
2. 在扩展设置中配置：
   - **API Base:** `https://open.cherryin.ai/v1`
   - **API Key:** 你的 CherryIn API Key
   - **Model:** 选择可用的模型（如 `gpt-4o-mini`）

### 3. 使用 SiliconFlow

1. 访问 [SiliconFlow 官网](https://siliconflow.cn/) 获取 API Key
2. 在扩展设置中配置：
   - **API Base:** `https://api.siliconflow.cn/v1`
   - **API Key:** 你的 SiliconFlow API Key
   - **Model:** 选择可用的模型（如 `Qwen/Qwen2.5-7B-Instruct`）

### 4. 使用自定义 OpenAI 兼容服务

1. 获取你的 API Base URL 和 API Key
2. 在扩展设置中配置：
   - **API Base:** 你的 API Base URL
   - **API Key:** 你的 API Key
   - **Model:** 你的模型名称

## 使用翻译功能

### 在 UI 中使用

1. 打开扩展的翻译面板
2. 选择翻译 API：选择新的 AI 平台（如 Deepseek、CherryIn 等）
3. 输入要翻译的文本
4. 点击翻译按钮

### 通过 API 使用

```bash
curl -X POST http://localhost:7860/physton_prompt/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, world!",
    "from_lang": "en_US",
    "to_lang": "zh_CN",
    "api": "deepseek",
    "api_config": {
      "translate_api.deepseek": {
        "api_base": "https://api.deepseek.com/v1",
        "api_key": "your-api-key",
        "model": "deepseek-chat"
      }
    }
  }'
```

## 使用 AI 生成功能

### 在 UI 中使用

1. 打开 ChatGPT 提示词生成面板
2. 配置 AI 平台（API Base、API Key、Model）
3. 输入图像描述
4. 点击生成按钮

### 通过 API 使用

```bash
curl -X POST http://localhost:7860/physton_prompt/gen_ai \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Generate a prompt for a beautiful landscape"}
    ],
    "api_config": {
      "api_base": "https://api.deepseek.com/v1",
      "api_key": "your-api-key",
      "model": "deepseek-chat"
    },
    "platform": "deepseek"
  }'
```

## 获取可用模型列表

```bash
curl -X POST http://localhost:7860/physton_prompt/get_ai_models \
  -H "Content-Type: application/json" \
  -d '{
    "api_base": "https://api.deepseek.com/v1",
    "api_key": "your-api-key"
  }'
```

## 常见问题

### Q: 如何选择合适的 AI 平台？

**A:** 根据以下因素选择：
- **成本：** SiliconFlow 通常最便宜
- **质量：** OpenAI 和 CherryIn 通常质量最好
- **速度：** Deepseek 通常速度较快
- **可用性：** 根据你的地区选择

### Q: 如何获取 API Key？

**A:** 
- **Deepseek:** https://platform.deepseek.com/
- **CherryIn:** https://open.cherryin.ai/
- **SiliconFlow:** https://siliconflow.cn/
- **OpenAI:** https://platform.openai.com/

### Q: 支持哪些语言？

**A:** 所有 AI 平台都支持以下主要语言：
- 中文（简体、繁体、香港）
- 英文（美国、英国）
- 日语、韩语、法语、德语、西班牙语、意大利语
- 葡萄牙语、俄语、阿拉伯语、泰语、越南语
- 以及 30+ 其他语言

### Q: 翻译结果会被缓存吗？

**A:** 是的，翻译结果会被缓存以提高性能。相同的文本不会被重复翻译。

### Q: 如何清除缓存？

**A:** 重启 Stable Diffusion WebUI 会清除缓存。

## 性能优化建议

1. **选择合适的模型：** 较小的模型速度更快，但质量可能较低
2. **使用批量翻译：** 一次翻译多个文本比逐个翻译更高效
3. **启用缓存：** 避免重复翻译相同的文本
4. **选择合适的并发数：** 根据 API 限制调整并发数

## 故障排除

### 问题：翻译失败，显示 "No module named 'openai'"

**解决方案：**
```bash
pip install openai
```

### 问题：翻译失败，显示 "API Key is required"

**解决方案：** 检查 API Key 是否正确配置

### 问题：翻译失败，显示 "API Base is required"

**解决方案：** 检查 API Base URL 是否正确配置

### 问题：翻译速度很慢

**解决方案：**
- 检查网络连接
- 选择更快的 AI 平台
- 选择更小的模型
- 检查 API 限制

### 问题：翻译结果不准确

**解决方案：**
- 选择更好的 AI 平台
- 选择更大的模型
- 检查输入文本是否正确

## 更多信息

- 详细文档：查看 `AI_TRANSLATION_REFACTOR.md`
- 重构总结：查看 `REFACTOR_SUMMARY.md`
- 源代码：查看 `scripts/physton_prompt/` 目录

## 反馈和支持

如有问题或建议，请在 GitHub 上提交 Issue 或 PR。
