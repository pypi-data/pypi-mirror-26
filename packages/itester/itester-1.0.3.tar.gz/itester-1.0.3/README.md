# itester

## 依赖

- xlrd
- click
- requests

## 介绍

看了不少测试框架 py.test、nose、unittest， 书写case 都需要写代码，所以简单写了一个 Excel 驱动的接口自动化框架。

开发过程中考虑了使用jenkins 调用的情况，输出的日志会有彩色标识

## 安装

```
pip install itester
```

or

```
make build
make install
```

## 使用

### 查看帮助

```
itester --help
```

```
Usage: itester.py [OPTIONS]

  Excel - driven interface automation framework

Options:
  -c, --casepath TEXT    case路径，默认当前路径
  -m, --mailto TEXT      收件人列表，使用逗号分割
  -o, --outputpath TEXT  测试报告输出路径，默认当前路径
  -p, --prefix TEXT      邮件内容中的url的前缀, 如不输入发送附件
  --help                 Show this message and exit.
```

### 运行测试

建议在-o 的路径上增加nginx 的配置，配合使用-p 参数，发送的邮件中变只发一个访问的url

```
itester -c /path/testcase/ -m mail1@mail.com,mail2@mail.com -o /path/report/ -p http://url/auto/report/

or

itester -c /path/testcase/ -m mail1@mail.com,mail2@mail.com -o /path/report/
```

## 原理

- 从excel中获取case
- 然后分别校验实际返回值和预计返回值的区别

## 模板

在testcase 文件夹中获取，excel中基本都有注释