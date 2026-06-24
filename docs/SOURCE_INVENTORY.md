# Source inventory

The cleaned project was reconstructed from `HLS与Vivado工程/prj/ov5640_hdmi` in the parent archive.

| Original asset | Managed destination | Purpose |
| --- | --- | --- |
| `ov5640_hdmi.srcs` | `srcs` | Block Design, HDL imports, XCI configurations, and constraints |
| `prj/ip_repo` | `ip_repo` | Custom packaged RTL and HLS IP |
| `hls/*/hls/impl/ip` | `hls_ip_repo` | Packaged acoustic-processing HLS IP |

Generated Vivado artifacts deliberately excluded from this repository include `.Xil`, `.gen`, `.cache`, `.runs`, journals, and logs.

## Design-reference documents

The following parent-directory documents were used to document intent and architecture. They are reference material, not build inputs.

| Document | Scope | How it is used here |
| --- | --- | --- |
| `高帧率低功耗的声学相机系统3月10日(1).docx` | Later 16-channel architecture | Beamforming model, fractional delay, sliding-window update, 128×72 grid, and performance terminology |
| `基于Zynq的声学相机.pdf` | Earlier 8-channel implementation | Functional module descriptions, PS/PL control division, camera/overlay path, and host-control behavior |

The reports describe different development stages. Counts and performance values are therefore retained with their stated context rather than treated as one simultaneous hardware configuration; see [DESIGN_BASIS.md](DESIGN_BASIS.md).
