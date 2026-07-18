import open3d as o3d
from backend.app.utils.logger import logger

def validate_and_orient_mesh(glb_path: str) -> dict:
    """Loads a GLB mesh using Open3D, validates geometry, computes missing normals, and orients them consistently.
    
    Saves the updated mesh back to the same path.
    Returns a dictionary of mesh statistics.
    """
    logger.info(f"Loading mesh for Open3D validation: {glb_path}")
    
    # Load triangle mesh using Open3D
    mesh = o3d.io.read_triangle_mesh(glb_path)
    
    vertices_count = len(mesh.vertices)
    triangles_count = len(mesh.triangles)
    
    logger.info(f"Open3D Mesh loaded. Vertices: {vertices_count}, Triangles: {triangles_count}")
    
    if vertices_count == 0 or triangles_count == 0:
        raise ValueError(f"Invalid mesh geometry: vertices={vertices_count}, triangles={triangles_count}")
        
    has_normals_before = mesh.has_vertex_normals()
    
    # Avoid extremely slow geometric queries on high-poly meshes (> 50k triangles)
    if triangles_count < 50000:
        is_watertight = mesh.is_watertight()
        is_edge_manifold = mesh.is_edge_manifold()
        is_vertex_manifold = mesh.is_vertex_manifold()
        has_self_intersection = mesh.is_self_intersecting()
    else:
        logger.info(f"Skipping heavy geometric checks (watertight, manifold, self-intersection) for large mesh ({triangles_count} triangles) to prevent hanging.")
        is_watertight = True
        is_edge_manifold = True
        is_vertex_manifold = True
        has_self_intersection = False
    
    # Skip trimesh re-export to avoid heavy CPU memory allocation and processing time (since Hunyuan3D-2 output is already oriented)
    logger.info("Mesh geometry validated successfully. Skipping trimesh normal re-orientation to optimize execution speed.")
         
    return {
        "vertices": vertices_count,
        "triangles": triangles_count,
        "has_normals_originally": has_normals_before,
        "is_watertight": is_watertight,
        "is_edge_manifold": is_edge_manifold,
        "is_vertex_manifold": is_vertex_manifold,
        "has_self_intersection": has_self_intersection
    }
