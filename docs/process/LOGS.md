# 开发日志

本文档记录「家庭照片管理系统」项目的关键开发决策和历程。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: "活跃"
**文档版本**: "**v0.1终极版**"

---

## 2025-07-05

### 任务: (BE-INIT) 初始化后端项目

- **执行者**: AI助手
- **变更**:
  - 创建了 `backend/` 目录结构，遵循 `docs/process/plan-DIR.md`。
  - 创建了 `backend/requirements.txt` 并定义了核心依赖。
  - 创建了 `backend/config.py` 用于项目配置。
  - 创建了 `backend/run.py` 作为应用启动脚本。
  - 初始化了Flask应用工厂 `backend/app/__init__.py`，并配置了SQLAlchemy, Migrate, Bcrypt扩展。
  - 根据 `docs/design/ERD.md` 创建了基础数据模型 (`User`, `Family`, `Photo`, `Album`)。
- **决策**:
  - 使用 `Flask-Bcrypt` 库进行密码哈希处理。
  - 采用 `python-dotenv` 管理环境变量，以区分开发和生产配置。
  - 默认数据库配置为 `SQLite` 以简化本地开发环境。
- **状态**: 任务进行中。下一步是创建虚拟环境并安装依赖。

## 2025-07-18: BE-SEARCH-01 - 实现照片搜索API
- **日期**: 2025-07-18
- **操作人**: AI Assistant
- **任务ID**: BE-SEARCH-01
- **描述**:
  - [RECOVERY]: 此任务是在项目状态意外回滚后恢复的。
  - [TDD-RED]: 重新创建了 `backend/tests/routes/test_search_routes.py`，并编写了一套全面的失败测试。
  - [TDD-GREEN]: 重新创建了 `backend/app/services/search_service.py` 和 `backend/app/routes/search_routes.py`。
  - [TDD-GREEN]: 在 `backend/app/__init__.py` 中注册了 `search_bp` 蓝图。
  - [DEBUG]: 恢复了 `photo_model.py` 中的 `to_dict` 方法，以包含 `uploader` 的详细信息。
  - [TDD-GREEN]: 成功让所有测试通过。
- **状态**: 已完成
- **关联文件**:
  - `backend/app/routes/search_routes.py`
  - `backend/app/services/search_service.py`
  - `backend/tests/routes/test_search_routes.py`
  - `backend/app/models/photo_model.py`
- **偏差记录**:
  - 关联偏差 `D003`

## 2025-07-15: BE-PHOTO-03 - 实现获取单张照片详情API
- **日期**: 2025-07-15
- **操作人**: AI Assistant
- **任务ID**: BE-PHOTO-03
- **描述**:
  - [SETUP]: 为此功能创建了 `feature/backend/get-photo-detail-api` Git分支。
  - [TDD-RED]: 在 `test_photo_routes.py` 中新增了 `TestGetPhotoById` 测试类，包含5个失败的测试用例，覆盖了未授权、照片未找到、跨家庭数据隔离、软删除照片以及成功获取等场景。
  - [TDD-GREEN]: 在 `photo_service.py` 中添加了 `get_photo_by_id` 方法，实现了获取照片详情的核心业务逻辑，包括权限检查。
  - [TDD-GREEN]: 在 `photo_routes.py` 中添加了 `GET /api/photos/<int:photo_id>` API端点，并使用 `@token_required` 装饰器进行保护。
  - [DEBUG]: 修复了 `photo_service.py` 中因未能正确过滤软删除照片而导致的测试失败。
  - [REFACTOR]: 将 `photo_service.py` 中过时的 `User.query.get()` 调用重构为 `db.session.get()`，消除了 `LegacyAPIWarning`。
  - [TDD-GREEN]: 成功让所有17个测试用例通过。
  - [DOCS]: 更新了 `TODOLIST.md` 中的任务状态。
- **状态**: 已完成
- **关联文件**:
  - `docs/process/TODOLIST.md`
  - `backend/tests/routes/test_photo_routes.py`
  - `backend/app/services/photo_service.py`
  - `backend/app/routes/photo_routes.py`
- **偏差记录**:
  - 无

## 2025-07-15: BE-PHOTO-02 - 实现获取照片列表API
- **日期**: 2025-07-15
- **操作人**: AI Assistant
- **任务ID**: BE-PHOTO-02
- **描述**:
  - [SETUP]: 为此功能创建了 `feature/backend/get-photos-list-api` Git分支。
  - [TDD-RED]: 在 `conftest.py` 中新增了一个 `family_with_photos` fixture，用于创建包含多个用户和15张具有不同上传时间的照片的复杂测试场景。
  - [TDD-RED]: 在 `test_photo_routes.py` 中添加了一个新的测试类 `TestGetPhotos`，包含6个失败的测试用例，覆盖了未授权、无家庭用户、空家庭、成功获取、排序正确性、分页功能以及数据隔离等多种场景。
  - [TDD-GREEN]: 对 `photo_service.py` 进行了重构，创建了 `PhotoService` 类，并将 `save_photos` 和新增的 `get_photos_by_family` 函数作为静态方法移入其中，以保证项目代码风格的一致性。
  - [TDD-GREEN]: 相应地，更新了 `photo_routes.py` 中的上传路由以调用 `PhotoService.save_photos`。
  - [TDD-GREEN]: 在 `photo_routes.py` 中实现了 `GET /api/photos` API端点，该端点能自动从用户Token中获取`family_id`，处理分页参数，并调用服务层获取数据。
  - [TDD-GREEN]: 在 `__init__.py` 中更新了 `photo_bp` 蓝图的注册方式。
  - [DEBUG]: 在 `photo_model.py` 中为 `Photo` 模型添加了 `to_dict` 方法，解决了在路由中序列化对象时发生的 `AttributeError`。
  - [TDD-GREEN]: 成功让所有34个测试用例通过。
  - [DOCS]: 更新了 `TODOLIST.md` 中的任务状态。
- **状态**: 已完成
- **关联文件**:
  - `docs/process/TODOLIST.md`
  - `backend/tests/conftest.py`
  - `backend/tests/routes/test_photo_routes.py`
  - `backend/app/services/photo_service.py`
  - `backend/app/routes/photo_routes.py`
  - `backend/app/models/photo_model.py`
  - `backend/app/__init__.py`
- **偏差记录**:
  - 无

## 2025-07-14: BE-PHOTO-01 - 实现照片上传API
- **日期**: 2025-07-14
- **操作人**: AI Assistant
- **任务ID**: BE-PHOTO-01
- **描述**:
  - [SETUP]: 为此功能创建了 `feature/backend/photo-upload-api` Git分支。
  - [SETUP]: 在 `conftest.py` 中为测试环境配置了一个临时的 `UPLOAD_FOLDER`，以确保测试的隔离性和上传文件的自动清理。
  - [TDD-RED]: 创建了 `test_photo_routes.py`，其中包含6个初始失败的测试用例，覆盖了从未授权访问、用户家庭状态检查、请求文件存在性验证到单/多文件成功上传等多种场景。
  - [DEBUG]: 对测试环境进行了多轮调试，解决了包括 `fixture 'db' not found`、`AttributeError`、装饰器 `TypeError` 以及 `ValueError: I/O operation on closed file` 在内的一系列问题。
  - [DEBUG]: 通过改进 `conftest.py` 中的 `user_in_family_details` fixture，在测试清理阶段优先删除关联的照片，解决了因外键约束导致的 `IntegrityError`。
  - [TDD-GREEN]: 创建了 `photo_service.py`，负责处理文件保存（使用UUID确保文件名唯一）和数据库记录创建的核心业务逻辑。
  - [TDD-GREEN]: 创建了 `photo_routes.py` 并注册了相应的蓝图，实现了 `/api/photos/upload` API端点，将路由、服务和响应格式化连接在一起。
  - [REFACTOR]: 对 `photo_service.py` 进行了微重构，将存入数据库的 `storage_path` 从完整的绝对路径修改为仅文件名，以增强系统的灵活性。
  - [DOCS]: 更新了 `TODOLIST.md` 中的任务状态。
- **状态**: 已完成
- **关联文件**:
  - `docs/process/TODOLIST.md`
  - `backend/app/routes/photo_routes.py`
  - `backend/app/services/photo_service.py`
  - `backend/tests/routes/test_photo_routes.py`
  - `backend/tests/conftest.py`
  - `backend/app/__init__.py`
- **偏差记录**:
  - 无

## 2025-07-13: BE-FAMILY-01 - 实现创建/加入/离开家庭API
- **日期**: 2025-07-13
- **操作人**: AI Assistant
- **任务ID**: BE-FAMILY-01
- **描述**:
  - [TDD-RED]: 在 `backend/tests/routes/` 下创建了 `test_family_routes.py` 并编写了9个失败的测试用例，覆盖了创建、加入、获取、离开家庭的各种场景。
  - [DEBUG]: 修复了因 `app.models` 目录缺少 `__init__.py` 文件导致的 `ImportError`。
  - [DEBUG]: 修复了 `conftest.py` 中因 `DetachedInstanceError` 导致的测试 `fixture` 错误，方法是在 `db.session.commit()` 后添加 `db.session.refresh()`。
  - [TDD-GREEN]: 在 `app/services/` 下创建了 `family_service.py` 用于处理家庭管理的业务逻辑。
  - [TDD-GREEN]: 在 `app/routes/` 下创建了 `family_routes.py` 来定义家庭模块的API端点。
  - [TDD-GREEN]: 在 `app/__init__.py` 中注册了 `family` 蓝图。
  - [REFACTOR]: 重构了 `family_service.py` 和 `test_family_routes.py`，将旧的 `Model.query.get(id)` 调用替换为推荐的 `db.session.get(Model, id)` 写法，消除了 `LegacyAPIWarning`。
  - [DOCS]: 更新了 `TODOLIST.md` 和 `work_directory.md`，并为本项目添加了日志。
- **状态**: 已完成
- **关联文件**:
  - `docs/process/TODOLIST.md`
  - `docs/process/work_directory.md`
  - `backend/app/routes/family_routes.py`
  - `backend/app/services/family_service.py`
  - `backend/tests/routes/test_family_routes.py`
  - `backend/tests/conftest.py`
  - `backend/app/models/__init__.py`
  - `backend/app/__init__.py`
- **偏差记录**:
  - 无

## 2025-07-12: BE-AUTH-04 - 实现Token登出与刷新API
- **日期**: 2025-07-12
- **操作人**: AI Assistant
- **任务ID**: BE-AUTH-04
- **描述**:
  - [DEVIATION]: 在任务开始前，发现项目未被初始化为Git仓库，这与工作流严重不符。优先解决了此偏差，初始化了Git仓库并创建了`main`和`develop`分支。此偏差已记录在`diff.md` (D002)。
  - [TDD-RED]: 为登出和刷新功能创建了`TokenBlocklist`模型及相应的数据库迁移脚本。
  - [TDD-RED]: 在`test_auth_routes.py`中为登出、刷新成功、刷新失败等场景编写了4个失败的测试用例。
  - [TDD-GREEN]: 在`auth_utils.py`中为刷新Token添加了`jti`声明和黑名单检查逻辑。
  - [TDD-GREEN]: 在`user_service.py`中添加了`logout_user`和`refresh_access_token`方法。
  - [TDD-GREEN]: 在`auth_routes.py`中添加了`/logout`和`/refresh`端点。
  - [DEBUG]: 通过在测试用例中加入`time.sleep(1)`，解决了因JWT `iat`声明相同而导致的刷新测试断言失败问题。
  - [REFACTOR]: 将`auth_utils.py`中的`User.query.get()`重构为 SQLAlchemy 2.0 推荐的 `db.session.get()`，消除了`LegacyAPIWarning`。
  - [DOCS]: 更新了`TODOLIST.md`，将任务标记为完成。
  - [DOCS]: 更新了`work_directory.md`，添加了新创建的文件记录。
- **状态**: 已完成
- **关联文件**:
  - `docs/process/diff.md`
  - `docs/process/TODOLIST.md`
  - `docs/process/work_directory.md`
  - `backend/app/models/token_blocklist_model.py`
  - `backend/migrations/versions/a8172d685717_add_tokenblocklist_model.py`
  - `backend/app/utils/auth_utils.py`
  - `backend/app/services/user_service.py`
  - `backend/app/routes/auth_routes.py`
  - `backend/tests/routes/test_auth_routes.py`
- **偏差记录**:
  - `D002`: 项目未初始化为Git仓库。

## 2025-07-12: FT-AUTH-LOOP - 核心认证流程功能测试

- **日期**: 2025-07-12
- **操作人**: AI Assistant
- **任务ID**: FT-AUTH-LOOP (Functional Test for Auth Loop)
- **描述**:
  - [TEST]: 在 `