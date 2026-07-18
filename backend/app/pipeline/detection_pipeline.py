import os
import time
import json
from backend.app.core.settings import settings
from backend.app.utils.logger import logger
from ai_models.florence2.loader import load_florence2_model, unload_florence2_model
from ai_models.florence2.caption import generate_caption, transform_caption_to_prompt
from ai_models.florence2.part_detection import detect_parts
from ai_models.grounding_dino.loader import load_grounding_dino_model, unload_grounding_dino_model
from ai_models.grounding_dino.detect import detect_objects
from backend.app.core.exceptions import NoObjectDetected
from backend.app.utils.artifacts_manager import artifacts_manager

def run_detection_pipeline_stage1(job_id: str, image_path: str) -> dict:
    """Executes Stage 1 of the detection pipeline: VLM Captioning (Phase 9).
    
    Loads Florence-2, generates a text description of the image, converts it
    into a dot-separated prompt, updates job metadata, and unloads the model.
    """
    start_time = time.time()
    logger.info(f"Starting VLM Caption Generation for Job ID: {job_id}")
    
    model = None
    try:
        # Step 1: Load Florence-2 VLM
        logger.info("Loading Florence-2 model into memory...")
        model, processor = load_florence2_model()
        
        # Step 2: Generate raw text caption
        logger.info("Generating caption...")
        caption = generate_caption(image_path, model, processor)
        logger.info(f"Raw caption generated: '{caption}'")
        
        # Step 3: Transform caption into GroundingDINO prompt
        detection_prompt = transform_caption_to_prompt(caption)
        logger.info(f"GroundingDINO prompt: '{detection_prompt}'")
        
        # Step 4: Unload model to recover VRAM immediately
        logger.info("Unloading Florence-2 model...")
        unload_florence2_model(model)
        model = None
        
        # Save caption.txt and grounding_prompt.txt in job output folder
        artifacts_manager.add_text_artifact(job_id, "caption", caption, "caption.txt")
        artifacts_manager.add_text_artifact(job_id, "grounding_prompt", detection_prompt, "grounding_prompt.txt")
        artifacts_manager.add_completed_phase(job_id, "caption_generation")
        
        # Step 5: Read existing job metadata, update it, and save
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                
        metadata["caption"] = caption
        metadata["detection_prompt"] = detection_prompt
        metadata["stage"] = "Florence-2 Captioning"
        
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: Florence-2 Captioning\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Caption: {caption}\n"
            f"Detection Prompt: {detection_prompt}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "caption": caption,
            "detection_prompt": detection_prompt
        }
        
    except Exception as e:
        if model is not None:
            unload_florence2_model(model)
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: Florence-2 Captioning\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

def run_detection_pipeline_stage2(job_id: str, image_path: str, detection_prompt: str) -> dict:
    """Executes Stage 2 of the detection pipeline: Zero-Shot Bounding Box Detection (Phase 10).
    
    Loads GroundingDINO, executes detection with a retry strategy across progressively lower
    thresholds, updates metadata with the highest confidence box, and unloads the model.
    """
    start_time = time.time()
    logger.info(f"Starting GroundingDINO Object Detection for Job ID: {job_id}")
    
    model = None
    try:
        # Step 1: Load GroundingDINO model
        logger.info("Loading GroundingDINO model into memory...")
        model, processor = load_grounding_dino_model()
        
        # Step 2: Retrieve threshold levels from configuration settings
        thresholds_cfg = settings.grounding_dino.thresholds
        # Map thresholds sequentially
        threshold_levels = [
            getattr(thresholds_cfg, "pass1", 0.20),
            getattr(thresholds_cfg, "pass2", 0.20),
            getattr(thresholds_cfg, "pass3", 0.15),
            getattr(thresholds_cfg, "pass4", 0.10)
        ]
        
        detections = []
        applied_threshold = None
        attempt_number = 1
        
        # Step 3: Run inference with threshold retry strategy
        for idx, thresh in enumerate(threshold_levels):
            logger.info(f"Detection attempt {idx + 1} using threshold: {thresh}")
            detections = detect_objects(image_path, detection_prompt, thresh, model, processor)
            if detections:
                applied_threshold = thresh
                attempt_number = idx + 1
                logger.info(f"Detection successful on attempt {attempt_number}! Found {len(detections)} boxes.")
                break
                
        # Step 4: Unload model to recover VRAM immediately
        logger.info("Unloading GroundingDINO model...")
        unload_grounding_dino_model(model)
        model = None
        
        # Step 5: Check if any bounding box was found
        if not detections:
            logger.error("Object detection failed: no bounding boxes returned across all thresholds.")
            raise NoObjectDetected()
            
        # Extract highest scoring bounding box
        highest_detection = detections[0]
        bbox = highest_detection["box"]
        score = highest_detection["score"]
        label = highest_detection["label"]
        
        # Save bounding box overlay validation image
        from PIL import Image, ImageDraw
        visual_check_path = None
        try:
            val_img = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(val_img)
            # Draw red box outline
            draw.rectangle(bbox, outline="red", width=3)
            images_dir = os.path.join(settings.OUTPUT_DIR, "images")
            os.makedirs(images_dir, exist_ok=True)
            visual_check_path = os.path.join(images_dir, f"{job_id}_detection.png")
            val_img.save(visual_check_path)
            logger.info(f"Saved detection verification image to: {visual_check_path}")
        except Exception as img_err:
            logger.warning(f"Could not save visual check overlay image: {img_err}")
            
        # Add visual check detection image artifact to outputs/<job_id>/
        if visual_check_path and os.path.exists(visual_check_path):
            artifacts_manager.add_file_artifact(job_id, "detection", visual_check_path, "detection.png")
            
        # Mark object detection phase as complete
        artifacts_manager.add_completed_phase(job_id, "groundingdino_detection")
        
        # Step 6: Save bounding box to metadata JSON file
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                
        metadata["bbox"] = bbox
        metadata["bbox_score"] = score
        metadata["bbox_label"] = label
        metadata["bbox_attempts"] = attempt_number
        metadata["stage"] = "GroundingDINO Detection"
        
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: GroundingDINO Detection\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Bounding Box: {bbox}\n"
            f"Confidence: {score:.4f}\n"
            f"Attempts: {attempt_number}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "bbox": bbox,
            "score": score,
            "label": label,
            "attempts": attempt_number
        }
        
    except Exception as e:
        if model is not None:
            unload_grounding_dino_model(model)
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: GroundingDINO Detection\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

def run_detection_pipeline_stage3(job_id: str, image_path: str, parts_list: list = None) -> dict:
    """Executes Stage 3 of the detection pipeline: Open-Vocabulary Part Detection (Phase 11).
    
    Loads Florence-2, detects component bounding boxes, generates overlay image,
    saves visual validation image to outputs/<job_id>/part_detection.png, and unloads model.
    """
    if parts_list is None:
        parts_list = ["body", "handle", "base", "wheels", "lid", "seat", "backrest", "legs"]

    start_time = time.time()
    logger.info(f"Starting Florence-2 Part Detection for Job ID: {job_id}")
    
    model = None
    try:
        # Step 1: Load Florence-2 VLM
        logger.info("Loading Florence-2 model into memory...")
        model, processor = load_florence2_model()
        
        # Step 2: Run part detection
        logger.info(f"Detecting parts: {parts_list}")
        parts_results = detect_parts(image_path, parts_list, model, processor)
        
        # Step 3: Unload model to recover VRAM immediately
        logger.info("Unloading Florence-2 model...")
        unload_florence2_model(model)
        model = None
        
        # Step 4: Generate visual bounding box overlay and save to outputs/<job_id>/part_detection.png
        from PIL import Image, ImageDraw
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        os.makedirs(job_dir, exist_ok=True)
        dest_visual_path = os.path.join(job_dir, "part_detection.png")
        
        try:
            val_img = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(val_img)
            
            # Draw overlay box + labels
            for label, boxes in parts_results.items():
                for bbox in boxes:
                    # Draw green rectangle
                    draw.rectangle(bbox, outline="green", width=3)
                    # Label text placement
                    draw.text((bbox[0] + 2, bbox[1] + 2), label, fill="green")
                    
            val_img.save(dest_visual_path)
            logger.info(f"Saved part detection verification image to: {dest_visual_path}")
        except Exception as img_err:
            logger.warning(f"Could not save parts visual check overlay: {img_err}")
            
        # Step 5: Save part details into result.json and mark phase complete
        # Add visual artifact path
        if os.path.exists(dest_visual_path):
            artifacts_manager.add_file_artifact(job_id, "part_detection", dest_visual_path, "part_detection.png")
            
        # Write parts coordinates inside outputs/<job_id>/result.json
        result_json_path = os.path.join(job_dir, "result.json")
        if os.path.exists(result_json_path):
            try:
                with open(result_json_path, "r") as f:
                    res_data = json.load(f)
                res_data["parts"] = parts_results
                with open(result_json_path, "w") as f:
                    json.dump(res_data, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append parts details in result.json: {js_err}")
                
        artifacts_manager.add_completed_phase(job_id, "part_detection")
        
        # Step 6: Save parts coordinates to metadata result JSON file
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                
        metadata["parts"] = parts_results
        metadata["stage"] = "Florence-2 Part Detection"
        
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: Florence-2 Part Detection\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Parts Found: {list(parts_results.keys())}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "parts": parts_results
        }
        
    except Exception as e:
        if model is not None:
            unload_florence2_model(model)
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: Florence-2 Part Detection\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

