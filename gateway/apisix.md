# APISIX快速开始

Cloud-native microservices API gateway, delivering the ultimate performance, security, open source and scalable platform for all your APIs and microservices.

Apache APISIX is based on Nginx and etcd. Compared with traditional API gateways, APISIX has dynamic routing and plug-in hot loading, which is especially suitable for API management under micro-service system.

![apisix-arc](/assets/apisix-arc.png)

## 安装

```sh
# Download the Docker image of Apache APISIX
git clone https://github.com/apache/apisix-docker.git
# Switch the current directory to the apisix-docker/example path
cd apisix-docker/example
# Run the docker-compose command to install Apache APISIX
docker-compose -p docker-apisix up -d

# Note: Please execute the curl command on the host where you are running Docker.
curl "http://127.0.0.1:9080/apisix/admin/services/" -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'

```

本地浏览器访问admin控制台：<http://172.22.46.73:9000/> 登录用户名密码都是admin

ETCD出现报错：cannot access data directory: mkdir /bitnami/etcd/data: permission denied，表示etcd启动时没有创建db的权限，在opt目录下执行：chmod -R 777 /opt/apps/

可能用到的命令：

```sh

# 停止指定容器
docker stop $(docker ps -qa)
# 删除全部容器
docker rm $(docker ps -qa)
# 删除指定容器
docker rmi   容器ID
# 通过docker-compose 启动容器（目录必须包含docker-compose.yml）
docker-compose up -d
# 查看所有镜像
docker images
# 查看容器日志
docker logs -f
# 进入到容器内部
docker exec -it 容器ID bash
```

## 创建一个路由

We can create a Route and connect it to an Upstream service(also known as the Upstream). When a Request arrives at Apache APISIX, Apache APISIX knows which Upstream the request should be forwarded to.

Because we have configured matching rules for the **Route object**, Apache APISIX can forward the request to the corresponding Upstream service.

```json
{
  "methods": ["GET"],
  "host": "example.com",
  "uri": "/services/users/*",
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "httpbin.org:80": 1
    }
  }
}
```

This routing configuration means that all matching inbound requests will be forwarded to the Upstream service httpbin.org:80 when they meet all the rules listed below:

- The HTTP method of the request is GET.
- The request header contains the host field, and its value is example.com.
- The request path matches /services/users/*,* means any subpath, for example /services/users/getAll?limit=10.

Once this route is created, we can access the Upstream service using the address exposed by Apache APISIX.

```sh
curl -i -X GET "http://{APISIX_BASE_URL}/services/users/getAll?limit=10" -H "Host: example.com"
```

This will be forwarded to <http://httpbin.org:80/services/users/getAll?limit=10> by Apache APISIX.

**创建一个 upstream:**

An Upstream can be created by simply executing the following command:

```sh
curl "http://127.0.0.1:9080/apisix/admin/upstreams/1" -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" -X PUT -d '
{
  "type": "roundrobin",
  "nodes": {
    "httpbin.org:80": 1
  }
}'

```

**绑定路由到upstream:**

```sh
curl "http://127.0.0.1:9080/apisix/admin/routes/1" -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" -X PUT -d '
{
  "uri": "/get",
  "host": "httpbin.org",
  "upstream_id": "1"
}'
```

**验证：**

```sh
curl -i -X GET "http://127.0.0.1:9080/get?foo1=bar1&foo2=bar2" -H "Host: httpbin.org"

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 370
Connection: keep-alive
Date: Thu, 26 Aug 2021 03:29:48 GMT
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Server: APISIX/2.6

{
  "args": {
    "foo1": "bar1",
    "foo2": "bar2"
  },
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.68.0",
    "X-Amzn-Trace-Id": "Root=1-61270aac-7689df6b2ecdeec66033afe4",
    "X-Forwarded-Host": "httpbin.org"
  },
  "origin": "172.18.0.1, 120.203.73.194",
  "url": "http://httpbin.org/get?foo1=bar1&foo2=bar2"
}

```

### 认证

Now we want only a specific user John to have access to this Upstream service, and we need to use Consumer and Plugin to implement authentication.

First, let's use **key-auth plugin** to create a Consumer John, we need to provide a specified key.

```sh
curl "http://127.0.0.1:9080/apisix/admin/consumers" -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" -X PUT -d '
{
  "username": "john",
  "plugins": {
    "key-auth": {
      "key": "key-of-john"
    }
  }
}'
```

Next, let's bind consumer (John) to the route, we just need to enable the key-auth plugin.

```sh
curl "http://127.0.0.1:9080/apisix/admin/routes/1" -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" -X PUT -d '
{
  "uri": "/get",
  "host": "httpbin.org",
  "plugins": {
    "key-auth": {}
  },
  "upstream_id": "1"
}'
```

Now when we access the route created in step 2, an Unauthorized Error will be triggered.

The correct way to access that route is to add a Header named apikey with the correct key, as shown in the code below:

```sh
curl -i -X GET http://127.0.0.1:9080/get -H "Host: httpbin.org" -H "apikey: key-of-john"
```

### 前缀路由

Now, suppose you want to add a prefix to a route (e.g. samplePrefix) and don't want to use the host header, then you can use the proxy-rewrite plugin to do so.

```sh
curl "http://127.0.0.1:9080/apisix/admin/routes/1" -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" -X PUT -d '
{
  "uri": "/samplePrefix/get",
  "plugins": {
    "proxy-rewrite": {
      "regex_uri": ["^/samplePrefix/get(.*)", "/get$1"]
    },
    "key-auth": {}
  },
  "upstream_id": "1"
}'
```

You can now use the following command to invoke the route:

```sh
curl -i -X GET "http://127.0.0.1:9080/samplePrefix/get?param1=foo&param2=bar" -H "apikey: key-of-john"
```
