# 目录
- claude code
- qwen code

## claude code
claude code是anthropic开发的代码工具，以纯命令行方式进行交互，对于某些👨🏻‍💻来说更平静。
[安装文档](https://docs.litellm.ai/docs/proxy/quick_start)
```shell
# 安装方式
pip install 'litellm[proxy]' #安装litellm提供claude code使用
litellm --config your_config.yaml #配置文件
```
> 📢坑点：很多公司都是使用自定义模型/网关的方式去调用模型，配置文件中直接写模型会出现404的问题。所以在使用模型的时候需要新增openai/xxx（openai/gemini-2.5-pro）[参考链接](https://docs.litellm.ai/docs/providers/openai_compatible)

### 参考文档
[源码地址](https://github.com/anthropics/claude-code)  
[api文档](https://docs.anthropic.com/zh-CN/docs/claude-code/overview)

## qwen code
安装方式参考[文档](https://help.aliyun.com/zh/model-studio/qwen-code?spm=5176.21213303.J_ZGek9Blx07Hclc3Ddt9dg.3.f9dc2f3dhM5fFF&scm=20140722.S_help@@%E6%96%87%E6%A1%A3@@2974721._.ID_help@@%E6%96%87%E6%A1%A3@@2974721-RL_qwencode-LOC_2024SPAllResult-OR_ser-PAR1_213e372617560329175553401e785e-V_4-PAR3_o-RE_new6-P0_1-P1_0)
> 📢坑点：在使用gpt-5的时候，要求temperature最少为1，但是qwen code默认是0，[issue](https://github.com/QwenLM/qwen-code/issues/224)  
> 将[解决方案配置文件](settings.json)放在~/.qwen/settings.json

### 参考文档
[源码地址](https://github.com/QwenLM/qwen-code/)  
[api文档](https://help.aliyun.com/zh/model-studio/qwen-code?spm=5176.21213303.J_ZGek9Blx07Hclc3Ddt9dg.3.f9dc2f3dhM5fFF&scm=20140722.S_help@@%E6%96%87%E6%A1%A3@@2974721._.ID_help@@%E6%96%87%E6%A1%A3@@2974721-RL_qwencode-LOC_2024SPAllResult-OR_ser-PAR1_213e372617560329175553401e785e-V_4-PAR3_o-RE_new6-P0_1-P1_0)
