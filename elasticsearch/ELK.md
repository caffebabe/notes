- [安装](#安装)
- [Beats](#beats)
- [Logstash](#logstash)
  - [Filebeat to Logstash](#filebeat-to-logstash)

## 安装

Install the Elastic Stack products you want to use in the following order:

- Elasticsearch ([install instructions](https://www.elastic.co/guide/en/elasticsearch/reference/7.14/install-elasticsearch.html))
- Kibana ([install](https://www.elastic.co/guide/en/kibana/7.14/install.html))
- Logstash ([install](https://www.elastic.co/guide/en/logstash/7.14/installing-logstash.html))
- Beats ([install instructions](https://www.elastic.co/guide/en/beats/libbeat/7.14/getting-started.html))
- APM Server ([install instructions](https://www.elastic.co/guide/en/apm/server/7.14/installing.html))
- Elasticsearch Hadoop ([install instructions](https://www.elastic.co/guide/en/elasticsearch/hadoop/7.14/install.html))

## Beats

Beats are open source data shippers that you install as agents on your servers to send operational data to Elasticsearch.

Elastic provides Beats for capturing:

- Audit data：[Auditbeat](https://www.elastic.co/beats/auditbeat)
- Log files：[Filebeat](https://www.elastic.co/products/beats/filebeat)
- Cloud data： [Functionbeat](https://www.elastic.co/products/beats/functionbeat)
- Availability：[Heartbeat](https://www.elastic.co/products/beats/heartbeat)
- Systemd journals：[Journalbeat](https://www.elastic.co/downloads/beats/journalbeat)
- Metrics：[Metricbeat](https://www.elastic.co/products/beats/metricbeat)
- Network traffic：[Packetbeat](https://www.elastic.co/products/beats/packetbeat)
- Windows event logs：[Winlogbeat](https://www.elastic.co/products/beats/winlogbeat)

Beats can send data directly to Elasticsearch or via Logstash, where you can further process and enhance the data, before visualizing it in Kibana.

![beats-plateform](img/beats-platform.png)

Filebeat quick start：<https://www.elastic.co/guide/en/beats/filebeat/7.14/filebeat-installation-configuration.html>

## Logstash

A Logstash pipeline has two required elements, input and output, and one optional element, filter.

The input plugins consume data from a source, the filter plugins modify the data as you specify, and the output plugins write the data to a destination.

![logstash-pipeline](img/basic_logstash_pipeline.png)

示例：stdin和stdout

```sh
cd logstash-7.14.0
.\bin\logstash.bat -e "input { stdin { } } output { stdout {} }"
```

### Filebeat to Logstash

下载示例log文件：logstash-tutorial.log

配置 filebeat.yml

```yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - F:\elastic\logstash-tutorial-dataset

output.logstash:
  hosts: ["localhost:5044"]
```

启动filebeat：

```sh
 .\filebeat.exe -e -c filebeat.yml -d "publish"
```

配置 logstash：first-pipeline.conf

```ruby
input {
    beats {
        port => "5044"
    }
}

output {
    stdout { codec => rubydebug }
}
```

启动logstash:

```sh
bin/logstash.bat -f config/first-pipeline.conf --config.reload.automatic
```
