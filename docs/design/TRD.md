# 技术需求文档

本文档定义了「家庭照片管理系统」的技术需求、选型和实现规范。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: "活跃"
**文档版本**: "**v0.1终极版**"

---

## 1. 技术架构概述

本项目采用 **前后端分离** 的现代化架构。

-   **后端**: 基于 **Python Flask** 的 **RESTful API** 服务器，提供无状态接口。
-   **前端**: 基于 **Vue.js 3** 的 **单页应用 (SPA)**，负责所有用户界面渲染和交互。

这种架构确保了职责分离、高度可扩展性和独立开发部署的能力。

## 2. 技术选型

| 类别 | 技术/框架 | 用途 | 备注 |
| :--- | :--- | :--- | :--- |
| **后端** |
| | Python 3.8+ | 核心编程语言 | |
| | Flask | Web框架 | 构建轻量级的RESTful API服务器。 |
| | SQLAlchemy | ORM框架 | 用于Python代码与SQLite数据库的交互。 |
| | Flask-Migrate | 数据库迁移 | 管理数据库结构变更。 |
| | Pytest | 测试框架 | 编写和执行单元测试、功能测试。 |
| **前端** |
| | Vue.js 3 | 核心框架 | 使用组合式API构建响应式用户界面。 |
| | Vite | 构建工具 | 提供极速的开发服务器和优化的构建输出。 |
| | Vue Router | 路由 | 管理前端单页应用的页面导航。 |
| | Pinia | 状态管理 | 轻量、直观的全局状态管理库。 |
| | Element Plus | UI组件库 | 提供一套高质量、可复用的Vue 3组件。 |
| | Axios | HTTP客户端 | 用于前端与后端API的通信。 |
| **数据库** |
| | SQLite | 关系型数据库 | 轻量、文件型，无需独立服务，适合快速开发。 |
| **认证** |
| | PyJWT | 认证方案 | 用于生成和验证JWT (JSON Web Tokens)，实现无状态认证。 |
| **开发工具** |
| | Git | 版本控制 | |
| | VS Code | 代码编辑器 | |
| | Prettier | 代码格式化 | 保证代码风格一致性。 |

## 3. 后端技术规范 (`backend/`)

### 3.1 API 设计原则

-   **RESTful**: 遵循REST架构风格，使用标准HTTP方法 (GET, POST, PUT, DELETE)。
-   **无状态 (Stateless)**: 每个请求都必须包含认证信息 (JWT)，服务器不维护用户会话。
-   **JSON**: 所有API请求体和响应体均使用JSON格式。
-   **统一响应格式**: 所有API响应都遵循统一结构：
    ```json
    {
      "code": 200, // 业务状态码, e.g., 200: 成功, 400: 客户端错误, 500: 服务器错误
      "message": "Success", // 响应消息
      "data": { ... } // 响应数据 (可选)
    }
    ```

### 3.2 认证 (JWT Bearer Token)

-   **登录**: 用户提供凭据，验证成功后，后端生成 `access_token` 和 `refresh_token` 并返回给客户端。
-   **请求认证**: 客户端在每次请求需要认证的API时，必须在 `Authorization` 请求头中附加 `access_token` (`Bearer <token>`)。
-   **中间件/装饰器**: 后端使用一个自定义的装饰器来验证每个受保护路由的 `access_token` 的有效性。

### 3.3 数据库

-   使用 **SQLAlchemy** 作为ORM进行数据库操作。
-   使用 **Flask-Migrate** 管理数据库模式的演进。
-   数据库文件位于 `backend/instance/app.db`。

### 3.4 文件存储

-   用户上传的照片存储在 `backend/storage/` 目录下。
-   目录按家庭ID进行隔离，以保证数据私密性。
-   API仅返回文件的访问URL，而不是直接传输文件内容。

## 4. 前端技术规范 (`frontend/`)

### 4.1 组件化开发

-   **`views/`**: 页面级组件，直接与Vue Router关联。
-   **`components/`**: 可复用的原子组件（如按钮、输入框、卡片等）。
-   所有组件应使用 `<script setup>` 语法和组合式API。

### 4.2 状态管理 (Pinia)

-   使用 **Pinia** 来管理全局共享的状态，例如：
    -   当前登录用户的信息 (user)。
    -   全局加载状态或通知。
-   Store应按功能模块划分（如 `authStore.js`, `photoStore.js`）。

### 4.3 API 通信 (Axios)

-   创建一个Axios实例 (`src/services/api.js`) 进行全局配置，例如：
    -   设置 `baseURL` 为后端API地址 (`/api`)。
    -   创建一个 **请求拦截器**，在每个请求发送前，动态地将存储在客户端的 `access_token` 注入到 `Authorization` 请求头中。
    -   创建一个 **响应拦截器**，进行统一的错误处理。特别是处理 `401 Unauthorized` 错误，当 `access_token` 过期时，应尝试使用 `refresh_token` 获取新Token并重发请求。
-   API请求按模块封装在 `src/services/` 目录下（如 `authService.js`）。

### 4.4 路由 (Vue Router)

-   使用 **Vue Router** 定义页面路由。
-   使用路由守卫 (`beforeEach`) 来检查用户的认证状态。通过检查本地是否存在有效的Token或调用 `/api/auth/me` 接口来验证登录状态。未登录用户访问受保护页面时，应重定向到登录页。

## 5. 安全规范

-   **密码安全**: 用户密码在存入数据库前必须使用 **bcrypt** 进行哈希处理。
-   **SQL注入**: 使用SQLAlchemy等ORM可有效防止SQL注入。
-   **XSS (跨站脚本)**: Vue.js默认对模板中的动态内容进行HTML转义。同时，为防止Token被XSS攻击窃取，应优先考虑将 `refresh_token` 存储在 `localStorage`中，而 `access_token` 可以存储在内存中。
-   **CORS (跨源资源共享)**: 后端需要配置CORS策略（如使用 `Flask-Cors`），允许来自前端域的跨源请求。

## 6. 代码规范

-   **后端 (Python)**: 遵循 **PEP 8** 规范。
-   **前端 (JS/Vue)**: 使用 **Prettier** 进行自动格式化，保持代码风格统一。
-   **命名**:
    -   Python: `snake_case` for variables/functions, `PascalCase` for classes.
    -   JavaScript: `camelCase` for variables/functions, `PascalCase` for classes/components.

---
最后更新: 2025-07-19 | 版本: v0.1终极版 