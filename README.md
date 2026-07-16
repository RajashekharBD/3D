# Automated Single-Image to 3D Asset and Point Cloud Generation System

This system automatically converts a single RGB image into a textured 3D asset (GLB) and a segmented point cloud (PLY) using an advanced AI pipeline.

## Features

- Dynamic image analysis and CLAHE enhancement (OpenCV).
- Automatic text captioning and part-level detection (Florence-2).
- Zero-shot primary object detection (GroundingDINO) with multi-pass retries.
- High-fidelity instance segmentation (SAM 2.1).
- Alpha-masked background removal (rembg / ONNX Runtime).
- Diffusion-based watertight 3D reconstruction and PBR texture synthesis (Hunyuan3D-2).
- Mesh evaluation and Poisson Disk point cloud sampling (Open3D).
- Density-based spatial clustering point cloud segmentation (DBSCAN).

## Getting Started

Refer to the documentation in [docs/](docs/) for:
- [Installation Guide](docs/11_INSTALLATION.md)
- [Configuration Guide](docs/12_CONFIGURATION.md)
- [System Architecture Details](docs/04_SYSTEM_ARCHITECTURE.md)
- [Development Phase Tracker](docs/PHASES.md)

## License

This project is licensed under the terms of the LICENSE file.
