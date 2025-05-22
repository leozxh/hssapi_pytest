# 接口自动化测试框架

## 项目概述

本项目是一个基于 `unittest` 的接口自动化测试框架，专为特定系统设计。它支持多环境配置、测试报告生成以及邮件通知等功能，旨在提高接口测试的效率和可维护性。

## 目录结构

```
├── common/                # 公共工具类和基础功能
│   ├── __init__.py
│   ├── common_utils.py      # 通用工具函数（数据生成、文件读写等）
│   ├── encryption_utils.py  # 加密相关工具（HMAC、AES加密等）
│   ├── httprequest.py       # HTTP请求封装（GET、POST方法）
│   └── myunit.py            # 测试基类（设置、清理方法等）
├── config/                # 配置文件
│   ├── __init__.py
│   └── config.py            # 环境配置（域名、报告配置等）
├── data/                  # 测试数据和资源文件
│   ├── __init__.py
│   ├── email_config.json    # 邮件配置
│   ├── env.ini              # 环境变量存储
│   ├── testcases.xlsx       # 测试用例数据
│   └── ~$testcases.xlsx     # Excel临时文件
├── reports/               # 测试报告输出目录
│   ├── history.json         # 历史报告记录
│   └── report.html          # 最新测试报告
├── run/                   # 运行脚本和启动器
│   ├── __init__.py
│   ├── run.py               # 主程序入口
│   ├── runner.py            # 测试执行器（运行测试并发送报告）
│   └── cli.py               # 命令行接口
├── testcases/             # 测试用例模块
│   ├── __init__.py
│   ├── get_account.py       # 获取账户信息测试
│   ├── get_aes_key.py       # 获取AES密钥测试
│   ├── hsslogin.py          # 登录功能测试
│   └── smart_business_order.py # 智能商单功能测试
├── .gitignore
└── README.md
```

## 主要模块说明

### common/ 公共工具模块
- **common_utils.py**: 提供通用工具函数，如随机数生成、时间处理、Excel数据读写等。
- **encryption_utils.py**: 实现 HMAC 和 AES 加密方法，用于接口安全认证。
- **httprequest.py**: 封装 GET 和 POST 请求方法，并提供认证请求头的构造功能。
- **myunit.py**: 测试基类，提供测试用例的基础设置和清理操作。

### config/ 配置模块
- **config.py**: 定义环境配置，包括域名、测试数据路径、报告配置等。

### data/ 数据模块
- **email_config.json**: 存储邮件服务器配置，用于测试报告的邮件发送。
- **env.ini**: 存储测试过程中需要的环境变量，如 token、用户 ID 等。
- **testcases.xlsx**: 测试用例数据源，包含不同接口的测试数据。

### testcases/ 测试用例模块
- **get_account.py**: 测试获取当前账户信息的功能。
- **hsslogin.py**: 测试登录功能，验证用户身份认证。
- **smart_business_order.py**: 测试智能商单相关的业务流程。

### run/ 执行模块
- **run.py**: 主程序入口，调用 runner.py 执行所有测试。
- **runner.py**: 测试执行器，负责加载测试用例、生成报告并发送邮件。

## 使用说明

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境**:
   修改 `data/env.ini` 和 `data/email_config.json` 文件，根据实际环境配置参数。

3. **运行测试**:
   ```bash
   python run/run.py
   ```

4. **查看报告**:
   测试完成后，报告会生成在 `reports/` 目录下，打开 `report.html` 查看详细结果。

## 注意事项

- 测试前请确保 `data/testcases.xlsx` 中的测试数据已正确填写。
- 如需扩展测试用例，请在 `testcases/` 目录下新增对应的测试文件，并在 `run/runner.py` 中加载相应的测试类。
- 报告模板可以通过修改 `config.py` 中的 `REPORT_CONFIG["template"]` 参数来切换。

## 依赖库

- `requests`: 用于发送 HTTP 请求。
- `openpyxl`: 用于读取 Excel 格式的测试数据。
- `unittest`: Python 内置的单元测试框架。
- `unittestreport`: 第三方库，用于生成 HTML 测试报告。
- `Crypto`: 用于 AES 加密解密操作。


## 关于 Git 上的目录结构

由于测试数据和报告文件通常包含敏感信息或动态生成的内容，因此它们不会上传到 Git 仓库中。以下是本地目录结构与 Git 上的区别：

- **data/**: 本地包含实际的测试数据文件（如 `testcases.xlsx`），而 Git 上可能只有示例文件或模板。
- **reports/**: 本地包含最新的测试报告文件（如 `report.html`），而 Git 上可能没有这些文件。
- **.gitignore**: 文件中列出了不上传到 Git 的文件和目录，包括 `data/testcases.xlsx` 和 `reports/`。

请确保在本地环境中正确配置这些文件，以确保测试能够正常运行。