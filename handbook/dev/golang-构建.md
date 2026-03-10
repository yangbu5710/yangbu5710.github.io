# Golang：构建

## 参考

- Golang 编程模式：`https://coolshell.cn/articles/21128.html`

## 交叉编译示例

```bash
# 构建 amd64 架构产物
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o covparse main.go

# 构建 arm64 架构产物
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o covparse main.go
```

