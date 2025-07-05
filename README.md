# 家庭照片管理系统 (Family Photo Management System)

本项目是一个基于前后端分离架构的家庭照片管理与分享平台。旨在为家庭提供一个私有的、安全的、易于使用的照片存储和浏览空间，解决家庭照片分散、长辈使用困难和隐私担忧等痛点。

---

## 核心功能

根据产品需求文档 (`docs/design/PRD.md`)，系统 V1.0 版本规划了以下核心功能模块：

*   **用户认证**: 提供安全的注册、登录、登出及认证状态保持功能。
*   **家庭管理**: 支持创建家庭、通过邀请码加入或离开家庭，实现家庭成员与照片资源的隔离。
*   **照片管理**: 支持单张或多张照片上传、按时间线的瀑布流展示、全屏浏览及软删除。
*   **相册管理**: 支持创建相册、编辑相册信息、将照片归类到相册以及浏览相册内容。
*   **智能检索**: 提供按上传者、上传日期、文件名关键词等多种维度的照片搜索功能。

---

## 技术栈

系统采用现代化的技术栈，详细定义见技术需求文档 (`docs/design/TRD.md`)。

*   **后端 (Backend)**:
    *   框架: **Python 3.10+**, **Flask**
    *   数据库: **SQLite**
    *   ORM: **SQLAlchemy**
    *   数据库迁移: **Flask-Migrate**
    *   认证: **JWT (JSON Web Tokens)**
    *   测试: **Pytest**

*   **前端 (Frontend)**:
    *   框架: **Vue.js 3**
    *   构建工具: **Vite**
    *   状态管理: **Pinia**
    *   路由: **Vue Router**
    *   UI组件库: **Element Plus**
    *   API通信: **Axios**

---

## 项目结构

项目遵循清晰的模块化目录结构，详情请参考 `docs/process/plan-DIR.md`。

```my_faimly_photos/
├── backend/            # 后端 Flask API
│   ├── app/            # 应用核心代码 (models, services, routes)
│   ├── tests/          # 测试代码
│   ├── storage/        # 上传文件存储
│   └── ...
├── frontend/           # 前端 Vue SPA
│   ├── src/            # 源码 (components, views, services, store)
│   └── ...
└── docs/               # 唯一的真理之源：所有项目文档
```

---

## 开发工作流

本项目采用一套严格的、**文档驱动、任务驱动、测试驱动**的开发工作流，所有开发活动必须遵循 `docs/process/WORKFLOW.md` 中定义的规范。

*   **核心原则**: 所有开发必须以`docs/`目录下的设计文档为依据，并以`TODOLIST.md`中的任务为单元进行。
*   **TDD**: 采用严格的测试驱动开发（TDD）模式。
*   **Git**: 使用简化的Git Flow，分支命名、提交信息均需遵循约定式规范。

---

## 快速开始 (Getting Started)

### 后端 (Backend)

1.  **进入目录**:
    ```bash
    cd backend
    ```

2.  **创建并激活Python虚拟环境** (以PowerShell为例):
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

3.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **初始化数据库**:
    *   (首次) 初始化迁移环境: `flask db init`
    *   (首次) 生成迁移脚本: `flask db migrate -m "Initial migration"`
    *   应用迁移到数据库: `flask db upgrade`

5.  **运行开发服务器**:
    ```bash
    flask run
    ```
    API服务将运行在 `http://127.0.0.1:5000`。

### 前端 (Frontend)

1.  **进入目录**:
    ```bash
    cd frontend
    ```

2.  **安装依赖**:
    ```bash
    npm install
    ```

3.  **运行开发服务器**:
    ```bash
    npm run dev
    ```

---

## 项目文档 (Single Source of Truth)

本项目所有设计、需求和流程的权威信息均存放在 `docs/` 目录中。在开始任何开发工作前，请务必仔细阅读相关文档。

*   **产品与功能**: `docs/design/PRD.md`
*   **系统架构**: `docs/design/ARCHITECTURE.md`
*   **API接口**: `docs/design/API.md`
*   **数据库设计**: `docs/design/ERD.md`
*   **开发任务**: `docs/process/TODOLIST.md`
*   **开发工作流**: `docs/process/WORKFLOW.md` 