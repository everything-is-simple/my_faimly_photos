# API接口文档

本文档定义了「家庭照片管理系统」前后端通信的 **RESTful API** 规范。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: "活跃"
**文档版本**: "**v0.1终极版**"

---

## 1. 基础规范

### 1.1. API 根路径

所有API端点都以 `/api` 为统一前缀。
- **开发环境**: `http://127.0.0.1:5000/api`
- **生产环境**: `https://yourdomain.com/api`

### 1.2. 认证机制 (JWT Bearer Token)

- **核心**: 本API采用 **基于 JWT (JSON Web Token) 的无状态认证机制**。
- **流程**:
    1.  客户端（前端）通过 `POST /api/auth/login` 发送用户名和密码。
    2.  服务器验证凭据，如果成功，生成一个 `access_token` 和一个 `refresh_token` 并返回给客户端。
    3.  客户端需要安全地存储这两个Token（例如，在 `localStorage` 或 `HttpOnly Cookie` 中）。
    4.  对于所有需要认证的请求，客户端必须在 `Authorization` 请求头中携带 `access_token`。
        ```
        Authorization: Bearer <access_token>
        ```
- **Token过期**:
    - `access_token` 的有效期较短（如15分钟）。如果过期，服务器将返回 `401 Unauthorized`。
    - 客户端在收到 `401` 后，应使用 `refresh_token` 调用 `POST /api/auth/refresh` 接口来获取新的 `access_token`。
    - `refresh_token` 的有效期较长（如30天）。如果它也过期，用户必须重新登录。

### 1.3. 标准响应格式

所有API的响应体都遵循以下统一的JSON结构：

```json
{
  "code": 200,      // 业务状态码 (200: 成功, 4xx: 客户端错误, 5xx: 服务器错误)
  "message": "Success", // 描述信息
  "data": { ... }   // 响应数据，可能为 null 或省略
}
```
- **成功**: `code: 200`
- **失败 (客户端)**: `code: 400` (通用错误), `401` (未认证), `403` (无权限), `404` (未找到), `422` (验证错误)。
- **失败 (服务器)**: `code: 500`

### 1.4. 数据验证

对于 `POST` 和 `PUT` 请求，服务器会对请求体中的数据进行验证。如果验证失败，将返回 `422 Unprocessable Entity` 响应，并在 `data` 字段中提供详细的错误信息。

```json
// 示例：注册时用户名已存在
{
  "code": 422,
  "message": "Validation Error",
  "data": {
    "errors": {
      "username": ["This username is already taken."]
    }
  }
}
```

---

## 2. 认证模块 (`/api/auth`)

### 2.1. 用户注册
- **接口**: `POST /api/auth/register`
- **描述**: 创建一个新用户账户。
- **请求体**:
  ```json
  {
    "username": "newuser",
    "password": "a_strong_password"
  }
  ```
- **成功响应 (201 Created)**:
  ```json
  {
    "code": 201,
    "message": "User registered successfully.",
    "data": {
      "user": { "id": 2, "username": "newuser" }
    }
  }
  ```

### 2.2. 用户登录
- **接口**: `POST /api/auth/login`
- **描述**: 使用用户名和密码登录，获取JWT。
- **请求体**:
  ```json
  {
    "username": "testuser",
    "password": "password123"
  }
  ```
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Login successful.",
    "data": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": { "id": 1, "username": "testuser" }
    }
  }
  ```
- **错误响应 (401 Unauthorized)**: 密码或用户名错误。

### 2.3. 用户登出
- **接口**: `POST /api/auth/logout`
- **描述**: 登出用户，使 `refresh_token` 失效。
- **权限**: **需要认证**
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Successfully logged out."
  }
  ```

### 2.4. 刷新认证Token
- **接口**: `POST /api/auth/refresh`
- **描述**: 使用 `refresh_token` 获取一个新的 `access_token`。
- **请求体**:
  ```json
  {
    "refresh_token": "your_refresh_token_here"
  }
  ```
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Token refreshed successfully.",
    "data": {
      "access_token": "new_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
  }
  ```

### 2.5. 获取当前用户信息
- **接口**: `GET /api/auth/me`
- **描述**: 使用请求头中的JWT `access_token` 获取当前登录用户的信息。
- **权限**: **需要认证**
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "User data retrieved successfully.",
    "data": {
      "user": { "id": 1, "username": "testuser" }
    }
  }
  ```

---

## 3. 照片模块 (`/api/photos`)

### 3.1. 上传一张或多张照片
- **接口**: `POST /api/photos/upload`
- **描述**: 上传照片文件。
- **权限**: **需要认证**
- **请求体**: `multipart/form-data`
  - `files`: 一个或多个文件字段。
- **成功响应 (201 Created)**:
  ```json
  {
    "code": 201,
    "message": "3 photo(s) uploaded successfully.",
    "data": {
      "uploaded_photos": [
        { "id": 10, "filename": "photo1.jpg", "url": "/storage/photos/photo1.jpg" },
        { "id": 11, "filename": "photo2.png", "url": "/storage/photos/photo2.png" },
        { "id": 12, "filename": "photo3.gif", "url": "/storage/photos/photo3.gif" }
      ]
    }
  }
  ```

### 3.2. 获取照片列表 (分页)
- **接口**: `GET /api/photos`
- **描述**: 获取当前用户所在家庭的照片列表，支持分页。
- **权限**: **需要认证**
- **查询参数**:
  - `page` (可选): 页码, 默认 `1`。
  - `per_page` (可选): 每页数量, 默认 `20`。
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Photos retrieved successfully.",
    "data": {
      "photos": [
        { "id": 10, "url": "...", "created_at": "..." }
      ],
      "pagination": {
        "page": 1,
        "per_page": 20,
        "total_pages": 5,
        "total_items": 98
      }
    }
  }
  ```

### 3.3. 获取单张照片详情
- **接口**: `GET /api/photos/<int:photo_id>`
- **描述**: 获取指定ID的照片的详细信息。
- **权限**: **需要认证** (且用户必须有权查看该照片)。
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Photo details retrieved successfully.",
    "data": {
      "photo": {
        "id": 10,
        "url": "...",
        "filename": "photo1.jpg",
        "uploader": { "id": 1, "username": "testuser" },
        "created_at": "..."
      }
    }
  }
  ```

### 3.4. 删除照片 (软删除)
- **接口**: `DELETE /api/photos/<int:photo_id>`
- **描述**: 删除一张照片 (软删除)。
- **权限**: **需要认证** (用户只能删除自己上传的照片)。
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Photo deleted successfully.",
    "data": null
  }
  ```

---

## 4. 家庭模块 (`/api/family`)

### 4.1. 创建一个新家庭
- **接口**: `POST /api/family`
- **描述**: 创建一个新的家庭空间。用户必须尚未加入任何家庭。
- **权限**: **需要认证**
- **请求体**:
  ```json
  {
    "name": "我的幸福一家"
  }
  ```
- **成功响应 (201 Created)**:
  ```json
  {
    "code": 201,
    "message": "Family created successfully.",
    "data": {
      "family": { "id": 1, "name": "我的幸福一家", "invite_code": "ABC123XYZ" }
    }
  }
  ```
- **错误响应 (409 Conflict)**: 用户已在一个家庭中。

### 4.2. 使用邀请码加入家庭
- **接口**: `POST /api/family/join`
- **描述**: 通过有效的邀请码加入一个已存在的家庭。用户必须尚未加入任何家庭。
- **权限**: **需要认证**
- **请求体**:
  ```json
  {
    "invite_code": "ABC123XYZ"
  }
  ```
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Successfully joined the family.",
    "data": {
      "family": { "id": 1, "name": "我的幸福一家" }
    }
  }
  ```
- **错误响应 (404 Not Found)**: 邀请码无效。
- **错误响应 (409 Conflict)**: 用户已在一个家庭中。

### 4.3. 获取我所在的家庭信息
- **接口**: `GET /api/family`
- **描述**: 获取当前用户所属的家庭信息。如果用户未加入家庭，返回null。
- **权限**: **需要认证**
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Family info retrieved successfully.",
    "data": {
      "family": { "id": 1, "name": "我的幸福一家", "invite_code": "ABC123XYZ" }
    }
  }
  ```

### 4.4. 离开当前家庭
- **接口**: `POST /api/family/leave`
- **描述**: 离开当前所在的家庭。
- **权限**: **需要认证**
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Successfully left the family.",
    "data": null
  }
  ```

---

## 5. 相册模块 (`/api/albums`)

### 5.1. 创建一个新相册
- **接口**: `POST /api/albums`
- **描述**: 在当前用户所在的家庭中创建一个新相册。
- **权限**: **需要认证**
- **请求体**:
  ```json
  {
    "name": "2025年春节",
    "description": "全家一起过大年"
  }
  ```
- **成功响应 (201 Created)**:
  ```json
  {
    "code": 201,
    "message": "Album created successfully.",
    "data": {
      "album": { "id": 1, "name": "2025年春节" }
    }
  }
  ```

### 5.2. 获取相册列表
- **接口**: `GET /api/albums`
- **描述**: 获取当前用户所在家庭的所有相册列表。
- **权限**: **需要认证**
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Albums retrieved successfully.",
    "data": {
      "albums": [
        { "id": 1, "name": "2025年春节", "photo_count": 58 },
        { "id": 2, "name": "云南之旅", "photo_count": 120 }
      ]
    }
  }
  ```

### 5.3. 向相册中添加照片
- **接口**: `POST /api/albums/<int:album_id>/photos`
- **描述**: 将一张或多张照片批量添加到一个相册中。
- **权限**: **需要认证**
- **请求体**:
  ```json
  {
    "photo_ids": [10, 11, 15]
  }
  ```
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "3 photo(s) added to album successfully.",
    "data": null
  }
  ```

### 5.4. 更新相册信息
- **接口**: `PUT /api/albums/<int:album_id>`
- **描述**: 更新相册的名称或描述。
- **权限**: **需要认证**
- **请求体**:
  ```json
  {
    "name": "2025年春节大团圆",
    "description": "修改后的描述"
  }
  ```
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Album updated successfully.",
    "data": {
      "album": { "id": 1, "name": "2025年春节大团圆" }
    }
  }
  ```

### 5.5. 删除相册
- **接口**: `DELETE /api/albums/<int:album_id>`
- **描述**: 删除一个相册 (不会删除相册中的照片)。
- **权限**: **需要认证** (用户只能删除自己创建的相册)。
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Album deleted successfully.",
    "data": null
  }
  ```

### 5.6. 从相册中移除照片
- **接口**: `DELETE /api/albums/<int:album_id>/photos`
- **描述**: 将一张或多张照片从相册中移除。
- **权限**: **需要认证**
- **请求体**:
  ```json
  {
    "photo_ids": [11, 15]
  }
  ```
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "2 photo(s) removed from album successfully.",
    "data": null
  }
  ```

---

## 6. 搜索模块 (`/api/search`)

### 6.1. 搜索照片
- **接口**: `GET /api/search/photos`
- **描述**: 根据指定条件搜索当前家庭的照片，支持多种过滤器和分页。
- **权限**: **需要认证**
- **查询参数**:
  - `uploader_id` (可选, `int`): 按上传者用户ID过滤。
  - `start_date` (可选, `YYYY-MM-DD`): 按上传日期的开始范围过滤 (包含当天)。
  - `end_date` (可选, `YYYY-MM-DD`): 按上传日期的结束范围过滤 (包含当天)。
  - `keywords` (可选, `string`): 在照片文件名中搜索关键词 (不区分大小写)。
  - `page` (可选, `int`): 页码, 默认 `1`。
  - `per_page` (可选, `int`): 每页数量, 默认 `20`。
- **成功响应 (200 OK)**:
  ```json
  {
    "code": 200,
    "message": "Photos retrieved successfully.",
    "data": {
      "photos": [
        { 
          "id": 15, 
          "url": "/storage/photos/test_photo_14.jpg",
          "uploaded_at": "2025-07-26T12:00:00Z",
          "filename": "test_photo_14.jpg",
          "uploader": {
            "id": 1,
            "nickname": "user1"
          }
        }
      ],
      "pagination": {
        "page": 1,
        "per_page": 20,
        "total_pages": 5,
        "total_items": 98
      }
    }
  }
  ```

最后更新: 2025-07-19 | 版本: v0.1终极版