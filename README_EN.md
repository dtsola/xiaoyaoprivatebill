# Xiaoyao Private Bill Analyzer

> Privacy-first personal bill analysis tool. All data is processed locally, nothing is uploaded to any server.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.4+-brightgreen.svg)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

English | [简体中文](README.md)

<p align="center">
  <img src="docs/产品文档/产品截图/宣传海报图.png" alt="Xiaoyao Bill Assistant Poster">
</p>

---

## Introduction

<p align="center">
  <img src="docs/产品文档/logos/logo.png" alt="Xiaoyao Bill Assistant" width="200">
</p>

Xiaoyao Private Bill Analyzer is a **privacy-first** personal bill analysis tool that supports automatic parsing and multi-dimensional data visualization for Alipay and WeChat bills.

**Key Features**:
- 🔒 **Privacy First** - All data is processed locally, nothing is uploaded to any server
- 🔐 **Manual Clear** - Manually clear bill data anytime, have full control of your financial privacy
- 📊 **Multi-dimensional Analysis** - Yearly, monthly, category, time, and consumption insights
- 📁 **Multiple Format Support** - Alipay CSV, WeChat CSV/XLSX bill files
- 🚀 **Quick Deployment** - One-click Docker setup, ready to use
- 💻 **Frontend-Backend Separation** - Vue 3 + Flask architecture, easy to maintain and extend
- 📱 **Responsive Design** - Supports desktop and mobile access

---

## Author

<p align="center">
  <img src="docs/产品文档/产品截图/作者头像.jpg" alt="dtsola" width="120" height="120" style="border-radius: 50%;">
</p>

<p align="center">
  <b>dtsola</b> — IT Solution Architect | Indie Solo Practitioner
</p>

<p align="center">
  🌐 <a href="https://www.dtsola.com">Personal Site</a> &nbsp;|&nbsp;
  📺 <a href="https://space.bilibili.com/736015">Bilibili</a> &nbsp;|&nbsp;
  💬 WeChat: dtsola (Connect with me, note: github)
</p>

<p align="center">
  <img src="docs/产品文档/产品截图/个人二维码.png" alt="WeChat QR Code" width="150">
</p>

---

## Feature Preview

### Upload Bills - One-Click Import

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/08-上传账单.png" alt="Upload Bills"></td>
<td width="50%">
<ul>
<li>📤 Drag & drop bill upload</li>
<li>📋 Auto-detect Alipay/WeChat bill format</li>
<li>⚡ Fast parsing, one-click analysis report</li>
</ul>
</td>
</tr>
</table>

### Homepage - Feature Dashboard

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/01-首页.png" alt="Homepage"></td>
<td width="50%">
<ul>
<li>🎯 All-in-One Bill Analysis Tool - Supports Alipay and WeChat bills</li>
<li>📊 4 Feature Cards - Multi-dimensional analysis, privacy protection, trend tracking, smart search</li>
<li>🚀 Quick Actions - Upload bill files or view sample data</li>
</ul>
</td>
</tr>
</table>

### Yearly Overview - At a Glance

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/02-年度总览.png" alt="Yearly Overview"></td>
<td width="50%">
<ul>
<li>📊 Yearly income/expense summary</li>
<li>📈 Yearly trend charts</li>
<li>📖 Yearly story review</li>
</ul>
</td>
</tr>
</table>

### Monthly Analysis - Detailed Comparison

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/03-月度分析.png" alt="Monthly Analysis"></td>
<td width="50%">
<ul>
<li>📅 Monthly trends & comparison</li>
<li>🗓️ Monthly calendar view</li>
<li>📉 Month-over-month analysis</li>
</ul>
</td>
</tr>
</table>

### Category Analysis - Spending Breakdown

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/04-分类分析.png" alt="Category Analysis"></td>
<td width="50%">
<ul>
<li>🏷️ Category breakdown & distribution</li>
<li>📊 Category ranking & statistics</li>
<li>📝 Category transaction details</li>
</ul>
</td>
</tr>
</table>

### Time Analysis - Spending Patterns

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/05-时间分析.png" alt="Time Analysis"></td>
<td width="50%">
<ul>
<li>⏰ Spending time distribution</li>
<li>🌡️ Peak hours heatmap</li>
<li>📈 Consumption habit insights</li>
</ul>
</td>
</tr>
</table>

### Consumption Insights - Smart Analytics

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/06-消费洞察-01.png" alt="Consumption Insights 1"></td>
<td width="50%"><img src="docs/产品文档/产品截图/06-消费洞察-02.png" alt="Consumption Insights 2"></td>
</tr>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/06-消费洞察-03.png" alt="Consumption Insights 3"></td>
<td width="50%">
<ul>
<li>💡 Spending habit analysis</li>
<li>🔍 Anomaly alerts</li>
<li>📊 Personalized recommendations</li>
</ul>
</td>
</tr>
</table>

### Transaction Records - Detailed History

<table>
<tr>
<td width="50%"><img src="docs/产品文档/产品截图/07-交易记录.png" alt="Transaction Records"></td>
<td width="50%">
<ul>
<li>📋 Complete transaction history</li>
<li>🔍 Multi-dimensional filtering</li>
<li>📤 Export support for further analysis</li>
</ul>
</td>
</tr>
</table>

---

## Quick Start

### Option 1: Docker One-Click Installation (Recommended for Users)

#### Environment Setup

Install Docker Desktop (includes Docker Compose):
- Windows: https://docs.docker.com/desktop/setup/install/windows-install/
- Mac: https://docs.docker.com/desktop/setup/install/mac-install/
- Linux: https://docs.docker.com/desktop/setup/install/linux/

#### Start Steps

```bash
# 1. Clone the repository
git clone https://github.com/dtsola/xiaoyaoprivatebill.git
cd xiaoyaoprivatebill

# 2. Start with one command
docker-compose up -d

# 3. Access the application
# Open in browser: http://localhost:8888
```

#### Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

---

### Option 2: Developer Local Setup

#### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

#### Backend Setup

```bash
# 1. Enter backend directory
cd backend

# 2. Create and activate virtual environment (Windows)
py -3.10 -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start backend service
python app.py
# Backend runs on: http://localhost:5000
```

#### Frontend Setup

```bash
# 1. Enter frontend directory (new terminal window)
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
# Frontend runs on: http://localhost:3000
```

#### Development Commands

```bash
# Build frontend for production
npm run build

# Preview production build
npm run preview

# Exit backend virtual environment
deactivate
```

---

## Usage Guide

### 1. Get Bill Files

**Alipay Bills**:
1. Open Alipay App → Bills
2. Click "Common Questions" in top right → Export Bills
3. Select "Personal Bills" → Date Range → Choose CSV format
4. Enter email, wait for bill file

**WeChat Bills**:
1. Open WeChat → Me → Services → Wallet → "Bills" in top right
2. Click "Common Questions" → Download Bills
3. Select date range → Enter email → Choose CSV/XLSX format

### 2. Upload and Analyze

1. Visit the application homepage
2. Click "Upload Bill" button
3. Select downloaded bill file (CSV/XLSX)
4. Wait for parsing to complete, auto-redirect to analysis page

### 3. Export Data

After analysis, results can be exported as:
- PNG images (chart screenshots)
- CSV data (raw data)

---

## Tech Stack

### Backend

| Technology | Version | Description |
|------------|---------|-------------|
| Python | 3.10+ | Backend language |
| Flask | 2.0+ | Web framework |
| Pandas | Latest | Data processing core |
| NumPy | Latest | Numerical computing |
| OpenPyXL | Latest | Excel file processing |

### Frontend

| Technology | Version | Description |
|------------|---------|-------------|
| Vue | 3.4+ | Frontend framework |
| Vite | 5.0+ | Build tool |
| Vue Router | 4.2+ | Router management |
| Pinia | 2.1+ | State management |
| ECharts | 5.4+ | Data visualization |

### Deployment

| Technology | Description |
|------------|-------------|
| Docker | Containerization |
| Docker Compose | Service orchestration |
| Nginx | Web server |

---

## Project Structure

```
xiaoyaoprivatebill/
├── backend/               # Backend project (Flask + Pandas)
│   ├── api/              # API routing layer
│   ├── services/         # Business logic layer
│   ├── parsers/          # File parsing modules
│   ├── utils/            # Utility functions
│   ├── data/             # Temporary data directory
│   ├── app.py            # Application entry
│   ├── config.py         # Configuration management
│   ├── Dockerfile        # Backend image build
│   └── requirements.txt  # Python dependencies
│
├── frontend/             # Frontend project (Vue 3 + Vite)
│   ├── src/
│   │   ├── api/         # API client
│   │   ├── views/       # Page components
│   │   ├── components/  # Shared components
│   │   ├── stores/      # State management (Pinia)
│   │   └── utils/       # Utility functions
│   ├── nginx.conf       # Nginx configuration
│   ├── Dockerfile       # Frontend image build
│   ├── package.json     # Dependencies config
│   └── vite.config.js   # Vite configuration
│
├── docs/                 # Documentation directory
├── docker-compose.yml    # Docker orchestration config
└── README.md            # This document
```

---

## Documentation

- [Market Requirements Document (MRD)](docs/00-mrd.md)
- [Product Requirements Document (PRD)](docs/01-prd.md)
- [API Documentation](docs/接口文档.md)
- [Technical Specification](docs/03-技术方案文档.md)
- [Deployment Guide](docs/部署文档.md)
- [Development Guide](docs/开发进度.md)

---

## Acknowledgments

This project's frontend and backend are completely refactored from the excellent open-source project [alipay_record_analysis](https://github.com/Hessel2333/alipay_record_analysis). Special thanks to the original author **Hessel2333** for the inspiration and foundation code.

Based on the original project, this project has made the following improvements:
- Frontend refactored from Jinja2 templates to Vue 3 + Vite modern architecture
- Backend refactored from monolithic application to modular blueprint architecture
- Optimized frontend and backend performance
- Enhanced data visualization
- Added Docker one-click deployment capability

---

## Contributing

Contributions, issue reports, and suggestions are welcome!

### Development Workflow

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

### Code Standards

- Backend follows [PEP 8](https://pep8.org/) standards
- Frontend follows [ESLint](https://eslint.org/) recommended standards
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) specification

For detailed standards, please refer to [CLAUDE.md](.claude/CLAUDE.md)

---

## FAQ

### Q: What bill formats are supported?

A: Currently supports:
- Alipay CSV bills
- WeChat CSV bills
- WeChat XLSX bills

### Q: Is data uploaded to servers?

A: No. All data processing is done entirely locally, nothing is uploaded to any server.

### Q: Is mobile supported?

A: Yes. The frontend uses responsive design and works normally on mobile browsers.

### Q: How to change default ports?

A:
- Docker deployment: Modify port mapping in `docker-compose.yml`
- Backend: Modify `PORT` config in `backend/config.py`
- Frontend development: Modify `server.port` in `frontend/vite.config.js`

---

## License

This project is licensed under the [MIT License](LICENSE)

---

## Contact

- Project Homepage: [GitHub](https://github.com/dtsola/xiaoyaoprivatebill)
- Issue Tracker: [Issues](https://github.com/dtsola/xiaoyaoprivatebill/issues)

---

**Made with ❤️ by Xiaoyao Team**
