import open3d as o3d
from backend.app.utils.logger import logger

def sample_pointcloud_from_mesh(glb_path: str, ply_dest_path: str, target_count: int = 100000) -> dict:
    """Loads a GLB mesh using Open3D, samples a dense point cloud using Poisson Disk Sampling.
    
    Saves the output PLY point cloud and returns statistics.
    """
    logger.info(f"Loading mesh for point cloud sampling: {glb_path}")
    mesh = o3d.io.read_triangle_mesh(glb_path)
    
    if len(mesh.vertices) == 0 or len(mesh.triangles) == 0:
        raise ValueError("Cannot sample points from an empty mesh.")
        
    logger.info(f"Sampling {target_count} points using Poisson Disk Sampling...")
    # Sample points
    pcd = mesh.sample_points_poisson_disk(number_of_points=target_count)
    
    sampled_count = len(pcd.points)
    logger.info(f"Sampled point count: {sampled_count}")
    
    # Estimate point normals if missing
    if not pcd.has_normals():
        logger.info("Point cloud normals are missing. Estimating point normals...")
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        
    # Orient normals consistently
    logger.info("Orienting point cloud normals consistently...")
    pcd.orient_normals_consistent_tangent_plane(k=15)
    
    has_colors = pcd.has_colors()
    has_normals = pcd.has_normals()
    
    # Write point cloud to PLY file
    logger.info(f"Saving point cloud to: {ply_dest_path}")
    success = o3d.io.write_point_cloud(ply_dest_path, pcd, write_ascii=False, compressed=True)
    if not success:
        raise RuntimeError(f"Failed to write PLY point cloud to {ply_dest_path}")
        
    return {
        "point_count": sampled_count,
        "has_normals": has_normals,
        "has_colors": has_colors
    }

def segment_pointcloud_dbscan(ply_src_path: str, ply_dest_path: str, eps: float = 0.05, min_points: int = 50, remove_outliers: bool = True) -> dict:
    """Loads a point cloud, applies DBSCAN clustering, and colors clusters.
    
    Removes outlier points if configured. Saves the segmented point cloud.
    """
    logger.info(f"Loading point cloud for DBSCAN segmentation: {ply_src_path}")
    pcd = o3d.io.read_point_cloud(ply_src_path)
    
    total_points = len(pcd.points)
    if total_points == 0:
        raise ValueError("Cannot perform DBSCAN on an empty point cloud.")
        
    logger.info(f"Running DBSCAN with eps={eps}, min_points={min_points}...")
    import numpy as np
    labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=False))
    
    outlier_points = int(np.sum(labels == -1))
    clustered_points = total_points - outlier_points
    total_clusters = int(labels.max() + 1) if labels.size > 0 and labels.max() >= 0 else 0
    
    logger.info(f"DBSCAN results: clusters={total_clusters}, clustered_points={clustered_points}, outliers={outlier_points}")
    
    # Assign colors to clusters
    if total_clusters > 0:
        # Helper to convert HSL to RGB floats
        def hsl_to_rgb(h: float, s: float, l: float) -> list:
            c = (1 - abs(2 * l - 1)) * s
            x = c * (1 - abs((h * 6) % 2 - 1))
            m = l - c / 2
            if h < 1/6:
                r, g, b = c, x, 0
            elif h < 2/6:
                r, g, b = x, c, 0
            elif h < 3/6:
                r, g, b = 0, c, x
            elif h < 4/6:
                r, g, b = 0, x, c
            elif h < 5/6:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            return [float(r + m), float(g + m), float(b + m)]

        # Generate unique colors for each cluster
        cluster_colors = []
        for i in range(total_clusters):
            # Rotate hue evenly
            hue = i / total_clusters
            cluster_colors.append(hsl_to_rgb(hue, 0.9, 0.5))

        # Color vertices
        pcd_colors = np.zeros((total_points, 3))
        for idx, label in enumerate(labels):
            if label >= 0:
                pcd_colors[idx] = cluster_colors[label]
            else:
                pcd_colors[idx] = [0.5, 0.5, 0.5] # Grey for outliers/noise
        pcd.colors = o3d.utility.Vector3dVector(pcd_colors)
    else:
        # If no clusters found, color all grey
        pcd.paint_uniform_color([0.5, 0.5, 0.5])
        
    # Remove outliers if enabled
    if remove_outliers:
        logger.info("Removing DBSCAN outlier points from the segmented point cloud...")
        valid_indices = np.where(labels >= 0)[0]
        if len(valid_indices) > 0:
            pcd = pcd.select_by_index(valid_indices)
        else:
            logger.warning("DBSCAN marked all points as outliers. Retaining full point cloud to prevent empty file.")
        
    # Save the segmented point cloud
    logger.info(f"Saving segmented point cloud to: {ply_dest_path}")
    success = o3d.io.write_point_cloud(ply_dest_path, pcd, write_ascii=False, compressed=True)
    if not success:
        raise RuntimeError(f"Failed to write segmented point cloud to {ply_dest_path}")
        
    return {
        "total_clusters": total_clusters,
        "total_points": total_points,
        "clustered_points": clustered_points,
        "outlier_points": outlier_points,
        "eps": eps,
        "min_points": min_points
    }
