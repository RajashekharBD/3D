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
    is_watertight = mesh.is_watertight()
    is_edge_manifold = mesh.is_edge_manifold()
    is_vertex_manifold = mesh.is_vertex_manifold()
    has_self_intersection = mesh.is_self_intersecting()
    
    # Update the GLB mesh normals and orientation using trimesh to avoid Open3D GLB export corruption
    import trimesh
    try:
        t_mesh = trimesh.load(glb_path)
        if isinstance(t_mesh, trimesh.Scene):
            for name, geom in t_mesh.geometry.items():
                if isinstance(geom, trimesh.Trimesh):
                    geom.vertex_normals  # Access triggers normal computation if missing
                    geom.fix_normals()   # Orient consistently
            t_mesh.export(glb_path, file_type="glb")
        else:
            t_mesh.vertex_normals
            t_mesh.fix_normals()
            t_mesh.export(glb_path, file_type="glb")
        logger.info("Successfully updated mesh normals and orientation using trimesh.")
    except Exception as export_err:
        logger.error(f"Failed to update GLB normals/winding: {export_err}")
        raise export_err
         
    return {
        "vertices": vertices_count,
        "triangles": triangles_count,
        "has_normals_originally": has_normals_before,
        "is_watertight": is_watertight,
        "is_edge_manifold": is_edge_manifold,
        "is_vertex_manifold": is_vertex_manifold,
        "has_self_intersection": has_self_intersection
    }
