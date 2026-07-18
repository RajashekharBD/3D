"""
Performance benchmarks: Measures stage execution times and memory usage.

This test collects metrics and generates tests/report.md.
It runs lightweight operations (no GPU-heavy model inference) to measure
controller and API response times.
"""
import io
import os
import time
import json
import shutil
import platform
import psutil
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

REPORT_PATH = os.path.join("tests", "report.md")


def _measure(label: str, func, *args, **kwargs):
    """Measures wall-clock execution time of a callable."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed, label


def _get_memory_mb():
    """Returns current process RSS memory in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def _get_gpu_info():
    """Attempts to get GPU memory info via torch.cuda."""
    try:
        import torch
        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            allocated = torch.cuda.memory_allocated(0) / (1024 ** 2)
            reserved = torch.cuda.memory_reserved(0) / (1024 ** 2)
            return {
                "gpu_name": props.name,
                "gpu_total_mb": props.total_mem / (1024 ** 2),
                "gpu_allocated_mb": round(allocated, 2),
                "gpu_reserved_mb": round(reserved, 2),
                "cuda_available": True,
            }
    except ImportError:
        pass
    return {"cuda_available": False}


def _get_system_info():
    """Collects system information."""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "python_version": platform.python_version(),
        "cpu": platform.processor() or "Unknown",
        "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 1),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 1),
        "cpu_count": os.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=0.5),
    }


class TestPerformanceBenchmarks:
    """Collects performance metrics and writes a summary report."""

    metrics: list = []
    stage_timings: dict = {}
    peak_memory_mb: float = 0
    start_memory_mb: float = 0

    def test_01_record_baseline_memory(self):
        """Records baseline memory usage."""
        TestPerformanceBenchmarks.start_memory_mb = _get_memory_mb()
        TestPerformanceBenchmarks.peak_memory_mb = TestPerformanceBenchmarks.start_memory_mb

    def test_02_health_endpoint_latency(self):
        """Measures health endpoint response time."""
        _, elapsed, label = _measure(
            "Health API",
            lambda: client.get("/api/v1/health")
        )
        TestPerformanceBenchmarks.metrics.append({"stage": label, "time_sec": elapsed})
        TestPerformanceBenchmarks.stage_timings[label] = elapsed
        assert elapsed < 1.0, "Health endpoint too slow"

    def test_03_upload_latency(self):
        """Measures upload + validation response time."""
        buf = io.BytesIO()
        Image.new("RGB", (256, 256), color="blue").save(buf, format="PNG")
        content = buf.getvalue()

        def do_upload():
            return client.post(
                "/api/v1/upload",
                files={"image": ("perf_test.png", io.BytesIO(content), "image/png")}
            )

        result, elapsed, label = _measure("Upload + Validation", do_upload)
        assert result.status_code == 200
        job_id = result.json()["job_id"]
        TestPerformanceBenchmarks.metrics.append({"stage": label, "time_sec": elapsed, "job_id": job_id})
        TestPerformanceBenchmarks.stage_timings[label] = elapsed

        current = _get_memory_mb()
        if current > TestPerformanceBenchmarks.peak_memory_mb:
            TestPerformanceBenchmarks.peak_memory_mb = current

        job_dir = os.path.join("outputs", job_id)
        if os.path.isdir(job_dir):
            shutil.rmtree(job_dir)
        import glob
        for f in glob.glob(os.path.join("data", "input", f"{job_id}*")):
            os.remove(f)

    def test_04_status_endpoint_latency(self):
        """Measures pipeline status endpoint response time for a fake job."""
        job_id = "perf_status_test"
        job_dir = os.path.join("outputs", job_id)
        os.makedirs(job_dir, exist_ok=True)
        with open(os.path.join(job_dir, "result.json"), "w") as f:
            json.dump({
                "job_id": job_id,
                "status": "running",
                "completed_phases": ["upload", "validation", "analysis", "clahe"],
                "artifacts": {}
            }, f)

        _, elapsed, label = _measure(
            "Pipeline Status API",
            lambda: client.get(f"/api/v1/pipeline/status/{job_id}")
        )
        TestPerformanceBenchmarks.metrics.append({"stage": label, "time_sec": elapsed})
        TestPerformanceBenchmarks.stage_timings[label] = elapsed
        assert elapsed < 0.5, "Status endpoint too slow"
        shutil.rmtree(job_dir)

    def test_05_download_list_latency(self):
        """Measures download list endpoint response time."""
        job_id = "perf_dl_test"
        job_dir = os.path.join("outputs", job_id)
        os.makedirs(job_dir, exist_ok=True)
        with open(os.path.join(job_dir, "result.json"), "w") as f:
            json.dump({"job_id": job_id, "status": "completed", "completed_phases": [], "artifacts": {}}, f)

        _, elapsed, label = _measure(
            "Download List API",
            lambda: client.get(f"/api/v1/download/{job_id}")
        )
        TestPerformanceBenchmarks.metrics.append({"stage": label, "time_sec": elapsed})
        TestPerformanceBenchmarks.stage_timings[label] = elapsed
        assert elapsed < 0.5, "Download list too slow"
        shutil.rmtree(job_dir)

    def test_06_download_artifact_latency(self):
        """Measures download artifact response time."""
        job_id = "perf_dl_art"
        job_dir = os.path.join("outputs", job_id)
        os.makedirs(job_dir, exist_ok=True)
        with open(os.path.join(job_dir, "result.json"), "w") as f:
            json.dump({"job_id": job_id, "status": "completed", "completed_phases": [], "artifacts": {}}, f)
        with open(os.path.join(job_dir, "original.png"), "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 1024)

        _, elapsed, label = _measure(
            "Download Artifact API",
            lambda: client.get(f"/api/v1/download/{job_id}/original")
        )
        TestPerformanceBenchmarks.metrics.append({"stage": label, "time_sec": elapsed})
        TestPerformanceBenchmarks.stage_timings[label] = elapsed
        assert elapsed < 0.5, "Download artifact too slow"
        shutil.rmtree(job_dir)

    def test_07_upload_reject_large_file_latency(self):
        """Measures rejection time for oversized file."""
        large = b"0" * (26 * 1024 * 1024)

        _, elapsed, label = _measure(
            "Upload Reject Large",
            lambda: client.post(
                "/api/v1/upload",
                files={"image": ("large.png", io.BytesIO(large), "image/png")}
            )
        )
        TestPerformanceBenchmarks.metrics.append({"stage": label, "time_sec": elapsed})
        TestPerformanceBenchmarks.stage_timings[label] = elapsed

    def test_08_upload_reject_invalid_latency(self):
        """Measures rejection time for invalid file."""
        _, elapsed, label = _measure(
            "Upload Reject Invalid",
            lambda: client.post(
                "/api/v1/upload",
                files={"image": ("test.pdf", io.BytesIO(b"PDF"), "application/pdf")}
            )
        )
        TestPerformanceBenchmarks.metrics.append({"stage": label, "time_sec": elapsed})
        TestPerformanceBenchmarks.stage_timings[label] = elapsed

    def test_09_sequential_upload_latency(self):
        """Measures latency of 3 sequential uploads."""
        buf = io.BytesIO()
        Image.new("RGB", (100, 100), color="red").save(buf, format="PNG")
        content = buf.getvalue()

        total_start = time.perf_counter()
        job_ids = []
        for i in range(3):
            result = client.post(
                "/api/v1/upload",
                files={"image": (f"seq_{i}.png", io.BytesIO(content), "image/png")}
            )
            assert result.status_code == 200
            job_ids.append(result.json()["job_id"])
        total_elapsed = time.perf_counter() - total_start

        TestPerformanceBenchmarks.metrics.append({
            "stage": "3 Sequential Uploads (total)",
            "time_sec": total_elapsed
        })
        TestPerformanceBenchmarks.stage_timings["3 Sequential Uploads"] = total_elapsed

        for jid in job_ids:
            jd = os.path.join("outputs", jid)
            if os.path.isdir(jd):
                shutil.rmtree(jd)
            import glob
            for f in glob.glob(os.path.join("data", "input", f"{jid}*")):
                os.remove(f)

    def test_99_generate_report(self):
        """Generates the final performance and test report."""
        gpu_info = _get_gpu_info()
        sys_info = _get_system_info()
        peak_memory = TestPerformanceBenchmarks.peak_memory_mb
        start_memory = TestPerformanceBenchmarks.start_memory_mb
        metrics = TestPerformanceBenchmarks.metrics

        unit_test_files = []
        unit_dir = os.path.join("tests", "unit")
        if os.path.isdir(unit_dir):
            unit_test_files = sorted([f for f in os.listdir(unit_dir) if f.startswith("test_") and f.endswith(".py")])

        integration_test_files = []
        int_dir = os.path.join("tests", "integration")
        if os.path.isdir(int_dir):
            integration_test_files = sorted([f for f in os.listdir(int_dir) if f.startswith("test_") and f.endswith(".py")])

        lines = []
        lines.append("# Test & Performance Report")
        lines.append("")
        lines.append(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Platform:** {sys_info['platform']} {sys_info['platform_release']}")
        lines.append(f"**Python:** {sys_info['python_version']}")
        lines.append(f"**CPU:** {sys_info['cpu']} ({sys_info['cpu_count']} cores)")
        lines.append(f"**RAM:** {sys_info['ram_gb']} GB total, {sys_info['ram_available_gb']} GB available")
        lines.append(f"**CPU Load:** {sys_info['cpu_percent']}%")
        lines.append("")

        # GPU Info
        lines.append("## GPU Information")
        lines.append("")
        if gpu_info.get("cuda_available"):
            lines.append(f"- **GPU:** {gpu_info.get('gpu_name', 'N/A')}")
            lines.append(f"- **Total VRAM:** {gpu_info.get('gpu_total_mb', 0):.0f} MB")
            lines.append(f"- **Allocated:** {gpu_info.get('gpu_allocated_mb', 0):.2f} MB")
            lines.append(f"- **Reserved:** {gpu_info.get('gpu_reserved_mb', 0):.2f} MB")
        else:
            lines.append("- CUDA not available in this environment.")
        lines.append("")

        # Memory
        lines.append("## Memory Usage")
        lines.append("")
        lines.append(f"- **Baseline RSS:** {start_memory:.1f} MB")
        lines.append(f"- **Peak RSS:** {peak_memory:.1f} MB")
        lines.append(f"- **Delta:** {peak_memory - start_memory:.1f} MB")
        lines.append("")

        # API Response Times
        lines.append("## API Response Times")
        lines.append("")
        lines.append("| Stage | Time (sec) | Status |")
        lines.append("|---|---|---|")
        for m in metrics:
            t = m["time_sec"]
            status = "OK" if t < 1.0 else "SLOW" if t < 5.0 else "CRITICAL"
            lines.append(f"| {m['stage']} | {t:.4f} | {status} |")
        lines.append("")

        # Performance targets
        lines.append("## Performance Targets")
        lines.append("")
        lines.append("| Stage | Target | Actual | Status |")
        lines.append("|---|---|---|---|")
        targets = {
            "Health API": "< 1.0s",
            "Upload + Validation": "< 5.0s",
            "Pipeline Status API": "< 0.5s",
            "Download List API": "< 0.5s",
            "Download Artifact API": "< 0.5s",
        }
        for stage, target in targets.items():
            actual = TestPerformanceBenchmarks.stage_timings.get(stage, 0)
            status = "PASS" if actual < float(target.replace("< ", "").replace("s", "")) else "FAIL"
            lines.append(f"| {stage} | {target} | {actual:.4f}s | {status} |")
        lines.append("")

        # Test Coverage Summary
        lines.append("## Test Suite Summary")
        lines.append("")
        lines.append("### Unit Tests")
        lines.append("")
        lines.append(f"Total test files: **{len(unit_test_files)}**")
        lines.append("")
        for f in unit_test_files:
            module = f.replace("test_", "").replace(".py", "")
            lines.append(f"- `{f}` - {module}")
        lines.append("")

        lines.append("### Integration Tests")
        lines.append("")
        lines.append(f"Total test files: **{len(integration_test_files)}**")
        lines.append("")
        for f in integration_test_files:
            lines.append(f"- `{f}`")
        lines.append("")

        lines.append("### Frontend Tests (Playwright)")
        lines.append("")
        lines.append("Total test files: **5**")
        lines.append("")
        lines.append("- `landing.spec.ts` - Landing page")
        lines.append("- `upload.spec.ts` - Upload page")
        lines.append("- `processing.spec.ts` - Processing page")
        lines.append("- `results.spec.ts` - Results page")
        lines.append("- `navigation.spec.ts` - Navigation & responsive")
        lines.append("")

        # Pipeline stages coverage
        lines.append("## Pipeline Stage Coverage")
        lines.append("")
        stages = [
            ("Upload", "test_upload.py"),
            ("Validation", "test_validation.py"),
            ("Image Analysis", "test_analysis.py"),
            ("CLAHE Enhancement", "test_clahe.py"),
            ("Florence-2 Captioning", "test_caption.py"),
            ("GroundingDINO Detection", "test_detection.py"),
            ("Florence-2 Part Detection", "test_part_detection.py"),
            ("SAM2.1 Segmentation", "test_segmentation.py"),
            ("Background Removal", "test_background_removal.py"),
            ("Shape Generation", "test_shape_generation.py"),
            ("Texture Generation", "test_texture_generation.py"),
            ("Mesh Validation", "test_mesh_validation.py"),
            ("Point Cloud Generation", "test_pointcloud.py"),
            ("DBSCAN Segmentation", "test_dbscan.py"),
            ("Pipeline Status API", "test_pipeline_status.py"),
            ("Download API", "test_download.py"),
        ]
        lines.append("| Pipeline Stage | Test File | Status |")
        lines.append("|---|---|---|")
        for stage, test_file in stages:
            status = "Covered" if test_file in unit_test_files else "Missing"
            lines.append(f"| {stage} | `{test_file}` | {status} |")
        lines.append("")

        # Recommendations
        lines.append("## Recommendations")
        lines.append("")
        lines.append("1. **Full GPU Pipeline Benchmark**: Run the complete pipeline on a CUDA-enabled machine to measure AI model inference times.")
        lines.append("2. **Load Testing**: Stress test concurrent uploads to measure API throughput.")
        lines.append("3. **VRAM Monitoring**: Profile GPU memory during consecutive job runs to detect leaks.")
        lines.append("4. **Browser Testing**: Expand Playwright tests to cover 3D viewer interactions and fullscreen mode.")
        lines.append("")

        report_content = "\n".join(lines)
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
        with open(REPORT_PATH, "w") as f:
            f.write(report_content)

        assert os.path.isfile(REPORT_PATH), "Report not generated"
