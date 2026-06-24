# ZYNQ 声学相机：独立 Vivado 工程

`acoustic-camera-repro` 是独立维护、可脚本化重建的 Vivado 工程。工程目标器件为 `xc7z020clg400-2`，顶层为 `system_wrapper`，以 `system` Block Design 连接 Zynq PS、摄像头采集、声学处理 HLS IP、帧缓存和 DVI 输出。

该工程对应的是一套面向工业巡检的声学相机：麦克风阵列信号经过延迟补偿、分数延迟插值和波束形成后，得到 128×72 声场网格；网格经伪彩色映射后与 OV5640 可见光视频叠加，并通过 HDMI/DVI 输出。系统与算法背景、模块边界和版本差异见 [系统架构](docs/ARCHITECTURE.md)、[波束形成与数据通路](docs/BEAMFORMING_PIPELINE.md) 和 [设计依据与性能口径](docs/DESIGN_BASIS.md)。

## 目录说明

- `srcs/`：Block Design、约束、HDL 源码和 XCI 配置。
- `ip_repo/`：工程自定义 IP（摄像头、DVI、图像处理等）。
- `hls_ip_repo/`：声学计算相关的已打包 HLS IP（calculate、delay、inter、vram_add）。
- `scripts/`：创建和综合工程的非交互式 Tcl 脚本。
- `docs/`：设计背景、数据通路、接口职责、性能口径与设计参考。
- `build/`：Vivado 自动生成的工程、缓存和报告；不纳入版本控制。

## 构建环境

构建脚本面向 Vivado 2025.2。使用其他 Vivado 版本时，IP 升级结果和实现结果可能不同。

## 运行综合

在 PowerShell 中执行：

```powershell
& 'C:\AMDDesignTools\2025.2\Vivado\bin\vivado.bat' -mode batch -source scripts\run_synth.tcl
```

脚本会在 `build/vivado` 创建名为 `acoustic-camera-repro` 的工程、重建 Block Design 产物并运行综合。综合报告位于 `build/vivado/acoustic-camera-repro.runs/synth_1/`。

## 运行实现与 bitstream 生成

实现脚本会重建工程，运行布局布线，生成 DRC、利用率和时序报告，并仅在不存在 `Error` 级 DRC 违规时写出 bitstream：

```powershell
& 'C:\AMDDesignTools\2025.2\Vivado\bin\vivado.bat' -mode batch -source scripts\run_impl.tcl
```

产物位于 `build/vivado/acoustic-camera-repro.runs/impl_1/`：`drc.rpt`、`utilization.rpt`、`timing_summary.rpt` 以及 `acoustic-camera-repro.bit`。

## 运行声学算法回归

独立的 Python 参考模型锁定了 16 路 24 位采样、1/32 分数延迟插值、当前/历史能量差分和 64 位声场缓存累加的定点算术。在仓库根目录运行：

```powershell
python -m unittest discover -s tests -v
```

成功时命令以 `OK` 结束。回归测试包含 0/1/31 个分数步长、负数符号扩展、16 通道求和与平方、滑窗差分、64 位累加及环形地址回绕。

## 已知边界

该仓库只管理可重建的设计输入；Vivado 的缓存、运行目录和输出文件均由脚本生成。实际烧录前仍应将工程 XDC 与所用开发板的原理图核对。

算法回归模型是数据通路算术的独立 oracle，不模拟 HLS 流水线延迟，也不覆盖阵列几何、延迟表生成或实机标定。这些输入对应的 HLS C/C++ 源码未纳入当前仓库，因此模型不声称与打包 IP 逐周期等价。
