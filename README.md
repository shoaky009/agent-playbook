# Agent Playbook

个人 AI 协作规则与 skills，供 Codex、Pi Coding Agent（pi）和 Oh My Pi（omp）共用，通过 Git 在不同开发环境间同步。

## 内容

```text
agent-playbook/
├── AGENTS.md                             # 全局协作原则：自主判断、任务质量、沟通方式
├── skills/
│   ├── frontend-craft/SKILL.md            # 前端页面、组件和视觉设计规范
│   ├── pragmatic-refactor/SKILL.md        # 保持行为和契约的务实重构原则
│   └── shoaky-kotlin-style/SKILL.md       # Kotlin、Spring、持久化、API 文档和缓存约定
└── scripts/
    └── install.py                        # 安装全局规则和共享 skills
```

## 全局规则的安装位置

仓库只维护一份 `AGENTS.md`，安装时将同一份内容复制到所选 agent 的全局规则目录：

| Agent | 默认安装位置 | 自定义目录参数 |
| --- | --- | --- |
| Codex | `~/.codex/AGENTS.md` | `--codex-home` |
| pi | `~/.pi/agent/AGENTS.md` | `--pi-agent-dir` |
| omp | `~/.omp/agent/AGENTS.md` | `--omp-agent-dir` |

三个 skills 统一安装到 `~/.agents/skills/<skill-name>/`。`--agent` 控制全局规则的安装对象，共享 skills 每次只安装一份。

## 安装

需要 Python 3，无第三方依赖。在目标环境下载或克隆本仓库后，进入仓库根目录执行：

```sh
# 预览三个 agent 的安装计划，不写入文件
python3 scripts/install.py --dry-run

# 默认给 Codex、pi、omp 安装相同的全局规则，并安装共享 skills
python3 scripts/install.py

# 也可以只给某个 agent 安装全局规则，同时安装共享 skills
python3 scripts/install.py --agent pi
python3 scripts/install.py --agent omp
python3 scripts/install.py --agent codex
```

`--agent all` 与默认行为相同。安装后重启对应 agent，或开启新会话加载全局规则。

内容相同时跳过；内容不同时先备份，再复制仓库版本：

- 全局规则备份到各自安装目录下的 `backups/agent-playbook/<UTC 时间戳>/AGENTS.md`。
- skills 备份到 `~/.agents/backups/agent-playbook/<UTC 时间戳>/skills/`；使用 `--skills-dir` 时，备份位于该目录的同级 `backups/` 下。

使用自定义目录的环境可显式指定安装位置：

```sh
python3 scripts/install.py \
  --codex-home /path/to/codex-home \
  --pi-agent-dir /path/to/pi-agent \
  --omp-agent-dir /path/to/omp-agent \
  --skills-dir /path/to/agent-skills
```

设置 `CODEX_HOME` 时，脚本默认使用该目录安装 Codex 全局规则。pi 和 omp 如通过环境变量或 profile 改过目录，请分别用 `--pi-agent-dir` 和 `--omp-agent-dir` 指定实际目录。`--skills-dir` 是复制目标，应使用 agent 支持的扫描目录。

## 日常同步

直接在本仓库修改 `AGENTS.md` 或 `skills/` 下的文件，将更改通过 Git 同步到其他环境后，再执行安装脚本。安装目录中的本地修改需要先手动同步回仓库。

如需恢复旧版本，从脚本输出的备份路径取回对应文件或 skill 目录，放回原安装位置。

