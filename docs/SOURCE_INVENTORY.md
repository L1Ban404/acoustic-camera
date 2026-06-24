# Source inventory

The cleaned project was reconstructed from `HLS与Vivado工程/prj/ov5640_hdmi` in the parent archive.

| Original asset | Managed destination | Purpose |
| --- | --- | --- |
| `ov5640_hdmi.srcs` | `srcs` | Block Design, HDL imports, XCI configurations, and constraints |
| `prj/ip_repo` | `ip_repo` | Custom packaged RTL and HLS IP |
| `hls/*/hls/impl/ip` | `hls_ip_repo` | Packaged acoustic-processing HLS IP |

Generated Vivado artifacts deliberately excluded from this repository include `.Xil`, `.gen`, `.cache`, `.runs`, journals, and logs.
