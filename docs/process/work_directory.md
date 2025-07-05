# 工作目录结构快照

**快照时间**: 2025-07-05
**关联任务**: (BE-INIT)

本文档是当前项目工作目录的真实快照，用于与 `docs/process/plan-DIR.md` 进行比对。

```
my_faimly_photos/
├── backend/
│   ├── .gitignore
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── album_model.py
│   │   │   ├── family_model.py
│   │   │   ├── photo_model.py
│   │   │   └── user_model.py
│   │   ├── routes/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── utils/
│   │       └── __init__.py
│   ├── config.py
│   ├── logs/
│   ├── requirements.txt
│   ├── run.py
│   ├── storage/
│   │   └── photos/
│   └── tests/
│       ├── routes/
│       └── services/
├── docs/
│   ├── ... (现有文档)
│   └── process/
│       ├── LOGS.md
│       └── work_directory.md
└── ...
```

# 动态工作目录记录 (v0.1终极版)

本文档是 `plan-DIR.md` 的 **动态对应物**，旨在通过自动化脚本实时记录项目开发过程中 **实际** 的目录结构，作为"现实"的证据。

**警告**: 在自动化脚本部署前，此文件内容与 `plan-DIR.md` 保持一致，作为初始基线。请勿手动修改。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: 活跃
**文档版本**: **v0.1终极版**

---

## 1. 后端目录结构 (`backend/`)

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

---

## 2. 前端目录结构 (`frontend/`)

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

## 偏差恢复 (D003)

以下文件是在解决 "D003: 项目状态严重回滚" 偏差期间恢复或创建的。

### `app/`

#### `services/`
- **`search_service.py`**: 恢复。

#### `routes/`
- **`search_routes.py`**: 恢复。
- **`album_routes.py`**: 创建占位文件以修复依赖。

#### `models/`
- **`photo_model.py`**: 修改被恢复。

#### `__init__.py`
- **状态**: 修改被恢复。

### `tests/routes/`
- **`test_search_routes.py`**: 恢复。
