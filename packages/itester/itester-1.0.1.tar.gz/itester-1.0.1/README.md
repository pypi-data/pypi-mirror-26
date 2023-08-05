# itester

## 要求

- click
- requests

## 介绍

看了不少测试环境 py.test、nose、unittest 对于QA 来说，书写case 需要写代码，所以简单写了一个使用Excel 维护case 的工具

## 安装

```
pip install itester

or

make build
make install
```

## 使用命令

```
itester -c /path/testcase/ -m mail1@mail.com,mail2@mail.com -o /path/report/ -p http://url/auto/report/
```

## 原理

- 从excel中获取case
- 然后分别校验实际返回值和预计返回值的区别