# 调研报告

## 概念解析
- gallery与probe：gallery指注册集或参考集，probe指查询集。通俗一点，gallery是数据库，probe是待识别的图片
- mAP：mean Average Precision，平均准确率，是一种评价指标，用于评价检索系统的性能。mAP是所有类别AP的平均值。AP是每个类别的准确率，表示的是检测器在各个 Recall 情况下的平均值，对应的就是 PR 曲线下的面积（AUC， Area Under Curve）。mAP越高，说明检索系统性能越好。
- IoU（交并比，Intersection over Union）: IoU 计算的是 “预测的边框” 和 “真实的边框” 的交集和并集的比值。

## Bike-Person Re-Identification: A Benchmark and a Comprehensive Evaluation
提出了第一个人-自行车数据集，并做了第一个进行人-自行车配对再识别的工作。

### 背景
BPReid数据集的特点：
1. 该数据集是第一个自行车-人员再识别数据集。
2. 从真实监控系统采样
3. 摄像头间距离远，涉及场所范围大

要考虑的困难有：光线、遮挡、视角、相似识别对象

相比人员再识别增加的困难有：
1. 人车对在不同角度看变化更大，特别是尺寸和轮廓方面（自行车侧看正看差别巨大）
2. 一辆自行车可以载多个人

### 方法
> 本文仅关心给出一个基本流程，故使用方法较基础，效果较差

流程：分割-特征提取-度量学习(Metric Learning)

分割方法极为粗浅，无参考价值

resize经验表明在其流程下识别精度对人像大小远比自行车图像大小更敏感（它的resize是含拉伸的）

特征提取方法可参考：ELF, LOMO and GOG，上GOG下ELF与上ELF下GOG的效果较好。一般来说，ELF提取局部特征，GOG提取全局特征。LOMO表现差，因为其涉及极大值，容易注意到噪声。

和度量学习(Metric Learning)配合使用时：MLAPG对单车效果较佳，鲁棒性较好，不过较耗时；改进的FDA如LFDA与XQDA也有较好的表现













## 11


































