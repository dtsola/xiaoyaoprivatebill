# 小遥账单助手 - 项目开发规范

> **文档版本**: v1.0
> **创建日期**: 2026-02-17
> **项目类型**: 前后端分离重构项目

---

## 目录

1. [项目概述](#1-项目概述)
2. [技术选型](#2-技术选型)
3. [代码规范](#3-代码规范)
4. [Git 规范](#4-git-规范)
5. [测试规范](#5-测试规范)
6. [部署规范](#6-部署规范)
7. [设计文档引用](#7-设计文档引用)
8. [开发约定](#8-开发约定)
9. [架构决策记录](#9-架构决策记录)

---

## 1. 项目概述

### 1.1 产品定位

小遥账单助手是一个**隐私优先**的个人账单分析工具，支持支付宝和微信账单的自动解析和多维度数据可视化分析。

**核心特点**：
- 数据完全本地处理，不上传任何服务器
- 支持支付宝 CSV 和微信 CSV/XLSX 账单文件
- 多维度分析：年度、月度、分类、时间、消费洞察
- 前后端分离架构

### 1.2 项目结构

```
xiaoyaoprivatebill/
├── backend/               # 后端项目（Flask + Pandas）
│   ├── api/              # API 路由层
│   ├── services/         # 业务逻辑层
│   ├── parsers/          # 文件解析模块
│   ├── utils/            # 工具函数
│   ├── data/             # 临时数据目录
│   ├── app.py            # 应用入口
│   ├── config.py         # 配置管理
│   └── requirements.txt  # Python 依赖
│
├── frontend/             # 前端项目（Vue 3 + Vite）
│   ├── src/
│   │   ├── api/         # API 客户端
│   │   ├── views/       # 页面组件
│   │   ├── components/  # 公共组件
│   │   ├── stores/      # 状态管理（Pinia）
│   │   └── utils/       # 工具函数
│   ├── package.json
│   └── vite.config.js
│
├── docs/                 # 设计文档目录
│   ├── base/            # 基础模板文档
│   ├── 00-mrd.md        # 市场需求文档
│   ├── 01-prd.md        # 产品需求文档
│   ├── 接口文档.md      # API 接口文档
│   └── 项目提示词.md    # 项目提示词
│
└── CLAUDE.md            # 本文档（项目开发规范）
```

### 1.3 开发阶段

当前项目处于**前后端分离重构**阶段：

- **后端**：已从单体 `app.py`（3500+ 行）重构为模块化架构
- **前端**：从原生 JavaScript + Jinja2 模板迁移到 Vue 3 + Vite
- **API**：保持现有 API 接口完全兼容

---

## 2. 技术选型

### 2.1 后端技术栈

| 技术 | 版本 | 说明 | 选择理由 |
|------|------|------|---------|
| **Python** | 3.10+ | 后端开发语言 | 成熟稳定，数据处理能力强 |
| **Flask** | 2.0+ | Web 框架 | 轻量级，灵活，适合小型项目 |
| **Pandas** | Latest | 数据处理核心 | 强大的数据分析和处理能力 |
| **NumPy** | Latest | 数值计算 | 高效的数值运算 |
| **OpenPyXL** | Latest | Excel 文件处理 | 支持 .xlsx 格式读取 |

### 2.2 前端技术栈

| 技术 | 版本 | 说明 | 选择理由 |
|------|------|------|---------|
| **Vue** | 3.4+ | 前端框架 | 渐进式框架，易上手 |
| **Vite** | 5.0+ | 构建工具 | 快速的开发服务器和构建 |
| **Vue Router** | 4.2+ | 路由管理 | 官方路由解决方案 |
| **Pinia** | 2.1+ | 状态管理 | Vue 3 官方推荐的状态管理 |
| **ECharts** | 5.4.3 | 数据可视化 | 复用现有图表库 |
| **Fetch API** | - | HTTP 客户端 | 原生 API，无需额外依赖 |

### 2.3 开发工具

| 工具 | 用途 |
|------|------|
| **Python 虚拟环境** | `py -3.10 -m venv venv` |
| **npm/pnpm** | 前端包管理 |
| **Git** | 版本控制 |

### 2.4 环境要求

- **Python**: 3.10.11+
- **Node.js**: 18+ （推荐使用 LTS 版本）
- **操作系统**: Windows 11 / macOS / Linux

---

## 3. 代码规范

### 3.1 通用规范

#### 3.1.1 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| **文件名** | 小写字母，单词间用下划线分隔 | `data_service.py` |
| **类名** | PascalCase（大驼峰） | `DataService` |
| **函数名** | snake_case（小写+下划线） | `get_yearly_analysis` |
| **变量名** | snake_case | `user_id` |
| **常量名** | UPPER_SNAKE_CASE | `MAX_UPLOAD_SIZE` |
| **私有成员** | 前缀下划线 | `_internal_method` |

#### 3.1.2 注释规范

**Python 代码**：
```python
def get_yearly_analysis(year: int) -> dict:
    """
    获取年度分析数据

    Args:
        year: 年份，如 2024

    Returns:
        包含年度收支汇总的字典

    Raises:
        ValueError: 当年份参数无效时
    """
    # 实现逻辑...
```

**JavaScript/Vue 代码**：
```javascript
/**
 * 获取年度分析数据
 * @param {number} year - 年份，如 2024
 * @returns {Promise<Object>} 年度收支汇总数据
 * @throws {Error} 当年份参数无效时
 */
async function getYearlyAnalysis(year) {
    // 实现逻辑...
}
```

### 3.2 Python 代码规范

遵循 **PEP 8** 规范，建议使用 `black` 进行代码格式化：

```bash
# 安装 black
pip install black

# 格式化代码
black backend/
```

**关键规范**：
- 每行代码不超过 88 字符
- 使用 4 空格缩进
- 函数之间空 2 行
- 类之间空 3 行

### 3.3 JavaScript/Vue 代码规范

遵循 **ESLint** 推荐规范：

```bash
# 安装 ESLint
npm install -D eslint

# 检查代码
npm run lint
```

**关键规范**：
- 使用 const/let，避免 var
- 优先使用箭头函数
- 组件名使用 PascalCase
- 模板文件使用 kebab-case

### 3.4 类型注解

**Python 类型注解**：
```python
from typing import Dict, List, Optional

def parse_transactions(data: List[Dict]) -> Optional[pd.DataFrame]:
    """解析交易数据"""
    ...
```

**JavaScript JSDoc**：
```javascript
/**
 * @typedef {Object} Transaction
 * @property {string} date - 交易日期
 * @property {number} amount - 交易金额
 * @property {string} category - 交易分类
 */

/**
 * @param {Transaction[]} transactions
 * @returns {number}
 */
function calculateTotal(transactions) {
    ...
}
```

---

## 4. Git 规范

### 4.1 分支策略

采用 **简化分支策略**：

```
main (主分支)
    └── dev (开发分支)
            └── feature/* (功能分支)
            └── fix/* (修复分支)
```

| 分支 | 用途 | 说明 |
|------|------|------|
| **main** | 生产分支 | 保持稳定，只接受 merge |
| **dev** | 开发分支 | 日常开发主分支 |
| **feature/*** | 功能分支 | 从 dev 创建，完成后合并回 dev |
| **fix/*** | 修复分支 | 从 dev 创建，紧急修复可直接合并到 main |

### 4.2 提交信息规范

采用 **Conventional Commits** 规范：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

**类型（type）**：
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 重构（不改变功能）
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：
```bash
feat(api): 添加年度分析API接口

实现了按年份获取收支汇总的功能，支持：
- 年度总收入/支出统计
- 月度趋势数据
- 分类占比分析

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

### 4.3 工作流程

**开发新功能**：
```bash
# 1. 从 dev 创建功能分支
git checkout dev
git pull origin dev
git checkout -b feature/yearly-analysis

# 2. 开发并提交
git add .
git commit -m "feat: 实现年度分析页面"

# 3. 推送到远程
git push origin feature/yearly-analysis

# 4. 创建 Pull Request 到 dev
```

**修复 Bug**：
```bash
# 1. 从 dev 创建修复分支
git checkout dev
git checkout -b fix/upload-error

# 2. 修复并提交
git add .
git commit -m "fix: 修复上传文件时的编码问题"

# 3. 推送并创建 PR
git push origin fix/upload-error
```

---

## 5. 测试规范

### 5.1 测试类型

| 测试类型 | 说明 | 覆盖率目标 |
|---------|------|-----------|
| **单元测试** | 测试单个函数/方法 | ≥ 70% |
| **集成测试** | 测试模块间交互 | 核心流程 100% |
| **API 测试** | 测试 API 接口 | 全部 API |
| **E2E 测试** | 端到端用户流程 | 核心场景 |

### 5.2 测试框架

**后端测试**：
```python
# 使用 pytest
import pytest
from services.data_service import DataService

def test_get_yearly_summary():
    """测试年度汇总功能"""
    service = DataService()
    result = service.get_yearly_summary(2024)
    assert result['total_expense'] >= 0
    assert 'monthly_data' in result
```

**前端测试**：
```javascript
// 使用 Vitest
import { describe, it, expect } from 'vitest'
import { formatMoney } from '@/utils/format'

describe('formatMoney', () => {
    it('should format number to currency', () => {
        expect(formatMoney(1234.5)).toBe('1,234.50')
    })
})
```

### 5.3 测试命令

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

---

## 6. 部署规范

### 6.1 环境变量

**后端 (.env)**：
```bash
# 应用配置
APP_NAME=小遥账单助手
APP_ENV=production
DEBUG=False

# Flask 配置
SECRET_KEY=your-secret-key
SESSION_LIFETIME=1800

# 文件上传
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/tmp/flask_uploads
```

**前端 (.env.production)**：
```bash
# API 地址
VITE_API_BASE_URL=/api

# 其他配置
VITE_APP_TITLE=小遥账单助手
```

### 6.2 构建流程

**前端构建**：
```bash
cd frontend
npm install
npm run build
# 输出到 frontend/dist/
```

**后端运行**：
```bash
cd backend
py -3.10 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 6.3 生产部署

**推荐配置**：
- 使用 Nginx 作为 Web 服务器
- 前端静态文件由 Nginx 直接服务
- 后端 API 通过反向代理访问

**Nginx 配置示例**：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 7. 设计文档引用

本项目采用**精益开发流程**，所有设计文档位于 `docs/` 目录。

### 7.1 基础模板文档（docs/base/）

| 文档 | 说明 | 用途 |
|------|------|------|
| [精益开发流程.md](docs/base/精益开发流程.md) | 开发流程指南 | 从商业模式到 MVP 的完整流程 |
| [00-精益MRD-模版.md](docs/base/00-精益MRD-模版.md) | 市场需求文档模板 | 定义目标用户和市场定位 |
| [01-精简PRD-模版.md](docs/base/01-精简PRD-模版.md) | 产品需求文档模板 | 定义功能需求 |
| [03-技术方案文档-模版.md](docs/base/03-技术方案文档-模版.md) | 技术方案模板 | 技术实现方案 |
| [04-开发任务清单-模版.md](docs/base/04-开发任务清单-模版.md) | 任务清单模板 | 开发任务分解 |
| [06-技术选型-模版.md](docs/base/06-技术选型-模版.md) | 技术选型模板 | 技术栈决策记录 |
| [07-代码架构-模版.md](docs/base/07-代码架构-模版.md) | 代码架构模板 | 项目结构设计 |
| [08-数据库文档-模版.md](docs/base/08-数据库文档-模版.md) | 数据库文档模板 | 数据库设计 |
| [09-接口文档-模版.md](docs/base/09-接口文档-模版.md) | 接口文档模板 | API 接口定义 |
| [10-部署文档-模版.md](docs/base/10-部署文档-模版.md) | 部署文档模板 | 部署流程说明 |
| [11-架构决策-模版.md](docs/base/11-架构决策-模版.md) | 架构决策模板 | 记录重要技术决策 |
| [12-测试文档-模版.md](docs/base/12-测试文档-模版.md) | 测试文档模板 | 测试用例和计划 |

### 7.2 项目核心文档

| 文档 | 说明 |
|------|------|
| [00-mrd.md](docs/00-mrd.md) | 市场需求文档 - 产品定位和目标用户 |
| [01-prd.md](docs/01-prd.md) | 产品需求文档 - 功能清单和页面结构 |
| [接口文档.md](docs/接口文档.md) | API 接口完整文档 |
| [02-老账单项目分析.md](docs/02-老账单项目分析.md) | 老项目技术分析 |
| [02-老账单重构方案.md](docs/02-老账单重构方案.md) | 前后端分离重构方案 |

### 7.3 运营文档

| 文档 | 说明 |
|------|------|
| [运营文档/应用宣传文档.md](docs/运营文档/应用宣传文档.md) | 产品宣传材料 |
| [运营文档/应用宣传视频脚本.md](docs/运营文档/应用宣传视频脚本.md) | 宣传视频脚本 |

---

## 8. 开发约定

### 8.1 个人偏好

**重要**：所有 AI 回复、文档编写、代码注释**必须使用中文**。

- ✅ 正确：`// 获取年度分析数据`
- ❌ 错误：`// Get yearly analysis data`

### 8.2 功能完成检查清单

每次完成一个功能后，**必须自己检查**以下项目：

- [ ] **功能正确性**：核心功能是否按需求实现
- [ ] **错误处理**：边界情况和异常是否有处理
- [ ] **代码质量**：代码是否符合规范，是否有必要的注释
- [ ] **测试验证**：是否通过了相关测试
- [ ] **文档更新**：相关文档是否已更新
- [ ] **Git 提交**：提交信息是否规范，代码是否已推送

### 8.3 代码审查要点

**后端代码审查**：
- API 接口是否保持兼容
- 错误处理是否完善
- 是否有安全隐患（SQL注入、XSS等）
- 性能是否可接受

**前端代码审查**：
- 组件是否可复用
- 状态管理是否合理
- 用户体验是否流畅
- 响应式布局是否正常

### 8.4 常用命令速查

**后端**：
```bash
# 进入后端目录
cd backend

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python app.py

# 退出虚拟环境
deactivate
```

**前端**：
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

---

## 9. 架构决策记录

### AD-20260217-001: 前后端分离重构

**日期**: 2026-02-17

**背景**:
原有项目采用 Flask + Jinja2 模板渲染，前后端高度耦合，`app.py` 文件超过 3500 行，难以维护。

**解决方案**:
采用渐进式重构策略：
1. 先分离前端（Vue 3 + Vite），后端 API 保持不变
2. 双前端并行运行，逐步验证
3. 前端稳定后，再重构后端模块化

**影响**:
- 开发周期增加约 4 周
- 长期可维护性大幅提升
- API 接口需保持向后兼容

---

## 附录：快速链接

- [精益开发流程图](docs/base/精益开发流程.md)
- [市场需求文档](docs/00-mrd.md)
- [产品需求文档](docs/01-prd.md)
- [API 接口文档](docs/接口文档.md)
- [老项目分析](docs/02-老账单项目分析.md)
- [重构方案](docs/02-老账单重构方案.md)

---

**文档维护**: 开发团队
**最后更新**: 2026-02-17
