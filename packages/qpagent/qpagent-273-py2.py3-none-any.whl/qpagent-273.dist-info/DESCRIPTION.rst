# 质量平台本地Agent

## 简介
用户在PC或Mac上安装好agent后，通过在终端运行utagent命令启动代理服务，服务启动后会向质量平台注册本地的ip、port、挂载的设备等信息；

本地agent会接收来自质量平台发来的请求，执行对应的本地任务。

## 支持任务类型
1、启动Macaca server

2、初始化测试工程

3、Macaca脚本录制

4、Macaca脚本回放

5、获得测试报告和单步截图

## 使用方法
(venv) ➜  test utagent

     A Terminal Tools For slave Agent

Please enter a path [.]: /Users/mafei/UITest

Please enter a environment [alpha]: alpha

Bottle v0.12.13 server starting up (using WSGIRefServer())...

Listening on http://:9096/

Hit Ctrl-C to quit.



(venv) ➜  test utagent --help

     A Terminal Tools For slave Agent

Usage: utagent [OPTIONS]

Options:

  -v, --version

  --help         Show this message and exit.


(venv) ➜  ui utagent -v

     A Terminal Tools For slave Agent

Version: 0.0.31


