# 华为杯数学建模与论文写作 Skills

这是一套面向“中国研究生数学建模竞赛（华为杯）”的Skills，覆盖从读取赛题、逐问建模、Python 求解与验证，到依据建模证据撰写中文竞赛报告的完整流程。

仓库包含两个可以独立安装、也可以配合使用的技能：

| 技能                              | 调用名称                    | 作用                                                                                       |
| --------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------ |
| `math-modeling-huaweicup-skill` | `math-modeling-huaweicup` | 读取赛题、数据和官方规范，逐问建立模型，使用 Python 求解并生成代码、图表、结果表和验证证据 |
| `paper-writing-huaweicup-skill` | `paper-writing-huaweicup` | 基于题目、官方规范和已有建模成果，撰写、修改或审查中文竞赛报告                             |

## 主要作用

### 建模与求解

`math-modeling-huaweicup` 按照“读题—数据画像—逐问建模—编码求解—结果验证”的顺序工作，主要完成：

- 分解各个问题的目标、约束和依赖关系；
- 检查数据规模、字段、缺失值、异常值及时间或空间结构；
- 从题目机理和数据特征出发选择模型；
- 使用 Python 生成可复现的求解与绘图代码；
- 通过基线、误差、可行性、稳健性或灵敏度分析验证结果；
- 按 `Q1`、`Q2` 等问题编号归档代码、图片和表格；
- 生成供论文写作使用的结果说明和建模证据清单。

该技能不会负责论文正文写作，也不会按题型机械套用固定算法。

### 论文写作

`paper-writing-huaweicup` 读取已有建模成果并将其组织成竞赛报告，主要完成：

- 撰写完整报告或摘要、问题分析、模型建立、求解、验证、结论等指定章节；
- 按真实的推导和证据关系组织段落，使章节衔接自然；
- 为公式补充建模目的、符号、单位、含义、边界条件和后续用途；
- 规范图题、表题、图注和表注，并在正文中解释图表的核心信息；
- 检查数字、公式、图表、结论与建模产物是否一致；
- 审查章节结构、引用、编号、语言和报告完整性；
- 在不改变事实和结论强度的前提下减少模板化、机械化表达。

该技能只使用能够追溯的题目、数据和运行结果，不会补造模型、数值、图表、参考文献或验证结论。

## 安装

### 方式一：安装两个技能（推荐）

下载或克隆本仓库后，在仓库根目录打开 PowerShell，执行：

```powershell
$codexSkillDir = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME "skills"
} else {
    Join-Path $env:USERPROFILE ".codex\skills"
}

New-Item -ItemType Directory -Force -Path $codexSkillDir | Out-Null

$mathSkillDir = Join-Path $codexSkillDir "math-modeling-huaweicup"
$paperSkillDir = Join-Path $codexSkillDir "paper-writing-huaweicup"

New-Item -ItemType Directory -Force -Path $mathSkillDir | Out-Null
New-Item -ItemType Directory -Force -Path $paperSkillDir | Out-Null

Copy-Item -Path ".\math-modeling-huaweicup-skill\*" `
    -Destination $mathSkillDir -Recurse -Force

Copy-Item -Path ".\paper-writing-huaweicup-skill\*" `
    -Destination $paperSkillDir -Recurse -Force
```

复制完成后重新打开 Codex，使技能目录被重新读取。

安装后的目录应为：

```text
<CODEX_HOME>/skills/
├── math-modeling-huaweicup/
│   ├── SKILL.md
│   ├── perfect-figures/
│   └── reference/
└── paper-writing-huaweicup/
    ├── SKILL.md
    ├── humanizer-chinese-math-modeling/
    └── references/
```

### 方式二：只安装一个技能

如果只需要建模，将 `math-modeling-huaweicup-skill` 复制到：

```text
<CODEX_HOME>/skills/math-modeling-huaweicup/
```

如果已有完整建模成果、只需要论文写作，将 `paper-writing-huaweicup-skill` 复制到：

```text
<CODEX_HOME>/skills/paper-writing-huaweicup/
```

Windows 未设置 `CODEX_HOME` 时，其默认位置通常为：

```text
C:\Users\<你的用户名>\.codex\skills\
```

## 项目准备

技能安装目录与实际竞赛项目目录是两个不同位置。使用时，请打开自己的竞赛项目，并按下面的结构放置材料：

```text
竞赛项目/
└── upload_material/
    ├── 题目.pdf
    ├── 数据1.xlsx
    ├── 数据2.csv
    ├── 规范1.pdf
    └── 规范2.docx
```

文件命名约定：

- `题目.*`：赛题文件；
- `数据1.*`、`数据2.*`：赛题数据；
- `规范1.*`、`规范2.*`：当届比赛规范、格式要求或其他官方材料。

`upload_material/` 中的文件会被当作只读输入。技能生成的文件分别写入：

```text
竞赛项目/
├── upload_material/       # 原始材料，只读
├── modeling_output/       # 建模、代码、图片、表格和验证证据
└── report_output/         # 报告、采用的图表、证据映射和写作审查
```

`modeling_output/` 和 `report_output/` 无需提前创建。

## 怎么使用

建议在提示词中显式写出技能调用名称，并说明本次要完成的问题或章节。

### 只完成问题一的建模测试

```text
math-modeling-huaweicup

读取当前项目 upload_material 中的赛题、数据和规范，只完成问题一：
建立模型、编写并运行 Python 代码、生成必要图表和结果表，并完成基线比较、误差分析和稳健性验证。所有产物按 Q1 归档。
```

预期主要产物：

```text
modeling_output/
├── 图片/Q1/
├── 代码/Q1/
├── 表格/Q1/
└── 说明文档/
    ├── 输入材料清单.md
    ├── 结果说明.md
    └── 建模证据清单.yaml
```

### 根据问题一结果撰写报告章节

```text
$paper-writing-huaweicup

读取 upload_material 和 modeling_output，只撰写问题一对应的报告章节。
完整介绍建模动机、公式、求解方法、结果和验证；采用必要的图表，并解释每张图表的核心信息和结论边界。
```

### 撰写完整报告

```text
paper-writing-huaweicup

根据当前项目的赛题、官方规范和 modeling_output 中的全部建模证据，撰写完整的华为杯数学建模报告。检查公式、图表、数字、结论和引用的一致性，并输出写作审查结果。
```

预期主要产物：

```text
report_output/
├── 报告.md
├── 图片/
│   ├── common/
│   ├── Q1/
│   └── Q2/
├── 表格/
│   ├── common/
│   ├── Q1/
│   └── Q2/
├── 报告证据映射.yaml
├── 写作审查.md
└── 待补充材料.md       # 仅在存在缺失内容时生成
```

### 修改或审查已有报告

```text
paper-writing-huaweicup

审查 report_output/报告.md 的问题一，重点检查：
1. 语言是否准确、自然；
2. 建模与结果之间的逻辑是否连贯；
3. 图题、表题、图注和表注是否规范；
4. 正文是否解释了每张图表的核心信息；
5. 每个公式是否有文字引入、符号说明和后续解释；
6. 所有结论是否能追溯到 modeling_output 中的证据。
在不改变模型和数值的前提下完成修改。
```

## 推荐工作流

```text
准备题目、数据和规范
        ↓
调用 $math-modeling-huaweicup
        ↓
检查 modeling_output 中的模型、结果和验证证据
        ↓
调用 $paper-writing-huaweicup
        ↓
检查 report_output 中的报告、证据映射和待补充项
        ↓
根据当届官方模板完成最终提交格式
```

如果只测试一个问题，可以在两个阶段都明确写“只处理问题一”。技能仍会使用 `Q1/` 保存该问题的专用产物，不会预建空的 `Q2/`、`Q3/` 目录。

## 使用注意事项

- 请提供完整赛题、所需数据和当届官方规范。题目引用的数据缺失时，技能不会自行编造。
- 建模求解需要本机具备可用的 Python 环境；具体第三方库取决于赛题和选用模型。
- 建模技能与写作技能通过 `结果说明.md` 和 `建模证据清单.yaml` 交接，建议先完成并检查建模结果，再开始写作。
- 论文写作技能不会重新建模或擅自调整计算结果。证据不足的部分会进入待补充清单。
- 图片、表格和公式必须在正文中得到解释，不能只插入对象而不说明其核心信息。
- 最终提交格式以当届组委会规范为准；默认生成的 Markdown 适合审阅和继续修改，不代表已经自动满足 DOCX、PDF 或 LaTeX 模板要求。

## 许可证

本项目采用 [MIT License](LICENSE)。
