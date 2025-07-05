# 目录结构规范 (v0.1终极版)

本文档定义了「家庭照片管理系统」项目 **v0.1终极版** 的目录结构规范。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: "活跃"
**文档版本**: "**v0.1终极版**"

## 1. 项目根目录结构

项目采用前后端分离的结构，代码分别位于 `backend/` 和 `frontend/` 目录中。

```text
photos/
├── backend/                 # 后端 (Flask API)
├── frontend/                # 前端 (Vue SPA)
├── docs/                    # 项目文档
├── .gitignore               # Git忽略文件
└── README.md                # 项目说明
```

---

## 2. 后端目录结构 (`backend/`)

后端是一个基于Flask的RESTful API项目。

```text
backend/
├── .venv/                   # Python虚拟环境 (Git忽略)
├── app/                     # Flask应用核心代码
│   ├── __init__.py          # 应用工厂和蓝图注册
│   ├── models/              # 数据模型层 (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── family_model.py
│   │   ├── photo_model.py
│   │   └── album_model.py
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── family_service.py
│   │   ├── photo_service.py
│   │   ├── album_service.py
│   │   └── search_service.py
│   ├── routes/              # 路由控制层 (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── family_routes.py
│   │   ├── photo_routes.py
│   │   ├── album_routes.py
│   │   └── search_routes.py
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── auth_utils.py
├── tests/                   # 测试代码 (Pytest)
│   ├── conftest.py
│   ├── routes/
│   │   ├── test_auth_routes.py
│   │   └── ...
│   └── services/
│       ├── test_user_service.py
│       └── ...
├── storage/                 # 文件存储目录 (Git忽略)
│   └── photos/
├── logs/                    # 日志目录 (Git忽略)
├── config.py                # 配置文件
├── run.py                   # 应用启动脚本
└── requirements.txt         # Python依赖
```

### 2.1 后端模块职责

-   **`app/models/`**: 定义与数据库表对应的SQLAlchemy模型。
-   **`app/services/`**: 包含纯粹的业务逻辑，由路由层调用。
-   **`app/routes/`**: 定义Flask蓝图，包含所有API端点。处理HTTP请求，验证数据，调用服务，并返回JSON响应。
-   **`storage/`**: 存储用户上传的原始文件，如照片。
-   **`tests/`**: 包含所有后端的单元测试和功能测试。

---

## 3. 前端目录结构 (`frontend/`)

前端是一个基于Vue.js的单页应用 (SPA)。(V1.0 MVP阶段，后端优先)

```text
frontend/
├── node_modules/            # Node.js依赖 (Git忽略)
├── public/                  # 公共静态资源
│   └── favicon.ico
├── src/                     # 主要源代码
│   ├── assets/              # 静态资源 (会被Vite处理)
│   ├── components/          # 可复用UI组件
│   ├── views/               # 页面级组件
│   ├── services/            # API服务 (Axios封装)
│   ├── store/               # 全局状态管理 (Pinia)
│   ├── router/              # 路由配置 (Vue Router)
│   ├── App.vue              # 根组件
│   └── main.js              # 应用入口点
├── .gitignore               # Git忽略文件
├── index.html               # SPA主HTML文件
├── package.json             # 项目元数据和依赖
├── vite.config.js           # Vite配置文件
└── README.md                # 前端项目说明
```

### 3.1 前端模块职责

-   **`src/components/`**: 存放可被多个视图复用的小型UI组件。
-   **`src/views/`**: 存放与特定路由对应的页面级组件。
-   **`src/services/`**: 封装所有与后端API的通信逻辑。每个文件通常对应后端的一个模块（如`authService.js`）。
-   **`src/store/`**: 使用Pinia管理需要跨组件共享的全局状态，例如当前登录的用户信息。
-   **`src/router/`**: 配置URL路径与视图组件之间的映射关系。

## 4. 命名规范

-   **Python (后端)**:
    -   文件名/模块名: `snake_case.py` (e.g., `user_service.py`)
    -   类名: `PascalCase` (e.g., `User`, `PhotoService`)
    -   变量/函数名: `snake_case` (e.g., `get_user_by_id`)
-   **JavaScript/Vue (前端)**:
    -   文件名 (组件): `PascalCase.vue` (e.g., `PhotoGallery.vue`)
    -   文件名 (其他JS): `camelCase.js` (e.g., `authService.js`)
    -   变量/函数名: `camelCase` (e.g., `getUserById`)

---
最后更新: 2025-07-19 | 版本: v0.1终极版 