# itester

## 依赖

- xlrd
- nose
- click
- requests

## 介绍

看了不少测试框架 py.test、nose、unittest， 书写case 都需要写代码，所以简单写了一个 Excel 驱动的接口自动化框架。

开发过程中考虑了使用jenkins 调用的情况，输出的日志会有彩色标识


## 更新LOG

- [1.0.5] : 1、更新中文处理方式 2、更新Mac 下-s 参数 3、增加casepath 从环境变量ITESTER_CASE_PATH中获取

## TODO

- Excel 中增加setup SQL/teardown SQL

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
Usage: itester [OPTIONS]

  Excel - driven interface automation framework

Options:
  -c, --casepath TEXT    case路径，默认当前路径
  -m, --mailto TEXT      收件人列表，使用逗号分割
  -o, --outputpath TEXT  测试报告输出路径，默认当前路径
  -p, --prefix TEXT      邮件内容中的url的前缀, 如不输入发送附件
  --help                 Show this message and exit.
```

### 运行测试

#### itester 运行方式
建议在-o 的路径上增加nginx 的配置，配合使用-p 参数，发送的邮件中变只发一个访问的url

```
itester -c /path/testcase/ -m mail1@mail.com,mail2@mail.com -o /path/report/ -p http://url/auto/report/

or

itester -c /path/testcase/ -m mail1@mail.com,mail2@mail.com -o /path/report/
```

#### nosetests 的运行方式

```
export ITESTER_CASE_PATH="/path/excel_autotest/"; cd /path/itester/itester; nosetests -s -v test_main.py --with-html --html-report=/path/result/test_report.html
```

## 原理

- 从excel中获取case
- 然后分别校验实际返回值和预计返回值的区别

## 模板

在testcase 文件夹中获取，excel中基本都有注释