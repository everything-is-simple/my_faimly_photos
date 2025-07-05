# TODOLIST - 开发任务清单 (v0.1终极版)

**项目状态说明 (2025-07-19):** 本任务清单已根据 `docs/process/LOGS.md` 的记录进行了同步，以修正 `D003` 偏差导致的状态回滚。

本文档列出「家庭照片管理系统」核心开发任务。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: 活跃
**文档版本**: **v0.1终极版**

## 1. 任务状态

| 状态      | 说明             |
|:------- |:-------------- |
| [ ] 未开始 | 任务已定义但尚未开始     |
| [x] 已完成 | 任务已完成并通过测试     |
| [ ] 待联调 | 单端任务完成，等待前后端联调 |

---

## 第1阶段: 后端API开发 (Backend API Development)

### 1.1 项目初始化

- [x] **(BE-INIT)**: 初始化Python虚拟环境、安装依赖，并初始化后端Flask项目、配置SQLAlchemy及基础模型。

### 1.2 用户与认证模块 (Auth)

#### 任务BE-AUTH-01: 实现用户注册API [x] 已完成

- **描述**: 创建接收用户注册请求的API端点，负责验证输入、创建新用户并存入数据库。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-01)
  - `docs/design/API.md` (2.1. 用户注册)
  - `docs/design/ERD.md` (3.1. USERS表)
- **生成文件**:
  - `backend/app/routes/auth_routes.py`
  - `backend/app/services/user_service.py`
  - `backend/app/models/user_model.py`
- **修改文件**:
  - `backend/app/__init__.py` (注册Blueprint)
- **验证标准**:
  - [x] 接口能成功接收 `POST /api/auth/register` 请求。
  - [x] 请求体中的 `username` 和 `password` 字段会经过验证。
  - [x] 密码在存入数据库前必须经过哈希处理。
  - [x] 成功创建用户后，返回 `201` Created 状态码和新用户的信息。
  - [x] 如果用户名已存在，返回 `422 Unprocessable Entity` 错误。

#### 任务BE-AUTH-02: 实现用户登录API [ ]

- **描述**: 创建用户登录API端点，验证用户凭据并生成JWT。
- **参考文件**:
  - `docs/design/API.md` (2.2. 用户登录)
- **修改文件**:
  - `backend/app/routes/auth_routes.py`
  - `backend/app/services/user_service.py`
- **生成文件**:
  - `backend/app/utils/auth_utils.py`
- **验证标准**:
  - [ ] 接口能成功接收 `POST /api/auth/login` 请求。
  - [ ] 成功验证用户名和密码后，返回包含 `access_token` 和 `refresh_token` 的 `200 OK` 响应。
  - [ ] 如果凭据无效，返回 `401 Unauthorized` 错误。

#### 任务BE-AUTH-03: 实现JWT认证与用户信息获取API [ ]

- **描述**: 创建一个可复用的JWT认证装饰器或中间件，用于保护需要认证的API端点。并创建 `/api/auth/me` 端点用于获取当前用户信息，**包括其所属家庭ID**。
- **参考文件**:
  - `docs/design/API.md` (1.2. 认证机制, 2.5. 获取当前用户信息)
- **修改文件**:
  - `backend/app/routes/auth_routes.py`
- **验证标准**:
  - [ ] 访问受保护的API（如 `/api/photos`）时，若无有效 `Authorization` 头，会返回 `401 Unauthorized`。
  - [ ] 使用有效的 `access_token` 访问受保护API，可以正常处理请求。
  - [ ] 使用过期的 `access_token` 访问，会返回 `401 Unauthorized`。
  - [ ] 使用有效的 `access_token` 请求 `GET /api/auth/me`，能成功返回当前用户的基本信息（包括 `family_id`）。

####  任务BE-AUTH-04: 实现Token登出与刷新API [x] 已完成

- **描述**: 实现 `logout` 和 `refresh` 两个API端点，用于管理认证Token。
- **参考文件**:
  - `docs/design/API.md` (2.3. 用户登出, 2.4. 刷新认证Token)
- **修改文件**:
  - `backend/app/routes/auth_routes.py`
  - `backend/app/services/user_service.py`
- **验证标准**:
  - [ ] `POST /api/auth/logout` 能成功接收请求并使 `refresh_token` 失效。
  - [ ] `POST /api/auth/refresh` 能接收有效的 `refresh_token` 并返回一个新的 `access_token`。
  - [ ] 使用已登出或无效的 `refresh_token` 请求刷新，会返回 `401 Unauthorized`。

### 1.3 家庭管理模块 (Family)

#### 任务BE-FAMILY-01: 实现创建/加入/离开家庭API [x] 已完成

- **描述**: 实现家庭管理的完整API，包括创建新家庭、凭邀请码加入家庭、以及离开当前家庭。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-02, FUNC-03)
  - `docs/design/API.md` (4. 家庭模块)
  - `docs/design/ERD.md` (USERS, FAMILIES表)
- **生成文件**:
  - `backend/app/routes/family_routes.py`
  - `backend/app/services/family_service.py`
  - `backend/app/models/family_model.py`
- **修改文件**:
  - `backend/app/__init__.py` (注册Blueprint)
- **验证标准**:
  - [ ] `POST /api/family`: 成功在 `FAMILIES` 表中创建新记录，并更新当前用户的 `family_id`。如果用户已在家庭中，返回`409`。
  - [ ] `POST /api/family/join`: 根据有效邀请码，更新当前用户的 `family_id`。如果用户已在家庭中，返回`409`。
  - [ ] `POST /api/family/leave`: 成功将当前用户的 `family_id` 更新为 `NULL`。
  - [ ] `GET /api/family`: 成功返回当前用户所属家庭的信息。

### 1.4 照片管理模块 (Photo)

#### 任务BE-PHOTO-01: 实现照片上传API [x] 已完成

- **描述**: 创建API端点以处理`multipart/form-data`格式的照片上传请求，并将文件保存到服务器，元数据存入数据库。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-04)
  - `docs/design/API.md` (3.1. 上传一张或多张照片)
  - `docs/design/ERD.md` (3.4. PHOTOS表)
- **生成文件**:
  - `backend/app/routes/photo_routes.py`
  - `backend/app/services/photo_service.py`
  - `backend/app/models/photo_model.py`
- **修改文件**:
  - `backend/app/__init__.py` (注册Blueprint)
- **验证标准**:
  - [ ] 接口能成功接收 `POST /api/photos/upload` 请求。
  - [ ] 能处理单文件和多文件上传。
  - [ ] 照片文件被保存到指定的存储路径。
  - [ ] 每张照片的元数据被正确写入 `PHOTOS` 表。
  - [ ] 成功后返回 `201 Created` 及上传成功的照片列表。

#### 任务BE-PHOTO-02: 实现获取照片列表API [x] 已完成

- **描述**: 创建API端点以获取当前用户所在家庭的照片列表，支持分页。
- **参考文件**:
  - `docs/design/API.md` (3.2. 获取照片列表)
- **修改文件**:
  - `backend/app/routes/photo_routes.py`
  - `backend/app/services/photo_service.py`
- **验证标准**:
  - [ ] 接口能成功接收 `GET /api/photos` 请求。
  - [ ] **API能自动从用户Token中获取`family_id`，无需客户端传递。**
  - [ ] 返回的数据按 `uploaded_at` 降序排列。
  - [ ] 支持 `page` 和 `per_page` 查询参数，并返回正确的分页信息。

#### 任务BE-PHOTO-03: 实现获取单张照片详情API [x] 已完成

- **描述**: 创建API端点以获取指定ID的照片的详细信息。
- **参考文件**:
  - `docs/design/API.md` (3.3. 获取单张照片详情)
- **修改文件**:
  - `backend/app/routes/photo_routes.py`
  - `backend/app/services/photo_service.py`
- **验证标准**:
  - [ ] 接口能成功接收 `GET /api/photos/<id>` 请求。
  - [ ] 如果照片存在且用户有权查看，返回 `200 OK` 及照片的详细信息。
  - [ ] 如果照片不存在或用户无权查看，返回 `404 Not Found`。

#### 任务BE-PHOTO-04: 实现删除照片API [ ]

- **描述**: 实现照片的软删除。
- **参考文件**:
  - `docs/design/API.md` (3.4. 删除照片)
- **修改文件**:
  - `backend/app/routes/photo_routes.py`
  - `backend/app/services/photo_service.py`
- **验证标准**:
  - [ ] `DELETE /api/photos/<id>` 能将 `PHOTOS` 表中对应记录的 `is_deleted` 标记为 `true`。
  - [ ] **用户只能删除自己上传的照片，删除他人照片应返回 `403 Forbidden`。**
  - [ ] 被软删除的照片不会出现在常规的照片列表中。

### 1.5 相册管理模块 (Album)

#### 任务BE-ALBUM-01: 实现相册的增删改查API [ ]

- **描述**: 创建相册管理所需的一整套API，包括创建新相册、编辑相册信息、删除相册以及获取相册列表和详情。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-07, FUNC-08, FUNC-10)
  - `docs/design/API.md` (5. 相册模块)
  - `docs/design/ERD.md` (3.5. ALBUMS表)
- **生成文件**:
  - `backend/app/routes/album_routes.py`
  - `backend/app/services/album_service.py`
  - `backend/app/models/album_model.py`
- **修改文件**:
  - `backend/app/__init__.py` (注册Blueprint)
- **验证标准**:
  - [ ] `POST /api/albums`：能成功在当前用户所在的家庭中创建新相册。
  - [ ] `GET /api/albums`：能返回当前家庭的相册列表。
  - [ ] `PUT /api/albums/<id>`：**用户只能更新自己创建的相册**。
  - [ ] `DELETE /api/albums/<id>`：**用户只能删除自己创建的相册**。
  - [ ] `GET /api/albums/<id>`：能返回指定相册的详细信息及其包含的照片列表。

#### 任务BE-ALBUM-02: 实现向相册中添加/移除照片API [ ]

- **描述**: 创建API端点，支持将一批照片批量添加到一个相册，或从相册中移除。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-09)
  - `docs/design/API.md` (5.3. 向相册中添加照片)
  - `docs/design/ERD.md` (3.6. ALBUM_PHOTOS表)
- **修改文件**:
  - `backend/app/routes/album_routes.py`
  - `backend/app/services/album_service.py`
- **验证标准**:
  - [ ] `POST /api/albums/<id>/photos`：能成功地在 `ALBUM_PHOTOS` 表中创建多条关联记录。
  - [ ] `DELETE /api/albums/<id>/photos`：能成功地从 `ALBUM_PHOTOS` 表中删除多条关联记录。

### 1.6 智能检索模块 (Search)

#### 任务BE-SEARCH-01: 实现照片搜索API [x] 已完成

- **描述**: 创建一个综合搜索API，允许用户根据多种条件（上传者、日期、关键词等）查找照片。
- **参考文件**:
  - `docs/design/API.md` (6.1. 搜索照片)
- **生成文件**:
  - `backend/app/routes/search_routes.py`
  - `backend/app/services/search_service.py`
  - `backend/tests/routes/test_search_routes.py`
- **修改文件**:
  - `backend/app/__init__.py` (注册Blueprint)
  - `backend/app/models/photo_model.py` (在`to_dict`中添加`uploader`信息)
- **验证标准**:
  - [ ] `GET /api/search/photos` 接口能接收并正确解析 `start_date`, `end_date`, `uploader_id`, `keywords` 等查询参数。
  - [ ] **API能自动从用户Token中获取`family_id`，无需客户端传递。**
  - [ ] 能够根据单个或多个条件的组合正确返回结果。
  - [ ] 搜索结果支持分页。
  - [ ] 搜索范围严格限制在当前用户所在的家庭内。

---

## 第2阶段: 前端界面实现 (Frontend UI Implementation)

*(V1.0 MVP阶段，后端优先，前端任务将在此后定义)*

### 2.1 项目初始化

- [ ] **(FE-INIT)**: 初始化前端Vue项目、配置Vue Router、Pinia、Element Plus及Axios。

### 2.2 用户与认证模块 (Auth)

#### 任务FE-AUTH-01: 实现注册/登录页面 [ ]

- **描述**: 开发用户注册和登录的UI界面。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-01)
  - `docs/design/UI.md` (用户认证界面)
  - `docs/design/API.md` (2. 用户认证模块)
- **生成文件**:
  - `frontend/src/views/AuthView.vue`
  - `frontend/src/components/auth/RegisterForm.vue`
  - `frontend/src/components/auth/LoginForm.vue`
  - `frontend/src/services/auth_api.js`
  - `frontend/src/store/auth.js`
- **验证标准**:
  - [ ] 用户能输入用户名和密码进行注册。
  - [ ] 用户能输入用户名和密码进行登录。
  - [ ] 界面符合UI设计规范，具备基础的输入验证。

#### 任务FE-AUTH-02: 实现用户认证状态管理 [ ]

- **描述**: 在前端实现JWT Token的管理，包括安全存储、自动刷新、请求头注入以及全局状态同步。
- **参考文件**:
  - `docs/design/API.md` (1.2. 认证机制)
  - `docs/design/TRD.md` (4.3 API 通信)
- **修改文件**:
  - `frontend/src/services/api.js` (创建Axios拦截器)
  - `frontend/src/store/auth.js` (管理Token和用户状态)
  - `frontend/src/router/index.js` (路由守卫)
- **验证标准**:
  - [ ] 登录后 `access_token` 和 `refresh_token` 被安全存储。
  - [ ] Axios请求拦截器能自动在请求头中附加 `Authorization: Bearer <token>`。
  - [ ] Axios响应拦截器能在遇到401错误时，使用 `refresh_token` 自动刷新 `access_token` 并重试请求。
  - [ ] 用户信息（包括`family_id`）被存储在Pinia中，并在应用中同步。
  - [ ] 路由守卫能阻止未登录用户访问受保护页面。

### 2.3 家庭管理模块 (Family)

#### 任务FE-FAMILY-01: 实现家庭创建/加入/离开页面 [ ]

- **描述**: 开发创建家庭、通过邀请码加入家庭、以及离开家庭的UI界面。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-02, FUNC-03)
  - `docs/design/UI.md` (家庭管理界面)
  - `docs/design/API.md` (4. 家庭模块)
- **生成文件**:
  - `frontend/src/views/FamilyView.vue`
  - `frontend/src/components/family/CreateFamilyForm.vue`
  - `frontend/src/components/family/JoinFamilyForm.vue`
  - `frontend/src/components/family/LeaveFamilyForm.vue`
  - `frontend/src/services/family_api.js`
  - `frontend/src/store/family.js`
- **验证标准**:
  - [ ] 用户能填写表单创建新家庭。
  - [ ] 用户能输入邀请码加入家庭。
  - [ ] 用户能离开当前家庭。
  - [ ] 界面能显示当前用户所属家庭信息（如家庭名称、邀请码）。

### 2.4 照片管理模块 (Photo)

#### 任务FE-PHOTO-01: 实现照片上传界面 [ ]

- **描述**: 开发支持单张和多张照片上传的界面，包含进度条。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-04)
  - `docs/design/UI.md` (照片上传界面)
  - `docs/design/API.md` (3.1. 上传一张或多张照片)
- **生成文件**:
  - `frontend/src/components/photo/PhotoUpload.vue`
  - `frontend/src/services/photo_api.js`
- **验证标准**:
  - [ ] 用户能选择本地照片文件进行上传。
  - [ ] 上传过程有进度反馈。
  - [ ] 上传成功后有提示。

#### 任务FE-PHOTO-02: 实现照片瀑布流展示 [ ]

- **描述**: 开发主页照片瀑布流展示界面，支持时间倒序和分页加载。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-05)
  - `docs/design/UI.md` (UI-01 主页布局)
  - `docs/design/API.md` (3.2. 获取照片列表)
- **生成文件**:
  - `frontend/src/views/HomeView.vue`
  - `frontend/src/components/photo/PhotoGrid.vue`
- **验证标准**:
  - [ ] 主页能以瀑布流形式展示照片缩略图。
  - [ ] 照片按时间倒序排列。
  - [ ] 支持滚动加载或点击加载更多以实现分页。

#### 任务FE-PHOTO-03: 实现照片全屏浏览与详情 [ ]

- **描述**: 开发点击照片缩略图后进入全屏浏览模式的界面，并显示照片基本信息。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-06)
  - `docs/design/UI.md` (UI-02 照片浏览)
  - `docs/design/API.md` (3.3. 获取单张照片详情)
- **生成文件**:
  - `frontend/src/components/photo/PhotoDetailModal.vue`
- **验证标准**:
  - [ ] 点击照片能弹出全屏浏览模式。
  - [ ] 全屏模式下能左右切换照片。
  - [ ] 能显示照片的上传者、时间等信息。

#### 任务FE-PHOTO-04: 实现照片删除功能 [ ]

- **描述**: 在照片详情或管理界面添加删除照片的按钮。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-18)
  - `docs/design/API.md` (3.4. 删除照片)
- **修改文件**:
  - `frontend/src/components/photo/PhotoDetailModal.vue`
  - `frontend/src/components/photo/PhotoGrid.vue` (或相关照片管理组件)
- **验证标准**:
  - [ ] 用户能通过界面操作删除照片。
  - [ ] 删除后照片不再显示在瀑布流中。

### 2.5 相册管理模块 (Album)

#### 任务FE-ALBUM-01: 实现相册列表与创建/编辑界面 [ ]

- **描述**: 开发相册列表展示界面和创建/编辑相册的表单。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-07, FUNC-08, FUNC-10)
  - `docs/design/UI.md` (UI-03 相册管理)
  - `docs/design/API.md` (5. 相册模块)
- **生成文件**:
  - `frontend/src/views/AlbumView.vue`
  - `frontend/src/components/album/AlbumList.vue`
  - `frontend/src/components/album/AlbumForm.vue`
  - `frontend/src/services/album_api.js`
  - `frontend/src/store/album.js`
- **验证标准**:
  - [ ] 能展示相册列表，包括封面、名称、照片数量。
  - [ ] 用户能创建新相册。
  - [ ] 用户能编辑现有相册的名称和描述。
  - [ ] 用户能删除相册。

#### 任务FE-ALBUM-02: 实现相册详情与照片管理界面 [ ]

- **描述**: 开发相册详情页，显示相册内照片，并支持添加/移除照片。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-09, FUNC-10)
  - `docs/design/API.md` (5. 相册模块)
- **修改文件**:
  - `frontend/src/views/AlbumDetailView.vue`
  - `frontend/src/components/album/AlbumPhotoGrid.vue`
- **验证标准**:
  - [ ] 能查看特定相册内的所有照片。
  - [ ] 用户能将照片添加到相册。
  - [ ] 用户能从相册中移除照片。

### 2.6 智能检索模块 (Search)

#### 任务FE-SEARCH-01: 实现搜索界面与结果展示 [ ]

- **描述**: 开发包含时间、上传者、关键词等筛选条件的搜索界面，并展示搜索结果。
- **参考文件**:
  - `docs/design/PRD.md` (FUNC-15, FUNC-16, FUNC-17)
  - `docs/design/API.md` (6. 智能检索模块)
- **生成文件**:
  - `frontend/src/views/SearchView.vue`
  - `frontend/src/components/search/SearchBar.vue`
  - `frontend/src/components/search/SearchResults.vue`
  - `frontend/src/services/search_api.js`
- **验证标准**:
  - [ ] 界面能提供日期范围选择器。
  - [ ] 界面能提供上传者选择列表。
  - [ ] 界面能提供关键词输入框。
  - [ ] 搜索结果能以照片列表形式展示。

### 2.7 通用UI/UX

#### 任务FE-GENERAL-01: 实现通用布局与导航 [ ]

- **描述**: 统一前端应用布局，包括顶部导航栏、路由配置和响应式设计。
- **参考文件**:
  - `docs/design/UI.md` (UI-01 主页布局, NF-10 响应式设计)
- **生成文件**:
  - `frontend/src/App.vue`
  - `frontend/src/router/index.js`
  - `frontend/src/components/layout/NavBar.vue`
  - `frontend/src/assets/styles/main.css` (或scss)
- **验证标准**:
  - [ ] 应用具备统一的头部导航，包含Logo、家庭名称、成员按钮、上传按钮。
  - [ ] 路由配置正确，页面切换流畅。
  - [ ] 界面在不同设备（PC、手机）上能良好显示。

#### 任务FE-GENERAL-02: 实现基础错误处理与加载状态 [ ]

- **描述**: 为前端API请求添加统一的错误处理和加载状态显示。
- **参考文件**:
  - `docs/design/PRD.md` (NF-08 容错性)
- **修改文件**:
  - `frontend/src/services/api_client.js` (Axios拦截器)
  - `frontend/src/store/global.js` (全局状态)
- **验证标准**:
  - [ ] API请求失败时，能友好的提示用户。
  - [ ] 数据加载时，能显示加载动画或骨架屏。

---

## 第3阶段: 端到端联调与测试 (End-to-End Integration & Testing)

### 3.1 模块联调

#### 任务E2E-AUTH-01: 用户认证模块联调 [ ]

- **描述**: 联调前端注册/登录界面与后端认证API，确保用户注册、登录、JWT获取、刷新、自动认证和登出流程的端到端畅通。
- **参考文件**:
  - `docs/design/API.md` (2. 用户认证模块)
  - `docs/process/WORKFLOW.md` (端到端联调测试)
- **验证标准**:
  - [ ] 前端注册用户后，后端数据库能成功创建用户。
  - [ ] 前端登录成功后，能获取并存储有效的 `access_token` 和 `refresh_token`。
  - [ ] 刷新页面后，仍然能通过 `GET /api/auth/me` 成功获取用户信息（包括`family_id`）。
  - [ ] `access_token` 过期后，前端应能静默刷新Token并成功完成后续API请求。
  - [ ] 登出后，Token被清除，受保护的API无法访问。

#### 任务E2E-FAMILY-01: 家庭管理模块联调 [ ]

- **描述**: 联调前端家庭创建/加入/离开界面与后端家庭管理API。
- **参考文件**:
  - `docs/design/API.md` (4. 家庭模块)
- **验证标准**:
  - [ ] 前端创建家庭后，后端能成功创建家庭记录，且前端能获取到新的家庭信息。
  - [ ] 前端使用邀请码加入家庭后，用户与家庭关联成功。
  - [ ] 前端离开家庭后，用户的家庭信息被清空。
  - [ ] 界面能根据用户是否有所属家庭，正确显示创建/加入或离开家庭的选项。

#### 任务E2E-PHOTO-01: 照片管理模块联调 [ ]

- **描述**: 联调前端照片上传、展示、详情、删除功能与后端照片API，确保照片的完整生命周期管理。
- **参考文件**:
  - `docs/design/API.md` (3. 照片模块)
- **验证标准**:
  - [ ] 前端上传照片能成功保存到后端服务器和数据库。
  - [ ] 照片列表能正确从后端获取并展示，无需前端传递family_id。
  - [ ] 单张照片详情能正确显示。
  - [ ] 用户尝试删除他人照片时，界面会提示无权限。
  - [ ] 软删除的照片不再出现在常规照片列表中。

#### 任务E2E-ALBUM-01: 相册管理模块联调 [ ]

- **描述**: 联调前端相册列表、创建/编辑、详情、添加/移除照片功能与后端相册API。
- **参考文件**:
  - `docs/design/API.md` (5. 相册模块)
- **验证标准**:
  - [ ] 相册的增删改查功能端到端正常。
  - [ ] 用户无法编辑或删除他人创建的相册。
  - [ ] 能成功向相册添加和移除照片。
  - [ ] 相册详情能正确显示其包含的照片。

#### 任务E2E-SEARCH-01: 智能检索模块联调 [ ]

- **描述**: 联调前端搜索界面与后端搜索API，确保搜索功能端到端正常工作。
- **参考文件**:
  - `docs/design/API.md` (6. 智能检索模块)
- **验证标准**:
  - [ ] 前端发起带条件的搜索请求能正确返回后端结果。
  - [ ] 搜索结果在前端能正确展示。

### 3.2 最终测试与优化

#### 任务E2E-TEST-01: 全局功能测试 [ ]

- **描述**: 按照 `PRD.md` 中的功能列表，进行全面的端到端功能测试，确保所有MVP功能均符合预期。
- **参考文件**:
  - `docs/design/PRD.md`
