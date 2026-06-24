# ZYNQ 声学相机：可复现 Vivado 工程

本目录从原始资料中整理出一个独立的、脚本化的 Vivado 工程。工程目标器件为 `xc7z020clg400-2`，顶层为 `system_wrapper`，以 `system` Block Design 连接 Zynq PS、摄像头采集、声学处理 HLS IP、帧缓存和 DVI 输出。

## 目录说明

- `srcs/`：Block Design、约束、HDL 源码和原始 XCI 配置。
- `ip_repo/`：原工程自定义 IP（摄像头、DVI、图像处理等）。
- `hls_ip_repo/`：声学计算相关的已打包 HLS IP（calculate、delay、inter、vram_add）。
- `scripts/`：创建和综合工程的非交互式 Tcl 脚本。
- `build/`：Vivado 自动生成的工程、缓存和报告；不纳入版本控制。

## 运行综合

在 PowerShell 中执行：

```powershell
& 'C:\AMDDesignTools\2025.2\Vivado\bin\vivado.bat' -mode batch -source scripts\run_synth.tcl
```

脚本会在 `build/vivado` 创建名为 `acoustic-camera-repro` 的工程、重建 Block Design 产物并运行综合。综合报告位于 `build/vivado/acoustic-camera-repro.runs/synth_1/`。

## 已知边界

该仓库只管理可重建的设计输入；Vivado 的缓存、运行目录和输出文件均由脚本生成。引脚约束来自原工程，实际烧录前仍应与所用开发板的原理图核对。
