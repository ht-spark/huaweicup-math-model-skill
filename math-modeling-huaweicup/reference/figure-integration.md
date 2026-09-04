# 华为杯竞赛绘图规范（内置 Python 路线）

本 Skill 已在同级目录内嵌完整的 `nature-figure/` 组件（含 `agents/`、`assets/`、`evals/`、`references/`、`scripts/`、`static/` 和 `tests/`），并同时内嵌了它所需的 `nature-shared/` 共享资源。本文件仅定义华为杯竞赛适配，不替代该组件的完整图表论证、模板和质量审查能力。

绘图时直接读取 `../nature-figure/SKILL.md`，明确选择 Python，并按其路由加载 Python 片段和与当前任务相关的资源。该目录是本 Skill 的组成部分：不得检查、调用或依赖原目录中的外部安装版本，也不得因外部版本不可用而跳过绘图流程。

所有竞赛数据图均使用 Python 的 matplotlib / seaborn 生成。

## 出图前：先写图表契约

每张图先用一句话说明其要支持的结论，再开始写代码。

1. **核心结论**：这张图要证明、比较或解释什么；一图只承担一个主要结论。
2. **证据角色**：多面板图中，每个面板承担主结果、基线对照、误差诊断或稳健性分析中的一种不同角色；合并或删除重复证据。
3. **图型选择**：比较类别用条形/点图，展示趋势用折线，展示相关或残差用散点，展示矩阵或空间格局用热图；不因“好看”而使用雷达图、双纵轴或 3D 图。
4. **数据与统计口径**：写明数据范围、汇总方式、误差条含义、样本单位与必要的检验指标。不得静默删除行、类别或异常值；如有排除，记录规则、前后数量和理由。
5. **导出契约**：在绘制前确定尺寸、坐标轴单位、图例策略、文件名和输出格式。

图表服务于建模结论，审美不能掩盖数据、假设或不确定性。

## Python 样式基线

每个绘图脚本在创建 Figure 前设置中文字体和可编辑矢量文字。优先使用实际可用的字体；若 SimHei 和 Microsoft YaHei 都不可用，应在说明中报告字体替代情况，而不是静默输出乱码。

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green": "#4E9F6D",
    "red": "#B64342",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "neutral_light": "#CFCECE",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
}
DEFAULT_COLORS = [
    PALETTE["blue_main"], PALETTE["green"], PALETTE["red"],
    PALETTE["teal"], PALETTE["violet"], PALETTE["neutral_mid"],
]

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["SimHei", "Microsoft YaHei", "DejaVu Sans"],
    "font.size": 11,
    "axes.unicode_minus": False,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

def save_competition_figure(fig, path_without_suffix, important=False):
    """输出竞赛图：所有图 PNG 300 dpi，重点图补充 PDF 与 SVG。"""
    fig.savefig(f"{path_without_suffix}.png", dpi=300, bbox_inches="tight")
    if important:
        fig.savefig(f"{path_without_suffix}.pdf", bbox_inches="tight")
        fig.savefig(f"{path_without_suffix}.svg", bbox_inches="tight")
    plt.close(fig)
```

中文上标或下标优先用 mathtext，例如 `r"$10^4$ t"`，不要直接使用可能缺失字形的 Unicode 上标。坐标轴必须标注变量名称和单位；无量纲变量应明确写出“无量纲”。

## 视觉与编码规则

- 白色背景；基线或对照使用中性灰或低饱和颜色，核心方案使用主色，红/绿只用于具有“变差/改善”等方向含义的差异。
- 同一变量在所有图中保持相同颜色、标签和单位；不把渐变色当作无关联类别色。
- 优先直接标注关键序列；图例仅在直接标注会拥挤时使用。保留模型名的规范拼写，如 `XGBoost`、`RF`。
- 条形图的柱顶数值与误差条不能遮挡；注释位置根据柱顶加误差上界动态计算，不使用固定高度。
- 有重复实验、随机种子、折叠或情景样本时，可比较的系列使用同一不确定性定义（如均值 ± 标准差、95% CI）；图注或说明中必须写明定义。
- 使用对数坐标前确认数据均为正且说明转换理由；插值前确认自变量单调，并同步重排配对数值。
- 不用彩虹色图；热图使用单调、感知均匀的色图。颜色不是唯一编码，应同时依靠线型、点型、文字或数值支持黑白阅读。

## 多面板图规则

- 多面板应回答同一个问题，按“主结果 → 对照/解释 → 稳健性”组织，而不是机械拼接多张图。
- 使用 `GridSpec` 或统一的 `subplots` 网格；同一行或列的可比较面板应保持绘图区边缘、尺寸与间距一致。
- 色条、嵌入图、专用图例轴不参与同尺寸比较，但不能遮挡主体面板。
- 面板标签使用加粗小写 `a`、`b`、`c`，置于左上角，并在最终渲染尺寸下检查对齐。
- 图例、标题、注释、误差条或标签发生任何布局变化后，必须重新检查整张图的对齐和遮挡。

## 渲染后的质量检查

每张图导出后，在最终使用尺寸下逐项检查；多面板图同时检查单个面板和完整拼图。

| 检查维度 | 通过条件 |
|---|---|
| 数据可追溯 | 图中数值可回溯至代码运行产物；排除或聚合规则有记录 |
| 表达准确 | 变量、单位、刻度、图例、误差条和统计口径与代码一致 |
| 可读性 | 中文无乱码，标签完整，最小文字在最终尺寸下可读，刻度不过密 |
| 视觉完整 | 无文字重叠、裁切、图例遮挡、柱顶标注碰撞或越出页边 |
| 多面板布局 | 可比较面板对齐、间距一致；面板标签位置一致；色条和图例不遮挡 |
| 色彩与层级 | 核心方案比基线更醒目；灰度阅读仍可区分；不确定性没有被颜色掩盖 |
| 输出文件 | PNG 为 300 dpi；重点图另有 PDF 或 SVG；重新运行后产物一致 |

如发现问题，修改绘图代码后重新导出并完整复查。源代码检查或单次肉眼浏览不能代替渲染后的最终尺寸检查。

## 内嵌质量脚本的使用

对每个最终图，使用内嵌组件中的本地脚本执行检查。脚本路径均相对于当前 Skill 根目录：

```powershell
python nature-figure/scripts/validate_figure.py path/to/figure.py
python nature-figure/scripts/audit_pdf_text.py path/to/figure.pdf --min-pt 5
python nature-figure/scripts/audit_figure_collisions.py path/to/figure.pdf --json-out path/to/figure.collision-audit.json
```

多面板图还应使用内嵌的 `nature-figure/scripts/audit_panel_alignment.py` 在最终布局后检查可比较面板的绘图区对齐；绘图脚本应调用其中的 `require_matplotlib_panel_alignment()`。脚本报告的阻断性失败必须修复后再交付；无法执行的检查应在说明文档中记录原因，不得宣称已通过。

## 竞赛边界

- 竞赛数据图必须由赛题数据或明确说明的模型模拟结果经 Python 绘制；不使用 AI 图像生成替代定量图。
- 不引入期刊投稿特有的图注字数、版面宽度、TIFF 600 dpi 或外部审计工具要求，除非赛题另有规定。
- 题目未要求图表且图表不能支撑结论时，可以不出图；一旦出图，仍须遵守本规范。
