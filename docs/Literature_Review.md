# KLE Society's
# KLE Technological University, Hubballi
## Department Of MCA
### MCA IV Semester

# Literature Review Report
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

# 1. LITERATURE REVIEW
Several studies have explored the automated detection of objects, background subtraction, and the generation of 3D assets to optimize virtual environments and robotic workflows. Early works in open-set object detection introduced architectures like GroundingDINO, which marries DINO visual encoders with BERT text encoders to achieve zero-shot open-vocabulary object detection based on text prompts [1]. These systems demonstrated powerful detection capabilities across diverse categories, though they remain highly dependent on controlled lighting and high contrast, frequently failing on dark or low-contrast images without preprocessing.

Further research focused on multi-task vision models to consolidate image annotation and part-level detection. Florence-2 was proposed as a unified vision-language sequence-to-sequence model capable of generating captions, prompts, and bounding box coordinates for object parts in a single feedforward pass [2]. While this model simplified captioning and prompt-free setups, it lacked spatial 3D reasoning and reconstruction capabilities. Similarly, instance segmentation advancements led to SAM 2 (Segment Anything Model), which offers pixel-precise masking of primary objects and video tracking [3]. Although SAM 2 achieves state-of-the-art segmentation, it only outputs 2D binary masks, leaving 3D spatial reconstruction unaddressed.

More recently, research has shifted to single-image generative 3D reconstruction frameworks to eliminate complex photogrammetry setups. The Tencent Hunyuan3D-2 framework introduced flow-matching diffusion transformers (DiT) for high-fidelity shape generation, coupled with appearance-flow UV texture synthesis yielding textured GLB assets [4]. Although Hunyuan3D-2 outputs watertight meshes with PBR materials, it demands high VRAM and expects a clean, background-free RGBA input, requiring preprocessing for multi-object or cluttered scenes. Fast reconstruction models such as TripoSR [7] provide fast feedforward 3D generation but output lower texture resolution and lack built-in segmentation pipelines. To handle the generated 3D data downstream, researchers utilize libraries like Open3D for Poisson-disk sampling and normal estimation [5], followed by density-based spatial clustering (DBSCAN) to segment points into isolated spatial clusters [6].

---

# 2. CHALLENGES IDENTIFIED
Despite progress in generative AI and segmentation, several challenges are evident from the reviewed literature:
* **Imaging Brittleness:** Zero-shot open-vocabulary detectors like GroundingDINO fail under poor lighting, low-contrast, or grayscale environments without adaptive enhancement [1].
* **Clean Input Dependency:** High-fidelity 3D generators like Hunyuan3D-2 assume background-free RGBA crops as inputs and cannot directly reconstruct objects from cluttered or natural scenes [4].
* **2D-3D Dimensional Gap:** Segmentation models like SAM 2 excel at 2D pixel-level masks but do not project objects or parts into 3D coordinate space [3].
* **Quality vs. Latency Trade-off:** Fast feedforward models like TripoSR generate meshes in seconds but sacrifice texture details and lacks topological segmentation features [7].
* **High VRAM Footprints:** Modern shape generators and texturing models have high peak VRAM requirements, causing Out-Of-Memory (OOM) failures on standard 16 GB GPUs when loaded simultaneously.

---

# 3. RESEARCH GAPS
The analysis of the literature reveals several major research gaps:
* **Lack of End-to-End Integration:** There is an absence of a single unified pipeline that automatically enhances input photographs, detects the subject, extracts it, generates a 3D asset, and clusters it geometrically.
* **Manual Prompt Dependency:** Existing high-quality 3D mesh generators require users to manually type text descriptions to guide the reconstruction, preventing fully automated batch operation.
* **GPU Memory Swapping Limitations:** Existing workflows load multiple models in memory concurrently, which leads to hardware failures. There is a lack of structured GPU memory scheduling to sequentialize execution and empty cache dynamically.
* **Absence of Clean 3D Part Segmentation:** Standard pipelines output raw, unsegmented meshes, lacking downstream geometric categorization (like isolating components of a generated point cloud).

---

# 4. FUTURE ENHANCEMENTS
To address the research gaps, the following enhancements are proposed:
* **Quantized Real-Time Inference:** Apply TensorRT and INT8 quantization to Hunyuan3D-2 flow-matching modules to reduce generation latency to under a minute.
* **turntable Video Reconstruction:** Integrate SAM 2.1's video tracking to capture consistent mask contours from product videos and generate multi-view consistent 3D outputs.
* **Multi-Object Reconstruction:** Extend the detection bounding boxes to allow batch cropping and simultaneous reconstruction of multiple objects from a single image.

---

# 5. CONCLUSION
This literature review establishes a clear foundation for the development of the Automated Single-Image to 3D Asset and Point Cloud Generation System. While modern foundational models (GroundingDINO, Florence-2, SAM 2, and Hunyuan3D-2) excel in their respective tasks, their integration into a unified, resource-managed, and prompt-free desktop application represents a significant advancement. By resolving issues related to background clutter, low illumination, prompt dependencies, and VRAM management, the proposed system provides a robust solution for automated 3D content creation.

---

# 6. REFERENCES
* [1] S. Liu, Z. Zeng, H. Ren, F. Li, H. Zhang, and L. Zhang, "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection," in *Proceedings of the European Conference on Computer Vision (ECCV)*, 2024.
* [2] B. Xiao et al., "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2024.
* [3] N. Ravi et al., "SAM 2: Segment Anything in Images and Videos," *arXiv preprint arXiv:2408.00714*, 2024.
* [4] Tencent Hunyuan3D Team, "Hunyuan3D-2: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation," *arXiv preprint arXiv:2501.12202*, 2025.
* [5] Q.-Y. Zhou, J. Park, and V. Koltun, "Open3D: A Modern Library for 3D Data Processing," *arXiv preprint arXiv:1801.09847*, 2018.
* [6] M. Ester, H.-P. Kriegel, J. Sander, and X. Xu, "A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise," in *Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD)*, 1996, pp. 226-231.
* [7] D. Tochilkin et al., "TripoSR: Fast 3D Object Reconstruction from a Single Image," *arXiv preprint arXiv:2403.02156*, 2024.

