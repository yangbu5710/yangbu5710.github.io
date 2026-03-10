# 代码工具：Claude Code 与 Qwen Code

## Claude Code

Claude Code 是 Anthropic 的代码工具，以纯命令行方式进行交互。

安装参考：`https://docs.litellm.ai/docs/proxy/quick_start`

```bash
pip install 'litellm[proxy]'
litellm --config your_config.yaml
```

### 坑点

很多公司使用自定义模型/网关调用模型，配置文件中直接写模型可能出现 404。实践中常见的做法是使用 OpenAI Compatible 的写法，例如 `openai/xxx`（如 `openai/gemini-2.5-pro`）。

参考：`https://docs.litellm.ai/docs/providers/openai_compatible`

### 参考

- 源码：`https://github.com/anthropics/claude-code`
- 文档：`https://docs.anthropic.com/zh-CN/docs/claude-code/overview`
- 示例配置：`handbook/ai/assets/litellm-config.yaml`

## Qwen Code

安装参考：`https://help.aliyun.com/zh/model-studio/qwen-code`

### 坑点

在使用 `gpt-5` 时，要求 `temperature` 最少为 1，但 Qwen Code 默认是 0。

Issue：`https://github.com/QwenLM/qwen-code/issues/224`

### 配置

将配置文件放到：`~/.qwen/settings.json`

示例：`handbook/ai/assets/qwen-settings.json`

### 参考

- 源码：`https://github.com/QwenLM/qwen-code/`
- 文档：`https://help.aliyun.com/zh/model-studio/qwen-code`

