import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image

def create_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(8.5, 3.6), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Top Section - User Client & Supabase
    rect_client = patches.FancyBboxPatch((0.02, 0.68), 0.44, 0.26, boxstyle="round,pad=0.02", facecolor="#E0F2FE", edgecolor="#0284C7", linewidth=1.8)
    ax.add_patch(rect_client)
    ax.text(0.24, 0.81, "Client / Frontend\n(Next.js 14, Three.js, Tailwind CSS)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')

    rect_supa = patches.FancyBboxPatch((0.54, 0.68), 0.44, 0.26, boxstyle="round,pad=0.02", facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1.8)
    ax.add_patch(rect_supa)
    ax.text(0.76, 0.81, "Supabase Cloud Service\n(Auth JWT & PostgreSQL Database)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')

    # Outer Container - FastAPI Backend
    rect_backend = patches.FancyBboxPatch((0.02, 0.04), 0.96, 0.56, boxstyle="round,pad=0.02", facecolor="#F3E8FF", edgecolor="#9333EA", linewidth=2)
    ax.add_patch(rect_backend)
    
    # Title at top header of backend card
    ax.text(0.5, 0.53, "FastAPI Backend & AI Pipeline Controller", ha='center', va='center', fontsize=11, fontweight='bold', color='#581C87')

    # Sub-steps inside Backend arranged in 2 rows of 3 columns
    sub_steps = [
        "1. Preprocessing\n(CLAHE Enhancement)", 
        "2. Auto Captioning\n(Florence-2)", 
        "3. Object Detection\n(GroundingDINO)", 
        "4. Precision Masking\n(SAM 2.1 + rembg)", 
        "5. 3D Mesh Generation\n(Hunyuan3D-2)", 
        "6. Point Cloud Sampling\n(Open3D + DBSCAN)"
    ]

    for i, step in enumerate(sub_steps):
        row = i // 3
        col = i % 3
        
        sx = 0.05 + col * 0.305
        sy = 0.27 - row * 0.19
        
        srect = patches.FancyBboxPatch((sx, sy), 0.29, 0.16, boxstyle="round,pad=0.01", facecolor="#FFFFFF", edgecolor="#C084FC", linewidth=1.2)
        ax.add_patch(srect)
        ax.text(sx + 0.145, sy + 0.08, step, ha='center', va='center', fontsize=8, color='#1E293B', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def create_pipeline_flowchart_diagram(output_path):
    fig, ax = plt.subplots(figsize=(8.5, 2.8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    steps = [
        "Image Upload",
        "P1: CLAHE",
        "P2: Florence-2",
        "P3/4: DINO",
        "P5/6: SAM2+rembg",
        "P7/8: Hunyuan3D",
        "P9/10: Open3D",
        "P11: DBSCAN",
        ".GLB & .PLY"
    ]

    for i, step in enumerate(steps):
        col = i % 5
        row = i // 5
        x = 0.02 + col * 0.195
        y = 0.58 - row * 0.46
        
        bg_color = "#EEF2FF" if i not in (0, 8) else ("#DCFCE7" if i == 8 else "#E0F2FE")
        border_color = "#6366F1" if i not in (0, 8) else ("#16A34A" if i == 8 else "#0284C7")
        
        rect = patches.FancyBboxPatch((x, y), 0.16, 0.35, boxstyle="round,pad=0.015", facecolor=bg_color, edgecolor=border_color, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + 0.08, y + 0.175, step, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

        if i < 4:
            ax.annotate("", xy=(x + 0.19, y + 0.175), xytext=(x + 0.165, y + 0.175),
                        arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2))
        elif i == 4:
            ax.annotate("", xy=(0.80, 0.175), xytext=(0.80, 0.56),
                        arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2))
        elif i >= 5 and i < 8:
            ax.annotate("", xy=(x - 0.035, y + 0.175), xytext=(x - 0.005, y + 0.175),
                        arrowprops=dict(arrowstyle="<-", color="#475569", lw=1.2))

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def generate_capstone_pdf(pdf_path, diagram_path, flowchart_path):
    create_architecture_diagram(diagram_path)
    create_pipeline_flowchart_diagram(flowchart_path)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Typography - Times-Roman, Bold Headings 14pt, Body 12pt
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#111827'),
        spaceAfter=8,
        spaceBefore=4,
        alignment=0
    )
    
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=4,
        spaceBefore=6
    )

    body_style = ParagraphStyle(
        'Body12',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E293B'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#E2E8F0'),
        borderWidth=0.5,
        borderPadding=4,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet12',
        parent=body_style,
        leftIndent=16,
        bulletIndent=6,
        spaceAfter=4
    )

    story = []

    # ================= PAGE 1: TABLE OF CONTENTS =================
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(Spacer(1, 2))

    toc_data = [
        [Paragraph("<b>Section No.</b>", body_style), Paragraph("<b>Section Title</b>", body_style), Paragraph("<b>Page No.</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("Project Title & Problem Statement", body_style), Paragraph("2", body_style)],
        [Paragraph("2", body_style), Paragraph("Project Objectives", body_style), Paragraph("3", body_style)],
        [Paragraph("3", body_style), Paragraph("Functional & Non-Functional Requirements", body_style), Paragraph("4", body_style)],
        [Paragraph("4", body_style), Paragraph("Hardware, Software & Technologies Used", body_style), Paragraph("5", body_style)],
        [Paragraph("5", body_style), Paragraph("System Architecture & Design", body_style), Paragraph("6", body_style)],
        [Paragraph("6", body_style), Paragraph("End-to-End AI Pipeline Workflow", body_style), Paragraph("7", body_style)],
        [Paragraph("7", body_style), Paragraph("Modules Implemented", body_style), Paragraph("8", body_style)],
        [Paragraph("8", body_style), Paragraph("AI Models Selection, Rationale & Installation (Part 1)", body_style), Paragraph("9", body_style)],
        [Paragraph("9", body_style), Paragraph("AI Models Selection, Rationale & Installation (Part 2)", body_style), Paragraph("10", body_style)],
        [Paragraph("10", body_style), Paragraph("REST API Endpoints & Database Schema", body_style), Paragraph("11", body_style)],
        [Paragraph("11", body_style), Paragraph("Core Implementation Code Snippets", body_style), Paragraph("12", body_style)],
        [Paragraph("12", body_style), Paragraph("Testing Strategy, Verification & Benchmarks", body_style), Paragraph("13", body_style)],
        [Paragraph("13", body_style), Paragraph("Industrial Applications & Real-World Use Cases", body_style), Paragraph("14", body_style)],
        [Paragraph("14", body_style), Paragraph("Important Engineering & Architectural Insights", body_style), Paragraph("15", body_style)],
        [Paragraph("15", body_style), Paragraph("Comprehensive End-to-End Processing & Model Integration Flow", body_style), Paragraph("16", body_style)],
        [Paragraph("16", body_style), Paragraph("Conclusion & Future Scope", body_style), Paragraph("17", body_style)],
    ]

    toc_table = Table(toc_data, colWidths=[80, 360, 60])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Examination Guidelines Quick Reference", h2_style))
    story.append(Paragraph("• <b>Document Purpose:</b> Official ESA Capstone Project Examination Booklet Reference.", bullet_style))
    story.append(Paragraph("• <b>Items to Bring:</b> Printed Project Report, Laptop + Charger, PPT, College ID Card.", bullet_style))
    story.append(Paragraph("• <b>Dress Code:</b> Formal dress is strictly compulsory.", bullet_style))
    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("Project Title", h1_style))
    story.append(Paragraph("Automated Single-Image to 3D Asset and Point Cloud Generation System", body_style))
    story.append(Spacer(1, 14))
    
    story.append(Paragraph("Problem Statement", h1_style))
    p_stmt = (
        "Traditional 3D content creation and 3D point cloud generation rely heavily on specialized 3D modeling skills, "
        "expensive multi-camera photogrammetry hardware setups, or complex and iterative text-prompt engineering. Existing single-image "
        "3D generation systems often suffer from significant limitations, including a lack of part-level semantic understanding, clean background "
        "isolation, structured point-cloud segmentation, or persistent multi-user history.<br/><br/>"
        "To bridge this technology gap, there is an urgent need for an end-to-end, automated, prompt-free software system capable of "
        "converting a standard single 2D RGB image into a high-quality textured 3D asset (.GLB format) and a semantically segmentable "
        "point cloud (.PLY format) suitable for Augmented Reality (AR), Virtual Reality (VR), e-commerce, digital twin applications, and robotics."
    )
    story.append(Paragraph(p_stmt, body_style))
    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("Project Objectives", h1_style))
    story.append(Paragraph("The primary goal of this project is to develop a fully automated, prompt-free deep learning and computer vision framework for 3D asset generation. The specific objectives are as follows:", body_style))
    
    objectives = [
        "<b>Automated AI Pipeline:</b> Eliminate manual prompt writing by automatically generating captions, bounding boxes, object masks, and 3D reconstructions directly from a single uploaded RGB image.",
        "<b>Zero-Shot Object Detection & Segmentation:</b> Perform part-level detection and background removal using state-of-the-art vision models including Florence-2, GroundingDINO, SAM 2.1, and ONNX rembg.",
        "<b>High-Quality 3D Mesh Generation:</b> Reconstruct complete 3D meshes with synthesized textures (.GLB format) using state-of-the-art Hunyuan3D-2 geometry models.",
        "<b>Point Cloud Generation & Semantic Clustering:</b> Sample surface meshes into dense 3D point clouds (.PLY format) with computed surface normals and segment them semantically using density-based DBSCAN clustering.",
        "<b>Full-Stack Web Application with Persistence:</b> Build a responsive production-grade web application featuring Next.js 14, Three.js interactive WebGL visualization, FastAPI backend microservices, Supabase authentication, and persistent PostgreSQL database storage."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", bullet_style))
    story.append(PageBreak())

    # ================= PAGE 4 =================
    story.append(Paragraph("Functional & Non-Functional Requirements", h1_style))
    
    story.append(Paragraph("Functional Requirements (FR)", h2_style))
    fr_items = [
        ("FR-01: Image Upload & Validation", "Allow upload of single RGB images (JPG, PNG, WEBP, BMP up to 25MB). Reject corrupted files with 400 validation error."),
        ("FR-02: Adaptive Contrast Enhancement", "Automatically apply CLAHE enhancement to low-contrast images while bypassing normal contrast images."),
        ("FR-03: Prompt-Free Auto Captioning", "Generate natural language object descriptions with Florence-2 without manual text prompt input."),
        ("FR-04: Multi-Pass Zero-Shot Detection", "Locate target objects with GroundingDINO using a 4-pass fallback confidence thresholding strategy."),
        ("FR-05: Part & Instance Segmentation", "Predict part-level bounding boxes (Florence-2) and generate pixel-perfect binary masks (SAM 2.1)."),
        ("FR-06: RGBA Background Isolation", "Combine SAM 2.1 masks with ONNX rembg to extract transparent RGBA foreground cutouts."),
        ("FR-07: 3D Mesh & Texture Generation", "Synthesize textured 3D meshes (.GLB format) with PBR materials using Hunyuan3D-2 diffusion models."),
        ("FR-08: Point Cloud & DBSCAN Clustering", "Sample 100k mesh surface points (Open3D) and segment coordinates into semantic clusters using DBSCAN."),
        ("FR-09: User Authentication & Security", "Provide email/password signup, login, JWT session tokens, and Supabase Row Level Security (RLS)."),
        ("FR-10: Persistent Job History & Export", "Allow users to query, search, filter, and download all generated output artifacts (.GLB, .PLY, .PNG, .JSON).")
    ]
    for fr_title, fr_desc in fr_items:
        story.append(Paragraph(f"• <b>{fr_title}:</b> {fr_desc}", bullet_style))

    story.append(Spacer(1, 2))
    story.append(Paragraph("Non-Functional Requirements (NFR)", h2_style))
    nfr_items = [
        ("NFR-01 Performance:", "Complete 13-stage execution pipeline within 3–4 minutes on CUDA GPU hardware."),
        ("NFR-02 Reliability:", "Gracefully handle OOM risks via sequential model unloading and provide local JSON fallback if Supabase is offline."),
        ("NFR-03 Usability:", "Deliver a responsive WebGL Next.js interface with real-time progress indicators and dark/light theme support."),
        ("NFR-04 Maintainability & Security:", "Follow modular FastAPI architecture with strict JWT validation and input payload size caps (25MB).")
    ]
    for nfr_title, nfr_desc in nfr_items:
        story.append(Paragraph(f"• <b>{nfr_title}:</b> {nfr_desc}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 5 =================
    story.append(Paragraph("Hardware, Software & Technologies Used", h1_style))
    story.append(Paragraph("Detailed technical specifications, rationale for component selection, and key features of all hardware, software runtimes, and core technologies powering the 3D generation system:", body_style))
    story.append(Spacer(1, 4))
    
    # 1. Hardware Requirements Table
    story.append(Paragraph("Hardware Requirements Specifications & Rationale", h2_style))
    hw_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Specification</b>", body_style), Paragraph("<b>Why Used in Project</b>", body_style), Paragraph("<b>Key Features</b>", body_style)],
        [Paragraph("Processor (CPU)", body_style), Paragraph("Intel Core i7 / AMD Ryzen 7 (11th Gen+)", body_style), Paragraph("Orchestrates backend API tasks, image preprocessing (CLAHE), Open3D sampling, & DBSCAN clustering.", body_style), Paragraph("High multi-core throughput, fast vector array operations.", body_style)],
        [Paragraph("Graphics Card (GPU)", body_style), Paragraph("NVIDIA GPU (Min 8GB, 12GB+ VRAM)", body_style), Paragraph("Executes heavy deep learning vision & generative 3D diffusion inference (Florence-2, SAM 2.1, Hunyuan3D-2).", body_style), Paragraph("CUDA Tensor Cores, parallel GPU tensor math, high VRAM bandwidth.", body_style)],
        [Paragraph("System Memory (RAM)", body_style), Paragraph("16 GB Min (32 GB Recommended)", body_style), Paragraph("Holds loaded PyTorch model checkpoints in host RAM before transferring tensors to GPU.", body_style), Paragraph("High bandwidth, prevents swapping during model initialization.", body_style)],
        [Paragraph("Storage", body_style), Paragraph("50 GB SSD available storage", body_style), Paragraph("Stores PyTorch model weights (~15-20GB), cached HuggingFace models, & output assets (.GLB, .PLY).", body_style), Paragraph("High NVMe/SSD IOPS for fast model weight loading.", body_style)]
    ]
    hw_table = Table(hw_data, colWidths=[90, 110, 160, 140])
    hw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(hw_table)
    story.append(Spacer(1, 4))

    # 2. Software Requirements Table
    story.append(Paragraph("Software Requirements & Environment", h2_style))
    sw_data = [
        [Paragraph("<b>Software / Tool</b>", body_style), Paragraph("<b>Version / Spec</b>", body_style), Paragraph("<b>Why Used in Project</b>", body_style), Paragraph("<b>Key Features</b>", body_style)],
        [Paragraph("Operating System", body_style), Paragraph("Windows 10/11 / Linux (Ubuntu 22.04)", body_style), Paragraph("Provides stable runtime platform for NVIDIA CUDA drivers, Python, and Node.js server execution.", body_style), Paragraph("Widespread driver support, Linux cloud server compatibility.", body_style)],
        [Paragraph("Programming Runtimes", body_style), Paragraph("Python 3.10+, Node.js v18+", body_style), Paragraph("Python runs FastAPI AI pipeline; Node.js executes Next.js 14 frontend web application.", body_style), Paragraph("Asynchronous event loops, rich ecosystem for AI & WebGL.", body_style)],
        [Paragraph("GPU Acceleration", body_style), Paragraph("CUDA Toolkit 11.8 / 12.1", body_style), Paragraph("Enables PyTorch & ONNX Runtime to execute tensor math directly on NVIDIA GPU hardware.", body_style), Paragraph("Direct GPU memory access, cuDNN deep learning acceleration.", body_style)],
        [Paragraph("Cloud Platform & DB", body_style), Paragraph("Supabase Cloud (PostgreSQL)", body_style), Paragraph("Manages user authentication (JWT) and persistent relational storage for job records.", body_style), Paragraph("Row Level Security (RLS), instant REST APIs, automated Auth.", body_style)],
        [Paragraph("Web Browser", body_style), Paragraph("WebGL2 Supported Browser", body_style), Paragraph("Renders interactive 3D meshes (.GLB) and point clouds (.PLY) in browser via Three.js.", body_style), Paragraph("Hardware-accelerated 3D canvas rendering without plugins.", body_style)]
    ]
    sw_table = Table(sw_data, colWidths=[90, 110, 160, 140])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(sw_table)
    story.append(Spacer(1, 4))

    # 3. Technologies Used Table
    story.append(Paragraph("Core Technologies & Frameworks Rationale", h2_style))
    tech_data = [
        [Paragraph("<b>Domain / Model</b>", body_style), Paragraph("<b>Framework / Stack</b>", body_style), Paragraph("<b>Why Used in Project</b>", body_style), Paragraph("<b>Key Features</b>", body_style)],
        [Paragraph("Frontend Web Stack", body_style), Paragraph("Next.js 14, TypeScript, Tailwind", body_style), Paragraph("Delivers a responsive, typed web interface for uploading images and viewing generated 3D assets.", body_style), Paragraph("Server/Client Components, glassmorphic UI, type safety.", body_style)],
        [Paragraph("3D Canvas Engine", body_style), Paragraph("Three.js, @react-three/fiber", body_style), Paragraph("Provides interactive WebGL 3D controls (orbit, zoom, wireframe toggle, HDRI lighting, quick preview).", body_style), Paragraph("GLTFLoader, PLYLoader, Camera Auto-fitter, OrbitControls.", body_style)],
        [Paragraph("Backend Services", body_style), Paragraph("FastAPI, Uvicorn, Pydantic, OpenCV", body_style), Paragraph("Handles REST API endpoints, image validation, CLAHE contrast tuning, & async pipeline execution.", body_style), Paragraph("Async background tasks, strict Pydantic validation schemas.", body_style)],
        [Paragraph("Vision & Auto Caption", body_style), Paragraph("Florence-2 (Microsoft)", body_style), Paragraph("Provides zero-shot image auto-captioning and candidate part bounding box prediction.", body_style), Paragraph("Prompt-free execution, lightweight VRAM footprint (~2-4GB).", body_style)],
        [Paragraph("Object Detection", body_style), Paragraph("GroundingDINO", body_style), Paragraph("Locates target object bounding boxes using natural language grounding from Florence-2 captions.", body_style), Paragraph("Open-vocabulary detection, 4-pass fallback threshold strategy.", body_style)],
        [Paragraph("Object Segmentation", body_style), Paragraph("SAM 2.1 (Meta) & rembg", body_style), Paragraph("Converts bounding boxes into pixel-perfect object masks and removes background for transparent RGBA cutouts.", body_style), Paragraph("High boundary accuracy, ONNX-accelerated background removal.", body_style)],
        [Paragraph("3D Mesh Generation", body_style), Paragraph("Hunyuan3D-2 (Tencent)", body_style), Paragraph("Reconstructs 3D geometry meshes (Stage 1) and synthesizes PBR surface textures (Stage 2) into .GLB format.", body_style), Paragraph("Watertight mesh synthesis, progressive CPU offloading for low VRAM.", body_style)],
        [Paragraph("3D & Point Cloud", body_style), Paragraph("Open3D, Trimesh, PyVista", body_style), Paragraph("Samples 100k surface points (Poisson Disk), computes normal vectors, & applies DBSCAN spatial clustering.", body_style), Paragraph("Poisson Disk Sampling, normal estimation, DBSCAN clustering.", body_style)],
        [Paragraph("Cloud DB & Security", body_style), Paragraph("Supabase Auth & PostgreSQL", body_style), Paragraph("Secures user login with JWT tokens and enforces Row Level Security (RLS) on user history records.", body_style), Paragraph("JWT session tokens, RLS policy protection, automatic triggers.", body_style)]
    ]
    tech_table = Table(tech_data, colWidths=[90, 110, 160, 140])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(tech_table)
    story.append(PageBreak())

    # ================= PAGE 6 =================
    story.append(Paragraph("System Architecture / Design", h1_style))
    story.append(Paragraph("The system follows a modular microservice architecture comprising a Next.js frontend, FastAPI backend services, state-of-the-art vision/3D generative AI models, and cloud persistence with Supabase PostgreSQL.", body_style))
    story.append(Spacer(1, 4))
    
    if os.path.exists(diagram_path):
        story.append(Image(diagram_path, width=480, height=215))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Pipeline Architectural Summary:", h2_style))
    arch_summary = (
        "The architecture establishes a clean separation of concerns. The Next.js frontend manages the WebGL canvas, "
        "user authentication, and job history. The FastAPI backend orchestrates sequential AI model execution with "
        "automatic GPU memory unloading. Database records and generated artifacts are stored securely in Supabase PostgreSQL."
    )
    story.append(Paragraph(arch_summary, body_style))
    story.append(PageBreak())

    # ================= PAGE 7 =================
    story.append(Paragraph("End-to-End AI Pipeline Workflow", h1_style))
    story.append(Paragraph("The system executes a strictly ordered 13-stage sequential workflow to transform a raw single RGB image into a complete textured 3D model and clustered point cloud:", body_style))
    story.append(Spacer(1, 4))

    workflow_stages = [
        ("Stage 1: Image Upload & Validation", "Accepts RGB image formats (JPG, PNG, WEBP, BMP up to 25MB), validates image integrity, and initializes job record in Supabase."),
        ("Stage 2: Image Quality Analysis", "Computes width, height, mean brightness, and standard deviation to determine contrast enhancement requirement."),
        ("Stage 3: CLAHE Contrast Enhancement", "Applies Contrast Limited Adaptive Histogram Equalization via OpenCV in LAB color space if contrast is low."),
        ("Stage 4: Florence-2 Auto Captioning", "Generates zero-shot natural language description (e.g., 'a ceramic coffee mug') and converts it to a dot-separated prompt."),
        ("Stage 5: GroundingDINO Object Detection", "Locates target object bounding boxes using natural language grounding with a 4-pass fallback threshold retry strategy."),
        ("Stage 6: Florence-2 Part Detection", "Predicts candidate structural part bounding boxes (e.g., body, handle, base, seat, wheels)."),
        ("Stage 7: SAM 2.1 Instance Segmentation", "Transforms part bounding boxes into pixel-perfect binary object masks, selecting the highest IoU candidate mask."),
        ("Stage 8: Background Removal (rembg)", "Applies ONNX U-2-Net background removal with SAM 2.1 mask to output a clean RGBA transparent object cutout."),
        ("Stage 9: Hunyuan3D-2 Shape Generation", "Reconstructs 3D geometry mesh using diffusion models with progressive GPU/CPU fallback strategy."),
        ("Stage 10: Hunyuan3D-2 Texture Synthesis", "Synthesizes PBR texture maps applied directly onto geometry mesh, exporting ready-to-use .GLB format."),
        ("Stage 11: Open3D Mesh Validation", "Loads .GLB mesh, validates surface normals, checks watertightness, and verifies geometry vertex integrity."),
        ("Stage 12: Point Cloud Poisson Sampling", "Samples 100,000 dense surface points with computed surface normal vectors to generate raw .PLY point cloud."),
        ("Stage 13: DBSCAN Semantic Clustering", "Clusters point cloud coordinates into semantic structural parts (eps=0.05, min_points=50), saving segmented .PLY.")
    ]

    for stage_title, stage_desc in workflow_stages:
        story.append(Paragraph(f"• <b>{stage_title}:</b> {stage_desc}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 8 =================
    story.append(Paragraph("Modules Implemented", h1_style))
    
    modules = [
        ("1. User Authentication & Profile Module", "Integrates Supabase Auth for email/password signup and login, issuing JWT session tokens for secure FastAPI calls. Manages user profile data and light/dark theme state preferences."),
        ("2. Image Preprocessing & Contrast Enhancement Module", "Processes raw uploaded images using CLAHE contrast adjustments, resolution resizing, color balancing, and standard tensor normalization."),
        ("3. Vision & Part Detection Module", "Leverages Florence-2 for automated zero-shot image caption generation and part detection, alongside GroundingDINO for precise object bounding box detection."),
        ("4. Segmentation & Background Isolation Module", "Combines SAM 2.1 mask generation with ONNX-based rembg foreground extraction to create crisp RGBA images free of background noise."),
        ("5. 3D Mesh Generation Module", "Executes Hunyuan3D-2 generative models to synthesize high-fidelity 3D mesh geometry and surface texture maps exported in standard .GLB format."),
        ("6. Point Cloud Sampling & DBSCAN Clustering Module", "Uses Open3D to perform Poisson Disk Sampling on generated meshes, estimate normal vectors, and apply density-based DBSCAN clustering for part segmentation."),
        ("7. Interactive Web 3D Viewer & History Module", "Provides a Three.js WebGL canvas allowing real-time 3D model rotation, zoom, wireframe toggle, point cloud visualization, and persistent job history management.")
    ]
    
    for mod_title, mod_desc in modules:
        story.append(Paragraph(mod_title, h2_style))
        story.append(Paragraph(mod_desc, body_style))
    story.append(PageBreak())

    # ================= PAGE 9 =================
    story.append(Paragraph("AI Models Rationale, Libraries & Installation (Part 1)", h1_style))

    ai_details_p1 = [
        ("1. Florence-2 (Vision Language Model)", 
         "<b>What it is:</b> An open-vocabulary lightweight Vision-Language Model developed by Microsoft.<br/>"
         "<b>Why we used it:</b> Enables prompt-free execution by automatically captioning images and predicting object part bounding boxes.<br/>"
         "<b>Key Features:</b> Zero-shot task execution, lightweight VRAM footprint (2-4GB), fast inference.<br/>"
         "<b>Libraries:</b> <code>transformers</code>, <code>torch</code>, <code>torchvision</code>, <code>PIL</code>.<br/>"
         "<b>Installation & Loading:</b> Installed via PyPI (<code>pip install transformers torch</code>). Downloaded automatically via Hugging Face Hub (<code>AutoModelForCausalLM.from_pretrained('microsoft/Florence-2-large')</code>) and cached locally on first run."),

        ("2. GroundingDINO (Open-Vocabulary Object Detector)", 
         "<b>What it is:</b> A zero-shot object detector combining DINO architecture with text grounding capabilities.<br/>"
         "<b>Why we used it:</b> Locates target objects dynamically using the natural language caption produced by Florence-2.<br/>"
         "<b>Key Features:</b> High localization precision, open-vocabulary capability, multi-pass fallback thresholding.<br/>"
         "<b>Libraries:</b> <code>transformers</code>, <code>torch</code>, <code>opencv-python</code>.<br/>"
         "<b>Installation & Loading:</b> Installed via PyPI (<code>pip install groundingdino-py</code>). Model weights are loaded directly via Hugging Face Transformers pipeline (<code>AutoModelForZeroShotObjectDetection</code>)."),

        ("3. SAM 2.1 (Segment Anything Model 2.1)", 
         "<b>What it is:</b> Meta's state-of-the-art promptable object segmentation foundation model.<br/>"
         "<b>Why we used it:</b> Converts GroundingDINO bounding boxes into pixel-perfect binary object masks.<br/>"
         "<b>Key Features:</b> Exceptional edge boundary quality, candidate mask evaluation, robust zero-shot generalization.<br/>"
         "<b>Libraries:</b> <code>torch</code>, <code>torchvision</code>, <code>sam2</code>.<br/>"
         "<b>Installation & Loading:</b> Installed via Meta's repository (<code>pip install git+https://github.com/facebookresearch/sam2.git</code>) and checkpoint weights are cached via PyTorch Hub.")
    ]

    for title, desc in ai_details_p1:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(PageBreak())

    # ================= PAGE 10 =================
    story.append(Paragraph("AI Models & Libraries Details (Part 2)", h1_style))

    ai_details_p2 = [
        ("4. rembg (ONNX Background Removal)", 
         "<b>What it is:</b> An ONNX Runtime-powered background removal tool utilizing U-2-Net architecture.<br/>"
         "<b>Why we used it:</b> Refines SAM 2.1 masks to generate clean RGBA cutout images with transparent backgrounds.<br/>"
         "<b>Key Features:</b> Blazing fast ONNX execution, minimal memory overhead, works on CPU and GPU.<br/>"
         "<b>Libraries:</b> <code>rembg</code>, <code>onnxruntime</code>, <code>numpy</code>.<br/>"
         "<b>Installation & Loading:</b> Installed via PyPI (<code>pip install rembg onnxruntime</code>). Model session initializes automatically."),

        ("5. Hunyuan3D-2 (3D Mesh & Texture Generator)", 
         "<b>What it is:</b> Tencent's two-stage 3D generative diffusion model for single-image to textured 3D mesh synthesis.<br/>"
         "<b>Why we used it:</b> Produces high-fidelity watertight 3D meshes (.GLB format) with PBR textures from a single RGBA image.<br/>"
         "<b>Key Features:</b> Stage 1 geometry diffusion + Stage 2 texture synthesis, watertight meshes, sequential CPU offloading & VAE tiling.<br/>"
         "<b>Libraries:</b> <code>torch</code>, <code>diffusers</code>, <code>trimesh</code>, <code>accelerate</code>, <code>einops</code>.<br/>"
         "<b>Installation & Loading:</b> Cloned from Hugging Face / GitHub (<code>Hunyuan3D-2</code> repo) and dependencies installed via <code>pip install diffusers trimesh accelerate</code>. Model pipelines are loaded with CPU offloading enabled to support low VRAM."),

        ("6. Open3D (3D Surface Sampling & Point Cloud Engine)", 
         "<b>What it is:</b> An open-source industrial library for 3D data processing, geometry manipulation, and visualization.<br/>"
         "<b>Why we used it:</b> Converts 3D GLB meshes into dense point clouds (.PLY) using Poisson Disk Sampling and estimates surface normals.<br/>"
         "<b>Key Features:</b> Poisson Disk Sampling, surface normal estimation, fast C++ underlying matrix operations.<br/>"
         "<b>Libraries:</b> <code>open3d</code>, <code>numpy</code>.<br/>"
         "<b>Installation & Loading:</b> Installed via PyPI (<code>pip install open3d</code>). Loaded natively in Python."),

        ("7. DBSCAN (Density-Based Spatial Clustering Algorithm)", 
         "<b>What it is:</b> A density-based spatial clustering algorithm from machine learning.<br/>"
         "<b>Why we used it:</b> Clusters 3D point cloud coordinates into semantic part groups without needing a pre-defined cluster count $k$.<br/>"
         "<b>Key Features:</b> Arbitrary shape cluster discovery, noise filtering, unsupervised execution.<br/>"
         "<b>Libraries:</b> <code>scikit-learn</code>, <code>open3d</code>, <code>numpy</code>.<br/>"
         "<b>Installation & Loading:</b> Installed via PyPI (<code>pip install scikit-learn</code>).")
    ]

    for title, desc in ai_details_p2:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(PageBreak())

    # ================= PAGE 11 =================
    story.append(Paragraph("REST API Endpoints & Database Schema", h1_style))
    story.append(Paragraph("The backend exposes RESTful HTTP endpoints for frontend consumption and syncs execution data with Supabase PostgreSQL:", body_style))

    api_endpoints = [
        ("POST /api/v1/upload", "Accepts multipart image upload, validates file type/size, creates Supabase job row, and kicks off asynchronous background reconstruction."),
        ("GET /api/v1/pipeline/status/{job_id}", "Returns live progress (0-100%) and current pipeline stage (e.g. GroundingDINO, Hunyuan3D-2, DBSCAN)."),
        ("GET /api/v1/download/{job_id}/{artifact_key}", "Streams generated output assets (.GLB mesh, .PLY point cloud, RGBA image, JSON metadata)."),
        ("GET /api/v1/history", "Returns user's historical pipeline jobs with pagination, status filtering, and search criteria."),
        ("GET /api/v1/profile", "Fetches user usage statistics including completed jobs, total models generated, and average processing time.")
    ]

    story.append(Paragraph("Core Backend API Endpoints", h2_style))
    for ep_name, ep_desc in api_endpoints:
        story.append(Paragraph(f"• <b>{ep_name}:</b> {ep_desc}", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Database Schema (Supabase PostgreSQL)", h2_style))
    db_tables = [
        ("profiles", "Stores user profile records synced from <code>auth.users</code> via database triggers (fields: id, email, created_at)."),
        ("jobs", "Stores job execution records (fields: job_id, user_id, status, processing_duration_seconds, created_at, completed_at)."),
        ("artifacts", "Stores generated output file metadata (fields: id, job_id, artifact_type, storage_path, file_size, mime_type).")
    ]

    for tbl_name, tbl_desc in db_tables:
        story.append(Paragraph(f"• <b>{tbl_name}:</b> {tbl_desc}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 12 =================
    story.append(Paragraph("Core Implementation Code Snippets", h1_style))
    story.append(Paragraph("Key Python code snippets demonstrating core pipeline functions, memory management, and 3D point cloud generation:", body_style))

    story.append(Paragraph("1. FastAPI Asynchronous Upload Handler (upload_controller.py)", h2_style))
    code_1 = (
        "def handle_upload(self, file: UploadFile, background_tasks: BackgroundTasks, current_user: dict):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;job_id = storage_service.generate_job_id()<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;saved_path = storage_service.save_upload(file, job_id)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;image_service.validate_job_image(saved_path)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;artifacts_manager.init_job(job_id, saved_path, user_id=current_user.get('id'))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b># Offload heavy pipeline to background execution task</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;background_tasks.add_task(execute_full_reconstruction_pipeline, job_id, saved_path)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return UploadResponse(job_id=job_id)"
    )
    story.append(Paragraph(code_1, code_style))

    story.append(Paragraph("2. Hunyuan3D-2 Low-VRAM Pipeline Configuration (loader.py)", h2_style))
    code_2 = (
        "pipeline.enable_model_cpu_offload()<br/>"
        "pipeline.enable_sequential_cpu_offload()<br/>"
        "pipeline.enable_attention_slicing('max')<br/>"
        "pipeline.enable_vae_slicing()<br/>"
        "pipeline.enable_vae_tiling()<br/>"
        "torch.cuda.empty_cache()  <b># Free cached CUDA memory between stages</b>"
    )
    story.append(Paragraph(code_2, code_style))

    story.append(Paragraph("3. Open3D Point Cloud Sampling & DBSCAN Clustering (pointcloud.py)", h2_style))
    code_3 = (
        "mesh = o3d.io.read_triangle_mesh(glb_path)<br/>"
        "pcd = mesh.sample_points_poisson_disk(number_of_points=100000)<br/>"
        "pcd.estimate_normals()<br/>"
        "<b># DBSCAN Spatial Clustering</b><br/>"
        "labels = np.array(pcd.cluster_dbscan(eps=0.05, min_points=50, print_progress=False))<br/>"
        "o3d.io.write_point_cloud(output_ply_path, pcd)"
    )
    story.append(Paragraph(code_3, code_style))

    story.append(PageBreak())

    # ================= PAGE 13 =================
    story.append(Paragraph("Testing Strategy, Verification & Benchmarks", h1_style))
    story.append(Paragraph("The system was systematically validated through automated pytest backend suites, Playwright UI tests, and performance latency benchmarking:", body_style))

    story.append(Paragraph("Automated Test Suite Results (93 Backend Tests & 6 Frontend E2E Flow Files)", h2_style))
    test_summary_data = [
        [Paragraph("<b>Test Level</b>", body_style), Paragraph("<b>Framework</b>", body_style), Paragraph("<b>Test Files</b>", body_style), Paragraph("<b>Pass Count</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Unit Tests", body_style), Paragraph("pytest", body_style), Paragraph("20 files", body_style), Paragraph("53 Tests", body_style), Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style)],
        [Paragraph("Integration", body_style), Paragraph("pytest + FastAPI", body_style), Paragraph("1 file", body_style), Paragraph("30 Tests", body_style), Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style)],
        [Paragraph("Performance", body_style), Paragraph("pytest-benchmark", body_style), Paragraph("1 file", body_style), Paragraph("10 Tests", body_style), Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style)],
        [Paragraph("Frontend UI", body_style), Paragraph("Playwright", body_style), Paragraph("6 spec files", body_style), Paragraph("All Flows", body_style), Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style)]
    ]
    test_table = Table(test_summary_data, colWidths=[100, 100, 80, 100, 100])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("API Response Time Benchmarks & Performance Targets", h2_style))
    bench_data = [
        [Paragraph("<b>Endpoint / API Method</b>", body_style), Paragraph("<b>Target Latency</b>", body_style), Paragraph("<b>Actual Latency (CI)</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("GET /api/v1/health", body_style), Paragraph("< 1.0s", body_style), Paragraph("0.008s", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("POST /api/v1/upload", body_style), Paragraph("< 5.0s", body_style), Paragraph("0.017s", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("GET /pipeline/status/{id}", body_style), Paragraph("< 0.5s", body_style), Paragraph("0.008s", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("GET /download/{id}/{key}", body_style), Paragraph("< 0.5s", body_style), Paragraph("0.009s", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)]
    ]
    bench_table = Table(bench_data, colWidths=[160, 110, 130, 80])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("• <b>Backend Test Coverage:</b> <b>84% Code Coverage</b> measured via <code>pytest-cov</code>.", bullet_style))
    story.append(PageBreak())

    # ================= PAGE 14 (NEW INDUSTRIAL APPLICATIONS PAGE) =================
    story.append(Paragraph("Industrial Applications & Real-World Use Cases", h1_style))
    story.append(Paragraph("The generated textured 3D assets (.GLB) and segmented point clouds (.PLY) provide practical utility across multiple high-tech industries:", body_style))

    apps = [
        ("1. Augmented & Virtual Reality (AR/VR)", "Generates light web-ready .GLB assets compatible with WebXR, Unity, Unreal Engine, Apple Vision Pro, and Meta Quest for immersive virtual shopping and training."),
        ("2. E-Commerce & Interactive Product Viewer", "Transforms flat 2D product catalog images into interactive 360° rotatable 3D web assets, significantly improving customer engagement and reducing return rates."),
        ("3. Digital Twins & Smart Manufacturing", "Converts single photographs of physical machinery or components into spatial 3D digital representations for asset monitoring and virtual simulation."),
        ("4. Robotics Perception & Grasp Planning", "Segmented point clouds with surface normal vectors enable autonomous robotic grippers to perceive object geometry, plan grasp trajectories, and navigate obstacles."),
        ("5. Industrial Quality Inspection", "DBSCAN clustered point clouds enable surface defect detection, part alignment checking, and CAD variance measurement against ideal factory dimensions."),
        ("6. CAD/CAM Prototyping & Reverse Engineering", "Acts as an automated preliminary spatial scanning tool to jumpstart parametric CAD modeling (.STEP / .IGES) for rapid prototyping.")
    ]

    for app_title, app_desc in apps:
        story.append(Paragraph(f"• <b>{app_title}:</b> {app_desc}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 15 =================
    story.append(Paragraph("Important Engineering & Architectural Insights", h1_style))

    insights = [
        ("1. Sequential Model GPU VRAM Management", 
         "Running multiple heavy generative models simultaneously would cause Out-Of-Memory (OOM) GPU crashes. To prevent this, the backend implements a sequential lifecycle strategy: <b>Load Model → Execute Inference → Explicitly Unload from Memory → Call <code>torch.cuda.empty_cache()</code></b>. Furthermore, Hunyuan3D-2 utilizes <code>cpu_offload</code>, <code>sequential_cpu_offload</code>, <code>attention_slicing</code>, and <code>vae_tiling</code> to run smoothly even on consumer GPUs with 4GB-8GB VRAM."),

        ("2. Asynchronous Polling & Background Processing", 
         "Because 3D asset generation takes ~3 to 4 minutes, HTTP request timeouts are avoided by executing the pipeline asynchronously via FastAPI's <code>BackgroundTasks</code>. The frontend immediately receives a <code>job_id</code> upon upload and polls the status endpoint (<code>GET /api/v1/pipeline/{job_id}/status</code>) while rendering real-time progress steps."),

        ("3. Multi-Pass GroundingDINO Fallback Strategy", 
         "Low contrast or challenging lighting in user images can cause object detection failures. The system handles this with a 4-pass fallback mechanism: <b>Pass 1:</b> Standard detection (threshold 0.20) → <b>Pass 2:</b> Retry on CLAHE contrast-enhanced image → <b>Pass 3:</b> Lower threshold to 0.15 → <b>Pass 4:</b> Final low threshold (0.10)."),

        ("4. Database Security & Local Fallback Mode", 
         "User security is ensured via <b>Supabase Row Level Security (RLS)</b>, allowing users to query only their own job history and output files. For standalone development, the backend automatically falls back to a <b>Local File Storage Mode</b> if Supabase environment variables are missing, storing job metadata in JSON files without crashing.")
    ]

    for title, desc in insights:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(PageBreak())

    # ================= PAGE 16: COMPREHENSIVE PIPELINE BREAKDOWN =================
    story.append(Paragraph("Comprehensive End-to-End Processing & Model Integration Flow", h1_style))
    story.append(Paragraph("A detailed step-by-step breakdown of how the backend AI system handles pre-processing, prompt-free captioning, object detection, pixel segmentation, 3D mesh reconstruction, and point cloud clustering:", body_style))
    story.append(Spacer(1, 4))

    if os.path.exists(flowchart_path):
        story.append(Image(flowchart_path, width=480, height=155))
        story.append(Spacer(1, 6))

    flow_items = [
        ("1. 📤 Upload & Asynchronous Background Queueing", [
            "<b>How it works:</b> When a user uploads an image via the Next.js interface, the FastAPI controller (<code>upload_controller.py</code>) receives the file, validates format/size, generates a unique <code>job_id</code>, and initiates a database record in Supabase.",
            "<b>Non-blocking processing:</b> The request immediately returns the <code>job_id</code> to the client while launching the 11-stage AI pipeline in the background using FastAPI <code>BackgroundTasks</code> (<code>run.py</code>)."
        ]),
        ("2. 🔍 Phase 1: Image Analysis & CLAHE Enhancement", [
            "<b>How it works:</b> The input image is converted to LAB color space. The backend measures the mean brightness and contrast standard deviation.",
            "<b>CLAHE (Contrast Limited Adaptive Histogram Equalization):</b> If the image has low contrast, OpenCV applies CLAHE to balance luminance across local image tiles. This sharpens edges and reveals object details in dark/shadowed areas without over-amplifying noise."
        ]),
        ("3. 📝 Phase 2: Zero-Shot Auto Captioning (Florence-2)", [
            "<b>How it works:</b> The enhanced image is passed to Microsoft's Florence-2 Vision-Language Model (<code>microsoft/Florence-2-large</code>).",
            "<b>Prompt-free execution:</b> Instead of forcing the user to manually write text prompts, Florence-2 automatically describes the scene (e.g. <i>'a ceramic coffee mug on a table'</i>) and extracts core keywords into a dot-separated prompt."
        ]),
        ("4. 🎯 Phase 3 & 4: Bounding Box Detection (GroundingDINO & Florence-2)", [
            "<b>GroundingDINO Detection:</b> Uses text grounding to locate the target object's primary bounding box.",
            "<b>4-Pass Fallback Strategy:</b> If initial confidence is low (&lt; 0.20), the system automatically retries with: (1) CLAHE-enhanced image, (2) Lowered threshold (0.15), (3) Final low threshold (0.10).",
            "<b>Florence-2 Part Detection:</b> Concurrently predicts sub-component bounding boxes (e.g. handle, body, base)."
        ]),
        ("5. ✂️ Phase 5 & 6: SAM 2.1 Masking & rembg Cutout", [
            "<b>SAM 2.1 (Segment Anything 2.1):</b> Meta's SAM 2.1 model takes the predicted bounding box coordinates as visual prompts and generates a high-precision binary pixel mask around object contours.",
            "<b>Background Removal (rembg):</b> The binary mask is combined with rembg (ONNX U-2-Net model) to strip away all background elements, exporting a transparent <code>rgba.png</code> cutout."
        ]),
        ("6. 🧊 Phase 7 & 8: 3D Mesh Generation & Texture Synthesis (Hunyuan3D-2)", [
            "<b>Stage 1 (Geometry Diffusion):</b> Tencent's Hunyuan3D-2 generative model reconstructs a 3D geometry mesh from the transparent <code>rgba.png</code> image.",
            "<b>Stage 2 (Texture Synthesis):</b> Applies progressive texture diffusion to map high-resolution PBR surface textures onto the geometry, producing a ready-to-use <code>.GLB</code> 3D asset.",
            "<b>VRAM Memory Optimization:</b> Uses sequential model loading, CPU offloading, VAE slicing, and explicit <code>torch.cuda.empty_cache()</code> calls to prevent GPU Out-Of-Memory (OOM) errors."
        ]),
        ("7. 🌐 Phase 9, 10 & 11: Point Cloud Sampling & DBSCAN Clustering", [
            "<b>Poisson Disk Sampling (Open3D):</b> Open3D loads the generated <code>.GLB</code> mesh and samples 100,000 surface coordinates while calculating surface normal vectors.",
            "<b>DBSCAN Spatial Clustering:</b> An unsupervised spatial clustering algorithm (DBSCAN) groups the 100,000 points into semantic structural clusters based on spatial density (eps=0.05, min_points=50). The result is exported as a segmented <code>.PLY</code> point cloud file."
        ]),
        ("8. 📊 Real-Time Status Tracking & Persistence", [
            "<b>State Updates:</b> After completing each stage, the backend updates <code>artifacts_manager</code> state.",
            "<b>Polling:</b> The Next.js frontend polls <code>GET /api/v1/pipeline/status/{job_id}</code> to render real-time progress bars and stage logs to the user."
        ])
    ]

    for title, sub_bullets in flow_items:
        story.append(Paragraph(title, h2_style))
        for bullet in sub_bullets:
            story.append(Paragraph(f"• {bullet}", bullet_style))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # ================= PAGE 17 =================
    story.append(Paragraph("Conclusion", h1_style))
    conclusion_text = (
        "The Automated Single-Image to 3D Asset and Point Cloud Generation System successfully addresses the challenges of traditional "
        "3D modeling and point cloud extraction. By seamlessly integrating state-of-the-art generative AI models—Florence-2, GroundingDINO, "
        "SAM 2.1, Hunyuan3D-2, and Open3D—the system converts a single standard 2D image into production-ready 3D textured assets (.GLB) "
        "and semantically segmented point clouds (.PLY) within 3 to 4 minutes without requiring user prompt intervention.<br/><br/>"
        "Combined with a modern full-stack web application featuring Supabase user authentication, dynamic Three.js rendering, and persistent "
        "job history tracking, this project delivers an end-to-end scalable platform for automated 3D content creation."
    )
    story.append(Paragraph(conclusion_text, body_style))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Future Scope", h1_style))
    future_items = [
        "<b>Sparse Multi-View Integration:</b> Extend single-image generation to accept 2-3 sparse view inputs for improved geometry reconstruction of occluded rear surfaces.",
        "<b>Real-Time WebXR & Augmented Reality:</b> Integrate native WebXR features allowing users to directly project generated 3D models into real-world spaces via mobile AR browsers.",
        "<b>Mesh Optimization & Auto-Rigging:</b> Implement automatic polygon decimation, UV unwrapping, and skeletal auto-rigging for instant game-engine readiness.",
        "<b>Distributed GPU Task Queue:</b> Deploy Celery with Redis task queues to scale execution across multi-GPU server clusters for enterprise production concurrency.",
        "<b>CAD & Parametric Surface Export:</b> Convert output point clouds into standard CAD formats (.STEP / .IGES) for engineering and manufacturing workflows."
    ]
    for item in future_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    doc.build(story)

if __name__ == "__main__":
    out_pdf = r"c:\Personal\3D\ESA_Capstone_Project_Report.pdf"
    out_img = r"c:\Personal\3D\arch_diagram.png"
    out_flowchart = r"c:\Personal\3D\pipeline_flowchart.png"
    generate_capstone_pdf(out_pdf, out_img, out_flowchart)
    print("Master Capstone PDF generated successfully at:", out_pdf)
