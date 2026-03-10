# Maven：上传制品

## 通过命令行上传制品（deploy-file）

```bash
mvn deploy:deploy-file \
  -Dmaven.test.skip=true \
  -Dfile=/Users/yangbu/Desktop/ads-1.1.1.jar \
  -DgroupId=${groupId} \
  -DartifactId=${artifactId} \
  -Dversion=${version} \
  -Dpackaging=aar \
  -DrepositoryId=shared-aar \
  -Durl=https://nexus.bilibili.co/content/repositories/shared-aar/ \
  -DpomFile=/Users/yangbu/Desktop/pom.xml
```

