# 接口自动化测试框架

## 项目概述

本项目是一个基于 `pytest` 的接口自动化测试框架，专为特定系统设计。它支持多环境配置、Allure 测试报告生成以及邮件通知等功能，旨在提高接口测试的效率和可维护性。

## 目录结构

```
├── common/                # 公共工具类和基础功能
│   ├── __init__.py
│   ├── common_utils.py      # 通用工具函数（数据生成、文件读写等）
│   ├── encryption_utils.py  # 加密相关工具（HMAC、AES加密等）
│   ├── email_utils.py       # 邮件发送工具
│   ├── httprequest.py       # HTTP请求封装（GET、POST方法）
├── config/                # 配置文件
│   ├── __init__.py
│   └── config.py            # 环境配置（域名、报告配置等）
├── data/                  # 测试数据和资源文件
│   ├── __init__.py
│   ├── email_config.json    # 邮件配置
│   ├── env.ini              # 环境变量存储
│   └── testcases.xlsx       # 测试用例数据
├── allure_output/         # Allure 原始数据和 HTML 报告输出目录
│   ├── data/                # Allure JSON 测试结果
│   └── html/                # 生成的 HTML 报告
├── run/                   # 运行脚本和启动器
│   ├── __init__.py
│   ├── run.py               # 主程序入口
│   ├── cli.py               # 可选命令行接口
│   └── custom_runner.py     # 自定义测试执行器
├── testcases/             # 测试用例模块
│   ├── __init__.py
│   ├── get_aes_key.py       # 获取AES密钥测试
│   ├── hsslogin.py          # 登录功能测试
│   └── smart_business_order.py # 智能商单功能测试
├── conftest.py             # pytest 全局 fixture
├── .gitignore
└── README.md
```

## 主要模块说明

### common/ 公共工具模块
- **common_utils.py**: 提供通用工具函数，如随机数生成、时间处理、Excel数据读写等。
- **encryption_utils.py**: 实现 HMAC 和 AES 加密方法，用于接口安全认证。
- **email_utils.py**: 封装邮件发送逻辑，支持打包并发送完整测试报告。
- **httprequest.py**: 封装 GET 和 POST 请求方法，并提供认证请求头的构造功能。

### config/ 配置模块
- **config.py**: 定义环境配置，包括域名、测试数据路径、报告配置等。

### data/ 数据模块
- **email_config.json**: 存储邮件服务器配置，用于测试报告的邮件发送。
- **env.ini**: 存储测试过程中需要的环境变量，如 token、用户 ID 等。
- **testcases.xlsx**: 测试用例数据源，包含不同接口的测试数据。

### testcases/ 测试用例模块
- **hsslogin.py**: 使用 pytest 编写的登录功能测试用例。
- **smart_business_order.py**: 智能商单相关的 pytest 测试用例。
- **get_aes_key.py**: 获取 AES 密钥的测试用例。

### run/ 执行模块
- **custom_runner.py**: 自定义测试执行器，负责加载 pytest 测试用例、生成 Allure 报告。
- **cli.py**: 命令行入口，支持参数控制（如 --no-email 跳过邮件发送）
### allure_output/
- **data/**: 存放 pytest 生成的 Allure 原始测试数据（JSON 格式）。
- **html/**: 存放通过 allure generate 生成的 HTML 报告。

### allure_output/
- **data/**: 存放 pytest 生成的 Allure 原始测试数据（JSON 格式）。
- **html/**: 存放通过 allure generate 生成的 HTML 报告。

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
   或使用 pytest 命令直接运行指定测试文件：
   ```bash
   pytest testcases/hsslogin.py -v --alluredir=allure_output/data
   allure serve allure_output/data
   ```

4. **查看报告**:
   测试完成后，报告会生成在 `allure_output/html/` 目录下，打开 `index.html` 查看详细结果。

## 注意事项

- 测试前请确保 `data/testcases.xlsx` 中的测试数据已正确填写。
- 如需扩展测试用例，请在 `testcases/` 目录下新增对应的测试文件，并在 `run/custom_runner.py` 中指定测试目录。
- Allure 报告可通过本地服务预览：`allure serve allure_output/data`

## 依赖库

- `pytest`: 强大的 Python 单元测试框架。
- `allure-pytest`: 用于生成 Allure 测试报告。
- `requests`: 用于发送 HTTP 请求。
- `openpyxl`: 用于读取 Excel 格式的测试数据。
- `Crypto`: 用于 AES 加密解密操作。

## 关于 Git 上的目录结构

由于测试数据和报告文件通常包含敏感信息或动态生成的内容，因此它们不会上传到 Git 仓库中。以下是本地目录结构与 Git 上的区别：

- **data/**: 本地包含实际的测试数据文件（如 `testcases.xlsx`），而 Git 上可能只有示例文件或模板。
- **allure_output/**: 本地包含最新的 Allure 测试报告文件，而 Git 上可能没有这些文件。
- **.gitignore**: 文件中列出了不上传到 Git 的文件和目录，包括 `data/testcases.xlsx`、`allure_output/` 和 `reports/`。

请确保在本地环境中正确配置这些文件，以确保测试能够正常运行。