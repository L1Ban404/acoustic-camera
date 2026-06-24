# 文档图示来源

本目录中的图示由用户提供的设计资料提取，仅用于说明本工程的架构背景和历史实现，不是 Vivado 构建输入。

| 文件 | 来源 | 内容 |
| --- | --- | --- |
| `word-16ch-overall-microarchitecture.png` | `高帧率低功耗的声学相机系统3月10日(1).docx` | 16 通道总体微架构 |
| `word-ring-buffer-architecture.png` | 同上 | 环形缓存的短期/长期读取结构 |
| `word-video-cache-and-output.png` | 同上 | 声场缓存与视频输出通路 |
| `word-16ch-array-layout.png` | 同上 | 双圆环麦克风阵列与中心摄像头布局 |
| `pdf-8ch-system-overview.jpg` | `基于Zynq的声学相机.pdf` | 早期 8 通道系统概览 |
| `pdf-8ch-compute-pipeline.jpg` | 同上 | 早期计算流水线 |
| `pdf-video-vdma-dataflow.jpg` | 同上 | VDMA 与图像叠加数据流 |

两份资料记录了不同开发阶段；图片的通道数、时钟、接口或性能标注必须结合 [../DESIGN_BASIS.md](../DESIGN_BASIS.md) 的版本说明阅读。
