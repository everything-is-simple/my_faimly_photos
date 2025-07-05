# TODOLIST - 开发任务清单

本文档列出「家庭照片管理系统」前后端分离架构下的所有开发任务。

**作者**: 汪玮芸
**创建日期**: 2025-06-25
**最后更新**: 2025-07-08
**文档状态**: 活跃
**文档版本**: 完整版

## 1. 任务状态

| 状态 | 说明 |
| :--- | :--- |
| [ ] 未开始 | 任务已定义但尚未开始 |
| [ ] 进行中 | 任务正在进行中 |
| [ ] 已完成 | 任务已完成并通过测试 |
| [ ] 待联调 | 单端任务完成，等待前后端联调 |

---

## 第1阶段: 后端API开发 (Backend API Development)

### 1.1 项目初始化

-   [ ] **(BE)**: 初始化后端Flask项目、配置SQLAlchemy及基础模型。

### 1.2 用户与认证模块 (Auth)

#### 任务BE-AUTH-01: 实现用户注册API [ ]
-   **描述**: 创建接收用户注册请求的API端点，负责验证输入、创建新用户并存入数据库。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-01)
    -   `docs/design/API.md` (2.1. 用户注册)
    -   `docs/design/ERD.md` (3.1. USERS表)
-   **生成文件**:
    -   `backend/home_photo/routes/auth_routes.py`
    -   `backend/home_photo/services/user_service.py`
    -   `backend/home_photo/models/user_model.py`
-   **修改文件**:
    -   `backend/home_photo/__init__.py` (注册Blueprint)
-   **验证标准**:
    -   [ ] 接口能成功接收 `POST /api/auth/register` 请求。
    -   [ ] 请求体中的 `username` 和 `password` 字段会经过验证。
    -   [ ] 密码在存入数据库前必须经过哈希处理。
    -   [ ] 成功创建用户后，返回 `201 Created` 状态码和新用户的信息。
    -   [ ] 如果用户名已存在，返回 `422 Unprocessable Entity` 错误。

#### 任务BE-AUTH-02: 实现用户登录API [ ]
-   **描述**: 创建用户登录API端点，验证用户凭据并生成JWT。
-   **参考文件**:
    -   `docs/design/API.md` (2.2. 用户登录)
-   **生成文件**: (无)
-   **修改文件**:
    -   `backend/home_photo/routes/auth_routes.py`
    -   `backend/home_photo/services/user_service.py`
-   **验证标准**:
    -   [ ] 接口能成功接收 `POST /api/auth/login` 请求。
    -   [ ] 成功验证用户名和密码后，返回包含JWT的 `200 OK` 响应。
    -   [ ] 如果凭据无效，返回 `401 Unauthorized` 错误。

#### 任务BE-AUTH-03: 实现JWT认证与用户信息获取API [ ]
-   **描述**: 实现Flask的认证中间件或装饰器，用于保护需要认证的API端点。并创建一个 `/api/auth/me` 端点用于获取当前用户信息。
-   **参考文件**:
    -   `docs/design/API.md` (1.2. 认证机制, 2.3. 获取当前用户信息)
-   **生成文件**:
    -   `backend/home_photo/utils/jwt_utils.py`
-   **修改文件**:
    -   `backend/home_photo/routes/auth_routes.py`
-   **验证标准**:
    -   [ ] 访问受保护的API（如 `/api/photos`）时不带有效JWT，会返回 `401 Unauthorized`。
    -   [ ] 携带有效JWT访问受保护API时，可以正常处理请求。
    -   [ ] 携带有效JWT请求 `GET /api/auth/me`，能成功返回当前用户的基本信息。
    -   [ ] 如果凭据无效，返回 `401 Unauthorized` 错误。

### 1.3 家庭管理模块 (Family)

#### 任务BE-FAMILY-01: 实现创建家庭API [ ]
-   **描述**: 允许认证用户创建一个新的家庭空间，并自动成为该家庭的管理员。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-02)
    -   `docs/design/API.md` (4.1. 创建一个新家庭)
    -   `docs/design/ERD.md` (3.2. FAMILIES表, 3.3. USER_FAMILIES表)
-   **生成文件**:
    -   `backend/home_photo/routes/family_routes.py`
    -   `backend/home_photo/services/family_service.py`
    -   `backend/home_photo/models/family_model.py`
-   **修改文件**:
    -   `backend/home_photo/__init__.py` (注册Blueprint)
-   **验证标准**:
    -   [ ] 接口能成功接收 `POST /api/families` 请求。
    -   [ ] 必须为认证用户。
    -   [ ] 成功在 `FAMILIES` 表中创建新记录，并生成唯一的 `invite_code`。
    -   [ ] 成功在 `USER_FAMILIES` 表中将创建者与新家庭关联，并设置角色为 `admin`。
    -   [ ] 返回 `201 Created` 和新家庭的信息。

#### 任务BE-FAMILY-02: 实现通过邀请码加入家庭API [x]
-   **描述**: 允许认证用户使用有效的邀请码加入一个已存在的家庭。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-03)
    -   `docs/design/API.md` (4.2. 使用邀请码加入家庭)
    -   `docs/design/ERD.md` (3.3. USER_FAMILIES表)
-   **修改文件**:
    -   `backend/home_photo/routes/family_routes.py`
    -   `backend/home_photo/services/family_service.py`
-   **验证标准**:
    -   [ ] 接口能成功接收 `POST /api/families/join` 请求。
    -   [ ] 必须为认证用户。
    -   [ ] 如果 `invite_code` 无效或不存在，返回 `404 Not Found`。
    -   [ ] 如果用户已在该家庭，返回 `409 Conflict`。
    -   [ ] 成功在 `USER_FAMILIES` 表中创建关联记录，角色为 `member`。
    -   [ ] 返回 `200 OK` 和所加入家庭的信息。

### 1.4 照片管理模块 (Photo)

#### 任务BE-PHOTO-01: 实现照片上传API [x]
-   **描述**: 创建API端点以处理`multipart/form-data`格式的照片上传请求，并将文件保存到服务器，元数据存入数据库。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-04)
    -   `docs/design/API.md` (3.1. 上传一张或多张照片)
    -   `docs/design/ERD.md` (3.4. PHOTOS表)
-   **生成文件**:
    -   `backend/home_photo/routes/photo_routes.py`
    -   `backend/home_photo/services/photo_service.py`
    -   `backend/home_photo/models/photo_model.py`
-   **修改文件**:
    -   `backend/home_photo/__init__.py` (注册Blueprint)
-   **验证标准**:
    -   [ ] 接口能成功接收 `POST /api/photos/upload` 请求。
    -   [ ] 能处理单文件和多文件上传。
    -   [ ] 照片文件被保存到指定的存储路径，并生成缩略图。
    -   [ ] 每张照片的元数据被正确写入 `PHOTOS` 表。
    -   [ ] 成功后返回 `201 Created` 及上传成功的照片列表。

#### 任务BE-PHOTO-02: 实现获取照片列表API [x]
-   **描述**: 创建API端点以获取当前用户所在家庭的照片列表，支持分页。
-   **参考文件**:
    -   `docs/design/API.md` (3.2. 获取照片列表)
-   **修改文件**:
    -   `backend/home_photo/routes/photo_routes.py`
    -   `backend/home_photo/services/photo_service.py`
-   **验证标准**:
    -   [x] 接口能成功接收 `GET /api/photos` 请求。
    -   [x] 返回的数据按 `uploaded_at` 降序排列。
    -   [x] 支持 `page` 和 `per_page` 查询参数，并返回正确的分页信息。

#### 任务BE-PHOTO-03: 实现获取单张照片详情API [ ]
-   **描述**: 创建API端点以获取指定ID的照片的详细信息。
-   **参考文件**:
    -   `docs/design/API.md` (3.3. 获取单张照片详情)
-   **修改文件**:
    -   `backend/home_photo/routes/photo_routes.py`
    -   `backend/home_photo/services/photo_service.py`
-   **验证标准**:
    -   [ ] 接口能成功接收 `GET /api/photos/<id>` 请求。
    -   [ ] 请求必须经过认证。
    -   [ ] 如果照片存在且用户有权查看，返回 `200 OK` 及照片的详细信息。
    -   [ ] 如果照片不存在或用户无权查看，返回 `404 Not Found`。

#### 任务BE-PHOTO-04: 实现删除与恢复照片API [ ]
-   **描述**: 实现照片的软删除 (移入回收站) 和从回收站恢复的功能。
-   **参考文件**:
    -   `docs/design/API.md` (3.4. 删除照片, 3.5. 从回收站恢复照片)
    -   `docs/design/ERD.md` (3.5. DELETED_PHOTOS表)
-   **修改文件**:
    -   `backend/home_photo/routes/photo_routes.py`
    -   `backend/home_photo/services/photo_service.py`
-   **验证标准**:
    -   [ ] `DELETE /api/photos/<id>` 能将 `PHOTOS` 表中对应记录的 `is_deleted` 标记为 `true`。
    -   [ ] 删除操作会在 `DELETED_PHOTOS` 表中创建一条记录。
    -   [ ] `POST /api/photos/<id>/restore` 能将 `is_deleted` 标记改回 `false`。
    -   [ ] 被软删除的照片不会出现在常规的照片列表中。

### 1.5 相册管理模块 (Album)

#### 任务BE-ALBUM-01: 实现相册的增删改查API [ ]
-   **描述**: 创建相册管理所需的一整套API，包括创建新相册、编辑相册信息、删除相册以及获取相册列表和详情。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-07, FUNC-08, FUNC-10)
    -   `docs/design/API.md` (5. 相册模块)
    -   `docs/design/ERD.md` (3.6. ALBUMS表)
-   **生成文件**:
    -   `backend/home_photo/routes/album_routes.py`
    -   `backend/home_photo/services/album_service.py`
    -   `backend/home_photo/models/album_model.py`
-   **修改文件**:
    -   `backend/home_photo/__init__.py` (注册Blueprint)
-   **验证标准**:
    -   [ ] `POST /api/albums`：能成功创建新相册。
    -   [ ] `GET /api/albums`：能返回当前家庭的相册列表。
    -   [ ] `PUT /api/albums/<id>`：能成功更新指定相册的名称或描述。
    -   [ ] `DELETE /api/albums/<id>`：能成功删除指定相册（不删除照片）。
    -   [ ] `GET /api/albums/<id>`：能返回指定相册的详细信息及其包含的照片列表。

#### 任务BE-ALBUM-02: 实现向相册中添加/移除照片API [ ]
-   **描述**: 创建API端点，支持将一批照片批量添加到一个相册，或从相册中移除。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-09)
    -   `docs/design/API.md` (5.3. 向相册中添加照片)
    -   `docs/design/ERD.md` (3.7. ALBUM_PHOTOS表)
-   **修改文件**:
    -   `backend/home_photo/routes/album_routes.py`
    -   `backend/home_photo/services/album_service.py`
-   **验证标准**:
    -   [ ] `POST /api/albums/<id>/photos`：能成功地在 `ALBUM_PHOTOS` 表中创建多条关联记录。
    -   [ ] `DELETE /api/albums/<id>/photos`：能成功地从 `ALBUM_PHOTOS` 表中删除多条关联记录。
    -   [ ] 操作的原子性：如果部分photo_id无效，整个操作应回滚。

### 1.6 标签管理模块 (Tag)

#### 任务BE-TAG-01: 实现标签的增删改查API [ ]
-   **描述**: 创建标签管理所需的一整套API，包括创建新标签、删除标签以及获取当前家庭的所有标签。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-11, FUNC-13)
    -   `docs/design/API.md` (6. 标签模块)
    -   `docs/design/ERD.md` (3.8. TAGS表)
-   **生成文件**:
    -   `backend/home_photo/routes/tag_routes.py`
    -   `backend/home_photo/services/tag_service.py`
    -   `backend/home_photo/models/tag_model.py`
-   **修改文件**:
    -   `backend/home_photo/__init__.py` (注册Blueprint)
-   **验证标准**:
    -   [ ] `POST /api/tags`：能成功创建新标签，同一家庭内标签名不能重复。
    -   [ ] `GET /api/tags`：能返回当前家庭的所有标签列表。
    -   [ ] `DELETE /api/tags/<id>`：能成功删除指定标签，并清除所有 `PHOTO_TAGS` 中与此标签的关联。

#### 任务BE-TAG-02: 实现为照片打标签/移除标签API [ ]
-   **描述**: 创建API端点，支持为一张照片批量添加或移除多个标签。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-12)
    -   `docs/design/API.md` (6.3. 为照片打上标签)
    -   `docs/design/ERD.md` (3.9. PHOTO_TAGS表)
-   **修改文件**:
    -   `backend/home_photo/routes/tag_routes.py`
    -   `backend/home_photo/services/tag_service.py`
-   **验证标准**:
    -   [ ] `POST /api/photos/<id>/tags`：能成功地在 `PHOTO_TAGS` 表中为指定照片创建多条关联记录。
    -   [ ] `DELETE /api/photos/<id>/tags`：能成功地从 `PHOTO_TAGS` 表中删除指定照片的多条关联记录。

### 1.7 智能检索模块 (Search)

#### 任务BE-SEARCH-01: 实现多条件检索API [ ]
-   **描述**: 创建一个统一的、功能强大的搜索API，能根据时间范围、上传者、标签、关键词等多种条件组合筛选照片。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-15, FUNC-16, FUNC-17)
-   **生成文件**:
    -   `backend/home_photo/routes/search_routes.py`
    -   `backend/home_photo/services/search_service.py`
-   **修改文件**:
    -   `backend/home_photo/__init__.py` (注册Blueprint)
-   **验证标准**:
    -   [ ] `GET /api/search` 接口能接收并正确解析 `start_date`, `end_date`, `uploader_id`, `tag_ids`, `keywords` 等查询参数。
    -   [ ] 能够根据单个条件正确返回结果。
    -   [ ] 能够根据多个条件的组合（`AND` 逻辑）正确返回交集结果。
    -   [ ] 搜索结果支持分页。

---

## 第2阶段: 前端界面实现 (Frontend UI Implementation)

### 2.1 项目初始化与核心设置

#### 任务FE-CORE-01: 初始化前端项目及核心配置 [ ]
-   **描述**: 创建Vue.js项目，并集成Vite、Vue Router、Pinia、Element Plus和Axios等核心依赖，完成基础配置。
-   **参考文件**:
    -   `docs/design/TRD.md`
-   **生成文件**:
    -   整个 `frontend/` 项目结构。
-   **修改文件**:
    -   `frontend/vite.config.js`
    -   `frontend/src/main.js`
-   **验证标准**:
    -   [ ] `npm run dev` 能成功启动开发服务器。
    -   [ ] Element Plus 组件可以按需或全局引入并正常使用。
    -   [ ] Vue Router 和 Pinia 初始化成功。

#### 任务FE-CORE-02: 创建全局Axios实例和Store [ ]
-   **描述**: 创建一个全局的Axios实例用于所有API请求，配置请求拦截器自动附加JWT。创建Pinia的`authStore`来管理用户登录状态和Token。
-   **参考文件**:
    -   `docs/design/API.md` (1.2. 认证机制)
-   **生成文件**:
    -   `frontend/src/services/api.js`
    -   `frontend/src/store/authStore.js`
-   **验证标准**:
    -   [ ] `authStore` 能正确地保存和读取`localStorage`中的JWT。
    -   [ ] 发起API请求时，请求头能自动附带 `Authorization: Bearer <token>`。
    -   [ ] 当API返回401时，能自动清除本地token并重定向到登录页。

### 2.2 用户与认证流程

#### 任务FE-AUTH-01: 创建登录/注册视图 [ ]
-   **描述**: 开发用户登录和注册的UI界面，并将其连接到后端API。
-   **参考文件**:
    -   `docs/design/UI.md`
    -   `docs/design/API.md` (2.1, 2.2)
-   **生成文件**:
    -   `frontend/src/views/LoginView.vue`
    -   `frontend/src/views/RegisterView.vue`
    -   `frontend/src/services/authService.js` (封装API调用)
-   **修改文件**:
    -   `frontend/src/router/index.js` (添加路由)
-   **验证标准**:
    -   [ ] 用户可以在注册页面输入信息并成功调用注册API。
    -   [ ] 用户可以在登录页面输入凭据并成功调用登录API。
    -   [ ] 登录成功后，JWT被存储在`authStore`和`localStorage`中。
    -   [ ] 登录成功后，页面自动跳转到主页。
    -   [ ] 实现路由守卫，未登录用户访问受保护页面时，自动跳转到登录页。

### 2.3 核心照片展示

#### 任务FE-PHOTO-01: 创建主页视图与照片展示组件 [ ]
-   **描述**: 开发项目的主页/仪表盘，使用瀑布流布局展示照片。创建可复用的`PhotoCard`组件来显示单张照片的缩略图。
-   **参考文件**:
    -   `docs/design/UI.md` (UI-01)
    -   `docs/design/API.md` (3.2. 获取照片列表)
-   **生成文件**:
    -   `frontend/src/views/HomeView.vue`
    -   `frontend/src/components/PhotoCard.vue`
    -   `frontend/src/components/PhotoGrid.vue`
    -   `frontend/src/services/photoService.js`
-   **修改文件**:
    -   `frontend/src/router/index.js`
-   **验证标准**:
    -   [ ] `HomeView` 能成功调用照片列表API。
    -   [ ] 照片以瀑布流或网格形式正确展示。
    -   [ ] 页面滚动到底部时，能自动加载下一页数据（无限滚动）。
    -   [ ] 图片使用懒加载技术以优化性能。

#### 任务FE-PHOTO-02: 实现照片上传与删除功能 [ ]
-   **描述**: 开发照片上传的交互界面（如对话框），并允许用户在照片卡片上执行删除操作。
-   **参考文件**:
    -   `docs/design/UI.md`
    -   `docs/design/API.md` (3.1, 3.4)
-   **生成文件**:
    -   `frontend/src/components/UploadDialog.vue`
-   **修改文件**:
    -   `frontend/src/views/HomeView.vue` (集成上传按钮)
    -   `frontend/src/components/PhotoCard.vue` (集成删除按钮)
    -   `frontend/src/services/photoService.js`
-   **验证标准**:
    -   [ ] 点击上传按钮能弹出上传对话框。
    -   [ ] 用户可以使用 `el-upload` 或类似组件选择并上传照片。
    -   [ ] 上传成功后，照片列表能自动刷新。
    -   [ ] 点击照片上的删除按钮，调用删除API后，该照片能从视图中移除。

### 2.4 家庭、相册、标签与搜索

#### 任务FE-ADVANCED-01: 创建家庭与相册管理视图 [ ]
-   **描述**: 开发用于管理家庭（创建、邀请、查看成员）和相册（列表、创建、编辑、查看详情）的核心界面。
-   **参考文件**:
    -   `docs/design/UI.md` (UI-03)
    -   `docs/design/API.md` (4. 家庭模块, 5. 相册模块)
-   **生成文件**:
    -   `frontend/src/views/FamilyView.vue`
    -   `frontend/src/views/AlbumListView.vue`
    -   `frontend/src/views/AlbumDetailView.vue`
    -   `frontend/src/services/familyService.js`
    -   `frontend/src/services/albumService.js`
-   **修改文件**:
    -   `frontend/src/router/index.js`
-   **验证标准**:
    -   [ ] 用户可以创建新的家庭。
    -   [ ] 用户可以展示邀请码，并使用邀请码加入其他家庭。
    -   [ ] 相册以网格形式展示，包含封面、名称和照片数量。
    -   [ ] 用户可以创建、修改和删除相册。
    -   [ ] 点击相册可以进入详情页，查看该相册内的所有照片。

#### 任务FE-ADVANCED-02: 实现照片的分类与标签管理交互 [ ]
-   **描述**: 实现将照片添加到相册的交互（如拖拽、或在选择模式下批量添加），以及在照片详情页中管理照片的标签。
-   **参考文件**:
    -   `docs/design/PRD.md` (FUNC-09, FUNC-12)
    -   `docs/design/API.md` (5.3, 6.3)
-   **修改文件**:
    -   `frontend/src/views/HomeView.vue` (添加"选择模式")
    -   `frontend/src/views/AlbumDetailView.vue`
    -   `frontend/src/components/PhotoDetailDialog.vue` (或类似的照片详情组件)
-   **验证标准**:
    -   [ ] 在主页，用户可以进入一个"选择模式"，批量选中多张照片。
    -   [ ] 在选择模式下，可以将选中的照片一次性添加到一个或多个相册中。
    -   [ ] 在照片的详情弹窗或页面中，可以展示当前照片已有的标签。
    -   [ ] 用户可以在详情页为照片添加新的标签（从标签列表中选择或新建）或移除已有标签。

#### 任务FE-ADVANCED-03: 创建多功能搜索界面 [ ]
-   **描述**: 开发一个集成的搜索面板或页面，允许用户通过时间、上传者、标签和关键词等多种条件组合进行搜索。
-   **参考文件**:
    -   `docs/design/API.md` (相关的Search API)
-   **生成文件**:
    -   `frontend/src/views/SearchView.vue`
    -   `frontend/src/services/searchService.js`
-   **修改文件**:
    -   `frontend/src/components/layout/Header.vue` (添加搜索入口)
-   **验证标准**:
    -   [ ] 搜索界面提供日期选择器、成员选择器、标签选择器和关键词输入框。
    -   [ ] 用户设置筛选条件后，点击搜索能正确调用后端API并展示结果。
    -   [ ] 搜索结果页的展现形式与主页的照片瀑布流保持一致。

---

## 第3阶段: 端到端联调与测试

#### 任务E2E-01: 核心认证与照片流联调 [ ]
-   **描述**: 确保最核心的用户流程和数据展示流程在前后端贯通。
-   **范围**: (BE+FE)
-   **涉及模块**: 用户认证、照片管理
-   **验证标准**:
    -   [ ] 用户能完成从注册、登录、上传照片、在主页看到照片、删除照片的完整闭环。
    -   [ ] 所有操作的UI反馈（如加载状态、成功提示、错误信息）均符合预期。

#### 任务E2E-02: 家庭与相册管理联调 [ ]
-   **描述**: 确保家庭和相册相关的管理功能在前后端正确协作。
-   **范围**: (BE+FE)
-   **涉及模块**: 家庭管理、相册管理
-   **验证标准**:
    -   [ ] 用户A创建家庭后，用户B可以使用邀请码成功加入。
    -   [ ] 用户可以创建相册，并将自己有权查看的照片添加到相册中。
    -   [ ] 相册的增删改查操作结果能正确地在UI上反映出来。

#### 任务E2E-03: 分类与检索功能联调 [ ]
-   **描述**: 确保为照片打标签以及使用多功能搜索的流程在前后端正确贯通。
-   **范围**: (BE+FE)
-   **涉及模块**: 标签管理、智能检索
-   **验证标准**:
    -   [ ] 用户可以为照片添加和移除标签，结果在照片详情和标签列表页正确更新。
    -   [ ] 搜索界面能使用多个筛选条件（时间、标签、关键词等）组合，并得到正确的、经过后台筛选的结果。

---
最后更新: 2025-07-06 | 版本: 规格 V1.0 