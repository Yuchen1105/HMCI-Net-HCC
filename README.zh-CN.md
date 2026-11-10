# HMCI-Net 期刊配套仓库

本仓库围绕期刊稿展示增强 CT 的三维全肿瘤与瘤内增强区分割方法、模型表现及泛化能力。完整结果与运行说明见[英文主页](README.md)。

> Automated 3D Segmentation and Quantification of Whole and Enhancing Tumor Burden in Hepatocellular Carcinoma: Multicenter Validation and Prognostic Evaluation

## 图示与实验覆盖

主页展示 **5 幅图示**：依据稿件第 2.3 节绘制的结构总览、稿件图 2–4，以及根据表 3 绘制的队列性能图。队列性能图同时提供 PNG 与可编辑 SVG，全部图片见[图示索引](docs/figures.md)。

| 模块 | 展示内容 | 稿件依据 |
| --- | --- | --- |
| 模型方法 | 四级编码器、解码器及 HM/MSFM/CDI 模块说明 | 第 2.3 节 |
| 内部对比 | 两项任务各 9 个模型，患者级与肿瘤级 DSC、JI 及 IQR | 表 2、图 2 |
| 内外部验证 | 7 组任务—队列结果，完整重叠指标及 IQR | 表 3 |
| 病灶检出 | 患者召回率、肿瘤精确率、召回率与 F1 | 表 3、图 2 |
| 分割可视化 | 全肿瘤与增强区的参考轮廓和模型预测对比 | 图 3 |
| 稳健性 | 肿瘤最大径分层与 CT 灰度分析 | 结果章节、图 4 |

## 主要结果

- 内部测试：全肿瘤患者级 DSC 为 **0.897**，肿瘤级为 **0.906**；增强区分别为 **0.801** 和 **0.811**。
- 全肿瘤外部验证覆盖 LiTS、MSD、CECT 和 TCIA-HCC；患者级 DSC 为 **0.665–0.814**，肿瘤级为 **0.750–0.856**。
- TCIA-HCC 增强区验证：患者级 DSC 为 **0.759**，肿瘤级为 **0.819**。
- 全肿瘤在 <3 cm、3–5 cm、>5 cm 分组的 DSC 分别为 **0.835、0.900、0.925**；增强区分别为 **0.806、0.808、0.815**。

数值均来自期刊稿，保留原始四分位区间与指标口径。完整 18 行模型—任务对比和 7 行队列—任务结果见[实验结果页](docs/experiments.md)及[结构化数据](docs/results/journal_results.json)。未提供的补充表和患者级数据不进行推算。

仓库聚焦分割方法与模型评估；临床基线、Cox 回归、预后 ROC、生存曲线及临床体积一致性图表不展示。

## 代码与使用

`source/` 保存模型及相关 Python 实现，`hmci_net/` 提供统一训练、滑窗推理、原图坐标恢复与患者级掩膜评估入口。两项研究任务分别使用全肿瘤和增强区二分类配置；另提供 LiTS 数据格式的三分类运行示例。

运行命令和数据格式见[Quick start](README.md#quick-start)。使用 `requirements-figures.txt` 安装绘图依赖后，可通过 `python tools/render_results.py` 根据期刊表 3 重建队列性能图。

## 复现说明

所附代码第二、第三扫描分支采用相同轴排列，与稿件三方向描述仍需核对。补充材料 4、5、精确病例划分和期刊训练权重未提供；本机未完成完整 Mamba/CUDA 训练推理验证。示例配置不代表已经核实的期刊实验配置。

详细材料：[方法与实现](docs/method.md) · [复现说明](docs/reproducibility.md) · [验证记录](docs/validation.md)。
