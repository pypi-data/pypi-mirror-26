# BUPTLoginByPython3

北邮网关登陆程序，Python3版本
> windows环境下且无python可以使用 [windows版本](https://github.com/zwk19023393/BUPTNetLoginByWPF)

## 安装
支持pip一键安装，输入：
```html
    pip install BUPTLogin
```

## 使用方法
- 带参数运行
命令格式如下：
```html
    bupt.login [校园网账户] [密码]
```

- 不带参数运行
直接输入
```html
    bupt.login
```
如果为第一次登陆将会提示输入账户密码

- 更新
```html
    pip install BUPTLogin --upgrade
```

## 注意事项
- 第一次登陆成功后将自动保存账户密码，下一次登陆不需要输入参数。若需要切换账户，直接带参数运行即可
- 仅在Python3版本测试通过，Python2运行情况未知

## 依赖库
无需自己安装，pip将自动安装
- BeautifulSoup4
- lxml

> 更多请前往 [个人博客](http://www.ingbyr.com)
