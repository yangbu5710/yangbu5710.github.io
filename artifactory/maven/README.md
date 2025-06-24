# 目录

## maven相关操作
### 通过shell指令上传包
```shell
mvn deploy:deploy-file -Dmaven.test.skip=true -Dfile=/Users/yangbu/Desktop/ads-1.1.1.jar -DgroupId=${groupId} -DartifactId=${artifactId} -Dversion=${version} -Dpackaging=aar -DrepositoryId=shared-aar  -Durl=https://nexus.bilibili.co/content/repositories/shared-aar/ -DpomFile=/Users/yangbu/Desktop/pom.xml
```
