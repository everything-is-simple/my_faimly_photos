# 架构设计文档

本文档定义了「家庭照片管理系统」的系统架构设计。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: "活跃"
**文档版本**: "**v0.1终极版**"

## 1. 系统架构概述

家庭照片管理系统采用现代化的 **前后端分离** 架构。该架构将用户界面（前端）与业务逻辑和数据处理（后端）解耦，通过清晰定义的API进行通信。这种设计提高了系统的可维护性、可扩展性和开发效率。

-   **后端 (Backend)**: 一个基于 **Python Flask** 的无状态 **RESTful API** 服务器。它负责处理所有业务逻辑、数据持久化、用户认证和文件存储。
-   **前端 (Frontend)**: 一个基于 **Vue.js** 的 **单页应用 (SPA)**。它为用户提供丰富的交互体验，并通过API与后端通信。
-   **数据库 (Database)**: 使用 **SQLite** 进行数据存储，通过 **SQLAlchemy ORM** 进行管理。

### 1.1 设计原则

-   **单一职责**: 前端专注于用户体验和界面展示，后端专注于业务逻辑和数据。
-   **无状态API**: 后端API应为无状态，每次请求都应包含所有必要信息（如通过JWT进行认证），不依赖服务器会话。
-   **模块化**: 前后端内部均采用模块化设计，便于开发和维护。

## 2. 架构图

### 2.1 高级架构图

```mermaid
graph TD
    subgraph "用户端"
        A[用户浏览器]
    end

    subgraph "前端 (Vue.js SPA)"
        B[视图层<br/>(Views/Components)]
        C[状态管理<br/>(Pinia)]
        D[路由<br/>(Vue Router)]
        E[API服务<br/>(Axios)]
    end

    subgraph "后端 (Flask RESTful API)"
        F[路由层<br/>(Flask Blueprints)]
        G[服务层<br/>(Services)]
        H[模型层<br/>(SQLAlchemy Models)]
        I[数据库<br/>(SQLite)]
        J[文件存储<br/>(本地文件系统)]
    end

    A --> B
    B --> C
    B --> D
    B --> E
    E -- "RESTful API (JSON + JWT)" --> F
    F --> G
    G --> H
    G --> J
    H --> I
```

### 2.2 数据流 (以照片上传为例)

1.  用户在 **前端界面** 选择照片并点击上传。
2.  **Vue组件** 触发 **API服务 (Axios)**，将照片数据发送到后端。
3.  后端 **Flask路由** 接收到API请求，并通过JWT认证装饰器验证Token。
4.  **照片服务 (Photo Service)** 处理业务逻辑：
    -   验证文件类型、大小等。
    -   将文件保存到 **文件存储**。
    -   创建一个新的 **照片模型 (Photo Model)** 实例。
5.  **照片模型** 通过 **SQLAlchemy** 将照片元数据存入 **SQLite数据库**。
6.  后端API向前端返回一个包含成功信息的 **JSON响应**。
7.  前端接收响应，并更新 **视图** 和 **全局状态 (Pinia)**，向用户显示上传成功。

## 3. 技术选型

详细技术选型请参考 `TRD.md`。

| 领域 | 技术 | 描述 |
| :--- | :--- | :--- |
| **后端** | Python, Flask, SQLAlchemy | 构建RESTful API，进行数据库操作。 |
| **前端** | Vue.js 3, Vite, Pinia, Vue Router | 构建响应式的单页应用。 |
| **API通信**| Axios, REST, JSON | 前后端数据交换。 |
| **认证** | JWT (JSON Web Tokens) | 实现基于Token的无状态认证。 |
| **UI组件库**| Element Plus | 提供高质量、可复用的前端UI组件。 |
| **测试** | Pytest (后端), Vitest (前端) | 保证代码质量。 |

## 4. 核心模块职责

### 4.1 后端模块 (`backend/`)

-   **`home_photo/routes/`**: 定义API端点 (Blueprints)，处理HTTP请求和响应，调用服务层。
-   **`home_photo/services/`**: 实现核心业务逻辑，不直接与数据库或HTTP层交互。
-   **`home_photo/models/`**: 定义SQLAlchemy数据模型，负责与数据库的ORM映射。
-   **`home_photo/utils/`**: 提供通用的工具函数（如文件处理、安全）。

### 4.2 前端模块 (`frontend/`)

-   **`src/views/`**: 页面级组件，由Vue Router直接渲染。
-   **`src/components/`**: 可复用的UI组件（如按钮、表单、照片卡片）。
-   **`src/store/`**: 使用Pinia定义和管理全局应用状态（如用户信息、照片列表）。
-   **`src/services/`**: 封装对后端API的调用 (使用Axios)。
-   **`src/router/`**: 定义前端路由规则。

## 5. 部署策略

-   **后端**: 作为一个独立的Web服务部署（例如，使用Gunicorn + Nginx）。
-   **前端**: 通过Vite构建为一组静态文件（HTML, CSS, JS），并由Web服务器（如Nginx）托管。
-   **通信**: 需要配置Web服务器（如Nginx）的反向代理，将特定的API请求（如 `/api/*`）转发到后端服务，以解决跨域问题。

---

最后更新: 2025-07-19 | 版本: v0.1终极版