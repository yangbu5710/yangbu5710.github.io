# 目录
> - 升级路由
> - 升级文档
> - docker-compose文件
  
# 升级路由
社区版升级路由：https://frolicking-brigadeiros-1cba5a.netlify.app/

# 升级文档
升级核心就是数据库和插件，这里主要介绍数据库，插件只用拷贝到指定目录，一般也不会太大
```shell
# 创建网络
docker network create sonarqube-9lta
# 导出postgresql数据
docker exec -it postgres bash
cd /var/lib/postgresql/data/
pg_dump -U sonar sonar > sonar.sql
# 进入到新的目录，启动新的postgresql
docker-compose up -d
# 将sonar.sql拷贝到新服务器，执行同步指令
docker exec -it new-sonarqube-postgres bash
cd /var/lib/postgresql/data/
psql -U sonar -d sonar -f sonar.sql | tee out.log
# 启动新的sonarqube 实例,第一次可能文件夹没权限，chmod 之后，再启动一次
docker-compose -f docker-compose-sonar.yaml up -d
```

# docker-compse文件
docker-compose-psql.yml
```yaml 
version: "3"
services:
  db:
    image: hub.bilibili.co/nyx-base/postgres:16.4
    shm_size: '4g'
    container_name: postgres_9lta
    ports:
      - "25432:5432"
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
    volumes:
      - ./postgresql_data:/var/lib/postgresql/data
      - ./psql_bak:/var/lib/postgresql/data_bak
    networks:
      - sonar9lta
networks:
  sonar9lta:
    external:
      name: sonarqube-9lta
```
docker-compose-sonar.yaml
```yaml
version: "3"
services:
  sonarqube-9lta:
    container_name: sonarqube-9lta
    image: sonar-9.9lta:v1.2
    restart: always
    privileged: true
    #entrypoint: ["sleep", "infinity"]
    environment:
      - SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonar
      - SONAR_JDBC_USERNAME=sonar
      - SONAR_JDBC_PASSWORD=sonar
      - SONAR_WEB_JAVAOPTS=-Xmx8192m
      - SONAR_CE_JAVAOPTS=-Xmx8192m
      - SONAR_WEB_JAVAADDITIONALOPTS=-javaagent:./extensions/plugins/sonarqube-community-branch-plugin-1.14.0.jar=web
      - SONAR_CE_JAVAADDITIONALOPTS=-javaagent:./extensions/plugins/sonarqube-community-branch-plugin-1.14.0.jar=ce
    ports:
      - "9909:9000"
      - "9999:9002"
    volumes:
      - ./extensions:/opt/sonarqube/extensions:rw
      - ./conf:/opt/sonarqube/conf:rw
      - ./logs:/opt/sonarqube/logs:rw
      - ./data:/opt/sonarqube/data:rw
    networks:
      - sonar9lta
networks:
  sonar9lta:
    external:
      name: sonarqube-9lta
```