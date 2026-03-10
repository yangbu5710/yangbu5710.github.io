# 知识库目录

本仓库沉淀日常开发/运维/AI 相关的笔记与资料索引。主要内容已逐步整理到 [Handbook](./handbook/)。

## 目录
- [handbook](./handbook/)（推荐入口）
- [ai](./ai)
  - [mcp](./ai/mcp/)
  - [model](./ai/model/)
  - [prompt](./ai/prompt/) 
    - [code_review](./ai/prompt/code_review/)
  - [code](./ai/code/)
- [linux指令操作](./linux) 
- [dev](./dev) 
  - [golang](./dev/golang/) 
  - [java](./dev/java/) 
- [git](./git)
- [artifactory](./artifactory/)
- [container](./container/)
- [sonarqube](./sonarqube/)
  - [升级](./sonarqube/upgrade/)

## 维护

- 生成 `handbook` 索引：`python3 scripts/handbook.py gen`
- 校验 Markdown 链接：`python3 scripts/handbook.py check --path .`
