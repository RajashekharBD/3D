# KLE Society's

# KLE Technological University, Hubballi

## Department Of MCA

### MCA IV Semester

# CHAPTER – 2

# LITERATURE SURVEY

## On

# “Automated Single-Image to 3D Asset and Point Cloud Generation System”

**Submitted by:**
Rajashekhar B Durgad (01FE24MCA027)

**Under the Guidance of:**
Prof. Akash Hulkund

**KLE Technological University**
Vidyanagar, Hubballi – 580031
2025-2026

---

## 2.1 Introduction

Single-image 3D reconstruction represents one of the most challenging and practical applications of generative AI in computer graphics. These systems integrate object detection, vision-language understanding, instance segmentation, generative 3D modelling, and point cloud processing technologies to convert a single RGB photograph into production-ready 3D assets without manual intervention.

Recent research in AI-driven 3D reconstruction has focused on improving:

* Zero-shot object detection accuracy under varied lighting conditions,
* Automated caption generation for prompt-free operation,
* Generative mesh and texture quality from single-view inputs,
* GPU memory efficiency for sequential model execution,
* And end-to-end pipeline integration with web-based interfaces.

Most early 3D reconstruction systems relied on multi-view photogrammetry or manual modelling, while modern systems increasingly leverage diffusion-based generative models and vision-language foundation models.

## 2.2 Review of Existing Systems

Several research works and implementations have contributed to the development of single-image to 3D reconstruction systems.

**Paper 1: Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection**

This paper introduces GroundingDINO, a zero-shot open-vocabulary object detection model that combines the DINO visual encoder with BERT text encoders. The model enables detection of objects based on arbitrary text prompts without task-specific training data. The system demonstrates powerful detection capabilities across diverse categories, though it remains highly dependent on controlled lighting and high contrast, frequently failing on dark or low-contrast images without adaptive preprocessing [1].

**Paper 2: Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks**

This research proposes Florence-2 as a unified vision-language sequence-to-sequence model capable of caption generation, object detection, and region-level description in a single feedforward pass. The system simplifies captioning and prompt-free setups by automatically generating structured text descriptions from images. However, it lacks spatial 3D reasoning and reconstruction capabilities, operating entirely in 2D image space [2].

**Paper 3: SAM 2: Segment Anything in Images and Videos**

This paper presents the Segment Anything Model 2, achieving state-of-the-art zero-shot instance segmentation. The system generates pixel-precise binary masks for any object given point, box, or text prompts without fine-tuning. Although SAM 2 achieves exceptional segmentation accuracy, it only outputs 2D binary masks and does not project segmentation results into 3D coordinate space [3].

**Paper 4: Hunyuan3D-2: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation**

This paper introduces the Tencent Hunyuan3D-2 framework, utilizing flow-matching diffusion transformers (DiT) for high-fidelity shape generation coupled with appearance-flow UV texture synthesis. The system outputs fully textured GLB assets with PBR materials from clean RGBA images. However, it demands high VRAM and expects background-free inputs, requiring preprocessing for cluttered or natural scenes [4].

**Paper 5: Open3D: A Modern Library for 3D Data Processing**

This work presents Open3D, a comprehensive library for 3D data processing providing tools for Poisson-disk sampling, normal estimation, and geometric analysis. The library enables downstream processing of generated meshes into point clouds with uniform point distribution and accurate surface normals [5].

**Paper 6: A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise**

This foundational paper introduces DBSCAN, an unsupervised clustering algorithm that groups points based on density reachability. For 3D point cloud segmentation, DBSCAN can isolate spatially distinct components without requiring prior knowledge of cluster count, making it suitable for automated geometric segmentation of generated point clouds [6].

## 2.3 Comparative Analysis

| Feature                   | Grounding DINO | Florence-2 | SAM 2 | Hunyuan3D-2 | Open3D + DBSCAN | Proposed System    |
| :------------------------ | :------------- | :--------- | :---- | :---------- | :-------------- | :----------------- |
| Open-Vocabulary Detection | ✓             | Limited    | ✗    | ✗          | ✗              | ✓ (Integration)   |
| Automated Captioning      | ✗             | ✓         | ✗    | ✗          | ✗              | ✓ (Florence-2)    |
| Instance Segmentation     | ✗             | Limited    | ✓    | ✗          | ✗              | ✓ (SAM 2)         |
| 3D Mesh Generation        | ✗             | ✗         | ✗    | ✓          | ✗              | ✓ (Hunyuan3D-2)   |
| Texture Generation        | ✗             | ✗         | ✗    | ✓          | ✗              | ✓ (Hunyuan3D-2)   |
| Point Cloud Generation    | ✗             | ✗         | ✗    | ✗          | ✓              | ✓ (Open3D)        |
| Geometric Segmentation    | ✗             | ✗         | ✗    | ✗          | ✓              | ✓ (DBSCAN)        |
| Adaptive Preprocessing    | ✗             | ✗         | ✗    | ✗          | ✗              | ✓ (CLAHE)         |
| VRAM Management           | ✗             | ✗         | ✗    | ✗          | ✗              | ✓ (Sequential)    |
| Web Interface             | ✗             | ✗         | ✗    | ✗          | ✗              | ✓ (Next.js + R3F) |
| End-to-End Automation     | ✗             | ✗         | ✗    | ✗          | ✗              | ✓                 |

The comparative analysis reveals that while individual models excel in their respective domains, no existing system provides end-to-end automation combining adaptive preprocessing, detection, segmentation, 3D generation, point cloud analysis, and user management in a single unified platform. The proposed system bridges this gap by integrating all these technologies into a cohesive pipeline.

## 2.4 Proposed System

The proposed system addresses the gaps identified in the literature by integrating the reviewed technologies into a unified, automated pipeline with the following key innovations:

1. **Adaptive CLAHE Preprocessing** — Automatically detects low-contrast or dark images and applies Contrast Limited Adaptive Histogram Equalization in the LAB colour space before feeding into detection models, improving robustness under real-world imaging conditions.
2. **Prompt-Free Operation** — Florence-2 generates natural language captions and extracts noun phrases automatically, which are passed to GroundingDINO without requiring manual text input from the user.
3. **Multi-Pass Detection Strategy** — GroundingDINO executes detection with progressively relaxed confidence thresholds (0.20 → 0.15 → 0.10) across multiple passes, increasing detection reliability for challenging images.
4. **Sequential GPU Memory Management** — Each model is loaded, executed, and unloaded sequentially with explicit GPU cache flushing between stages, enabling the full pipeline to run on a single GPU with 16 GB of VRAM.
5. **Dual-Channel Background Removal** — Combines SAM 2's binary mask with rembg's output to produce clean RGBA crops, leveraging the strengths of both approaches.
6. **Unified Output Pipeline** — Generates both a textured GLB mesh and a segmented PLY point cloud in a single run, eliminating the need for separate downstream processing tools.
7. **Full-Stack Web Application** — A Next.js frontend with Supabase authentication, real-time pipeline progress tracking, interactive 3D viewing via React Three Fiber, and persistent job history management.

## 2.5 Summary

From the study of existing systems, the following observations can be made:

* GroundingDINO enables zero-shot object detection but requires adaptive preprocessing for low-contrast images.
* Florence-2 provides automated captioning but lacks 3D spatial reasoning capabilities.
* SAM 2 achieves state-of-the-art segmentation but operates only in 2D image space.
* Hunyuan3D-2 generates high-quality textured meshes but requires clean RGBA inputs and high VRAM.
* Open3D and DBSCAN provide robust point cloud processing but require pre-generated meshes.
* No existing system integrates all these capabilities into a single automated pipeline.

These research gaps motivate the development of the **Automated Single-Image to 3D Asset and Point Cloud Generation System**, which integrates adaptive preprocessing, vision-language detection, instance segmentation, generative 3D reconstruction, point cloud analysis, and web-based user management into a single cohesive platform.

### References

[1] S. Liu, Z. Zeng, H. Ren, F. Li, H. Zhang, and L. Zhang, "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection," in *Proceedings of the European Conference on Computer Vision (ECCV)*, 2024.

[2] B. Xiao et al., "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2024.

[3] N. Ravi et al., "SAM 2: Segment Anything in Images and Videos," *arXiv preprint arXiv:2408.00714*, 2024.

[4] Tencent Hunyuan3D Team, "Hunyuan3D-2: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation," *arXiv preprint arXiv:2501.12202*, 2025.

[5] Q.-Y. Zhou, J. Park, and V. Koltun, "Open3D: A Modern Library for 3D Data Processing," *arXiv preprint arXiv:1801.09847*, 2018.

[6] M. Ester, H.-P. Kriegel, J. Sander, and X. Xu, "A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise," in *Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD)*, 1996, pp. 226-231.
