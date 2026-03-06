# 目录
- [Golang编程模式](https://coolshell.cn/articles/21128.html)
  
``` bash
# 构建amd64架构产物
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o covparse main.go
# 构建arm64架构产物
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o covparse main.go
```