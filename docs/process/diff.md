# 偏差记录 (Plan vs Reality)

本文档用于记录开发过程中出现的、在`LOGS.md`中标记为 **[DEVIATION]** 的重大偏差。

**作者**: 汪玮芸
**创建日期**: 2025-06-20
**最后更新**: 2025-07-19
**文档状态**: "活跃"
**文档版本**: "**v0.1终极版**"

**核心原则**: 偏差零容忍。一旦出现偏差，必须优先解决。

---

## 偏差记录格式

每个偏差记录应包含以下部分：

- **偏差ID**: 一个唯一的标识符 (例如 `D001`)
- **发现日期**: `YYYY-MM-DD`
- **偏差类型**:
    - `TASK`: 任务执行偏差 (`TODOLIST.md` vs `LOGS.md`)
    - `DIR`: 目录结构偏差 (`plan-DIR.md` vs `work_directory.md`)
    - `WORKFLOW`: 工作流程执行偏差 (e.g., Git仓库未初始化)
- **涉及任务**: `TODOLIST.md` 中的任务ID
- **计划 (Plan)**: 描述预期的状态（来自权威文档）。
- **现实 (Reality)**: 描述实际出现的状态。
- **根本原因分析 (RCA)**: 分析导致偏差的根本原因。
- **解决方案**: 为消除偏差所采取的具体步骤。
- **状态**: `OPEN` | `CLOSED`

---

## 偏差列表

### D003: 项目状态因Git问题严重回滚
- **发现日期**: 2025-07-18
- **偏差类型**: `WORKFLOW`
- **涉及任务**: `BE-SEARCH-01` (任务后)
- **计划 (Plan)**: 在 `BE-SEARCH-01` 任务完成后，代码和文档应处于已验证、已记录的稳定状态。
- **现实 (Reality)**: 在尝试提交和合并代码时，遇到了一系列无法解决的Git错误（怀疑是工作区或索引损坏）。后续的恢复操作导致项目意外回滚，所有与 `BE-SEARCH-01` 相关的代码和文档变更全部丢失。
- **根本原因分析 (RCA)**: Git的本地工作区或索引可能已损坏，导致标准的`merge`, `clean`, `reset`等命令均无法解决冲突。这是一个深层次的工具链问题，而非简单的代码冲突。
- **解决方案**:
    1.  **识别偏差**: 确认了代码和文档已回滚到旧状态，这是一个必须立即解决的严重偏差。
    2.  **系统性恢复代码**: 由AI根据历史记录，重新创建了`search_service.py`, `search_routes.py`, `test_search_routes.py`等文件，并恢复了对`photo_model.py`和`__init__.py`的修改。
    3.  **修复依赖问题**: 为解决`__init__.py`中的`ImportError`，创建了一个临时的占位文件 `album_routes.py`。
    4.  **验证恢复**: 运行了完整的`pytest`测试套件，确认所有44个测试全部通过，证明代码已成功恢复。
    5.  **系统性恢复文档**: 重新更新了`API.md`, `TODOLIST.md`, `LOGS.md`, `work_directory.md`，使其与恢复后的代码状态保持一致。
    6.  **记录偏差**: 在本文件 (`diff.md`) 中记录了此事件的全过程。
- **状态**: CLOSED

### D002: 项目未初始化为Git仓库
- **发现日期**: 2025-07-12
- **偏差类型**: `WORKFLOW`
- **涉及任务**: `BE-AUTH-04`
- **计划 (Plan)**: 根据 `WORKFLOW.md`，所有开发活动都应遵循基于Git的分支模型和提交规范。
- **现实 (Reality)**: 项目目录不是一个Git仓库，无法执行任何 `git` 命令，开发流程被阻塞。
- **根本原因分析 (RCA)**: 项目初始设置时遗漏了 `git init` 步骤，导致整个版本控制系统缺失。
- **解决方案**:
    1. 在项目根目录执行 `git init` 初始化仓库。
    2. 执行 `git add .` 将所有现有文件添加到暂存区。
    3. 执行 `git commit -m "chore: initial commit of existing project structure"` 完成首次提交。
    4. 执行 `git branch -M main` 将主分支重命名为 `main`。
    5. 执行 `git checkout -b develop` 创建并切换到开发分支。
- **状态**: CLOSED

### D001: [示例] 数据库模型与ERD不一致
- **发现日期**: 2025-07-10
- **偏差类型**: `DIR`
- **涉及任务**: `T003`
- **计划 (Plan)**: `User` 模型应包含 `email` 字段，根据 `ERD.md` v1.2。
- **现实 (Reality)**: `backend/app/models/user_model.py` 中的 `User` 模型缺少 `email` 字段。
- **根本原因分析 (RCA)**: 开发者在执行任务 `T003` 时遗漏了对 `ERD.md` 的最新更新的检查。
- **解决方案**:
    1. 为 `User` 模型添加 `email` 字段。
    2. 创建新的数据库迁移脚本。
    3. 执行迁移。
    4. 更新对应的单元测试。
- **状态**: CLOSED

--- 