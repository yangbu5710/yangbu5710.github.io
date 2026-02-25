# 常用操作

## 数据同步
```shell
#本地数据同步
rsync -avzP --delete --size-only --exclude=".nexus" --chown=200:200 /artifactory-new/android/ /mnt/storage00/android/ 

#远程数据同步，预先配置好ssh免登录
rsync -av -e "ssh -p 22" --delete /mnt/nexus-data/* root@10.149.12.14:/mnt/nexus-data/
```

## 数据清理
```shell
#清理./android/.nexus目录下超过15天的数据
find ./android/ -path "./android/.nexus/**/*" -prune -o -mtime -14 -print
```

## 好用的shell工具
> [ghostty](https://github.com/ghostty-org/ghostty)  
> [starship](https://starship.rs/)，配置文件https://github.com/yangbu5710/dotfiles/blob/master/.config/starship.toml

