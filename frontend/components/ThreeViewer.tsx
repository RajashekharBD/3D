'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Canvas, useThree } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import * as THREE from 'three';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { RotateCcw, Box, Disc, Maximize2, Minimize2, Loader2, AlertTriangle } from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

interface ThreeViewerProps {
  glbUrl: string;
  plyUrl: string;
}

// Subcomponent to automatically position the camera to fit the loaded object
function CameraAutoFitter({ object }: { object: THREE.Object3D | null }) {
  const { camera } = useThree();
  
  useEffect(() => {
    if (!object) return;
    
    const box = new THREE.Box3().setFromObject(object);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = (camera as THREE.PerspectiveCamera).fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
    
    // Add buffer margin
    cameraZ *= 1.5;
    
    // Make sure camera doesn't end up too close
    cameraZ = Math.max(cameraZ, 2.0);
    
    camera.position.set(center.x, center.y, center.z + cameraZ);
    camera.lookAt(center);
    camera.updateProjectionMatrix();
  }, [object, camera]);
  
  return null;
}

export default function ThreeViewer({ glbUrl, plyUrl }: ThreeViewerProps) {
  const { theme } = useTheme();
  const [viewMode, setViewMode] = useState<'mesh' | 'pointcloud'>('mesh');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [resetKey, setResetKey] = useState<number>(0);
  
  // Loaded assets
  const [meshObject, setMeshObject] = useState<THREE.Group | null>(null);
  const [plyGeometry, setPlyGeometry] = useState<THREE.BufferGeometry | null>(null);
  const [activeObject, setActiveObject] = useState<THREE.Object3D | null>(null);
  
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Load GLB Mesh
  useEffect(() => {
    if (!glbUrl) return;
    setLoading(true);
    setError(null);
    const loader = new GLTFLoader();
    
    loader.load(
      glbUrl,
      (gltf) => {
        const scene = gltf.scene;

        // Traverse mesh nodes to fix material rendering & lighting issues
        scene.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            const mesh = child as THREE.Mesh;
            if (mesh.material) {
              const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
              materials.forEach((mat) => {
                mat.side = THREE.DoubleSide;
                mat.needsUpdate = true;
                if (mat instanceof THREE.MeshStandardMaterial) {
                  if (mat.roughness > 0.8) mat.roughness = 0.5;
                }
              });
            }
          }
        });

        // Compute bounding box and adjust Y position to sit flat on the grid (Y = -0.5)
        const box = new THREE.Box3().setFromObject(scene);
        const yOffset = -0.5 - box.min.y;
        scene.position.y += yOffset;

        setMeshObject(scene);
        if (viewMode === 'mesh') {
          setActiveObject(scene);
        }
        setLoading(false);
      },
      undefined,
      (err) => {
        console.error('Error loading GLB mesh:', err);
        setError('Failed to load textured GLB mesh.');
        setLoading(false);
      }
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [glbUrl]);
  
  // Load PLY Point Cloud
  useEffect(() => {
    if (!plyUrl) return;
    const loader = new PLYLoader();
    
    loader.load(
      plyUrl,
      (geometry) => {
        // Convert any Float64Array attributes to Float32Array to prevent WebGL errors
        Object.keys(geometry.attributes).forEach((key) => {
          const attr = geometry.attributes[key];
          if (attr && attr.array instanceof Float64Array) {
            const f32Array = new Float32Array(attr.array);
            geometry.setAttribute(key, new THREE.BufferAttribute(f32Array, attr.itemSize));
          }
        });

        setPlyGeometry(geometry);
        if (viewMode === 'pointcloud') {
          const points = new THREE.Points(
            geometry,
            new THREE.PointsMaterial({ size: 0.03, vertexColors: true })
          );
          // Compute bounding box and adjust Y position to sit flat on the grid (Y = -0.5)
          const box = new THREE.Box3().setFromObject(points);
          const yOffset = -0.5 - box.min.y;
          points.position.y += yOffset;

          setActiveObject(points);
        }
      },
      undefined,
      (err) => {
        console.error('Error loading PLY point cloud:', err);
      }
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [plyUrl]);

  // Handle View Mode Toggle
  useEffect(() => {
    if (viewMode === 'mesh' && meshObject) {
      setActiveObject(meshObject);
    } else if (viewMode === 'pointcloud' && plyGeometry) {
      const points = new THREE.Points(
        plyGeometry,
        new THREE.PointsMaterial({ size: 0.03, vertexColors: true })
      );
      // Compute bounding box and adjust Y position to sit flat on the grid (Y = -0.5)
      const box = new THREE.Box3().setFromObject(points);
      const yOffset = -0.5 - box.min.y;
      points.position.y += yOffset;

      setActiveObject(points);
    }
  }, [viewMode, meshObject, plyGeometry]);
  
  const resetCamera = () => {
    setResetKey((prev) => prev + 1);
  };
  
  const toggleFullscreen = () => {
    if (!containerRef.current) return;
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().then(() => {
        setIsFullscreen(true);
      }).catch((err) => {
        console.error('Fullscreen request failed:', err);
      });
    } else {
      document.exitFullscreen().then(() => {
        setIsFullscreen(false);
      });
    }
  };
  
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  const isLight = theme === 'light';
  
  return (
    <div 
      ref={containerRef} 
      className={`w-full bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-900 rounded-2xl overflow-hidden relative transition-all duration-300 flex flex-col shadow-inner ${
        isFullscreen ? 'h-screen w-screen rounded-none border-none' : 'aspect-video'
      }`}
    >
      {/* Top Controls Bar */}
      <div className="absolute top-4 left-4 right-4 flex items-center justify-between z-10 pointer-events-none">
        <div className="flex bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-xl p-1 pointer-events-auto shadow-md">
          <button 
            onClick={() => setViewMode('mesh')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              viewMode === 'mesh' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/50'
            }`}
          >
            <Box size={14} />
            <span>Mesh</span>
          </button>
          <button 
            onClick={() => setViewMode('pointcloud')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              viewMode === 'pointcloud' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/50'
            }`}
          >
            <Disc size={14} />
            <span>Point Cloud</span>
          </button>
        </div>
        
        <div className="flex space-x-2 pointer-events-auto">
          <button 
            onClick={resetCamera}
            className="flex items-center justify-center w-8 h-8 rounded-xl bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-slate-200 hover:border-slate-300 dark:hover:border-slate-700 transition-all shadow-sm cursor-pointer"
            title="Reset Camera"
          >
            <RotateCcw size={15} />
          </button>
          <button 
            onClick={toggleFullscreen}
            className="flex items-center justify-center w-8 h-8 rounded-xl bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-slate-200 hover:border-slate-300 dark:hover:border-slate-700 transition-all shadow-sm cursor-pointer"
            title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
          >
            {isFullscreen ? <Minimize2 size={15} /> : <Maximize2 size={15} />}
          </button>
        </div>
      </div>
      
      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 bg-slate-900/40 dark:bg-slate-950/80 backdrop-blur-xs flex flex-col items-center justify-center z-20">
          <Loader2 className="w-8 h-8 text-indigo-600 dark:text-indigo-400 animate-spin mb-2" />
          <p className="text-xs font-medium text-slate-700 dark:text-slate-300">Loading 3D asset...</p>
        </div>
      )}
      
      {/* Error Overlay */}
      {error && (
        <div className="absolute inset-0 bg-slate-900/50 dark:bg-slate-950/90 backdrop-blur-xs flex flex-col items-center justify-center p-6 text-center z-20">
          <AlertTriangle className="w-10 h-10 text-rose-500 mb-2" />
          <p className="text-sm font-semibold text-slate-800 dark:text-slate-200">{error}</p>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">Please try re-generating or check the backend logs.</p>
        </div>
      )}
      
      {/* 3D Canvas */}
      {!error && (
        <div className="flex-grow w-full h-full">
          <Canvas key={resetKey} gl={{ antialias: true, alpha: true }} camera={{ fov: 45, near: 0.1, far: 1000 }}>
            <color attach="background" args={[isLight ? '#f8fafc' : '#030712']} />
            <hemisphereLight intensity={1.8} skyColor={isLight ? '#ffffff' : '#cbd5e1'} groundColor={isLight ? '#cbd5e1' : '#1e293b'} />
            <ambientLight intensity={1.8} />
            <directionalLight position={[10, 15, 10]} intensity={2.0} />
            <directionalLight position={[-10, 10, -10]} intensity={1.2} />
            <directionalLight position={[0, -10, 10]} intensity={0.8} />
            
            {/* HDRI Environment lighting ensures materials and textures render accurately */}
            <Environment preset="city" />

            {activeObject && <primitive object={activeObject} />}
            
            <CameraAutoFitter object={activeObject} />
            <OrbitControls makeDefault enableDamping dampingFactor={0.05} />
            <gridHelper args={[20, 20, isLight ? '#818cf8' : '#6366f1', isLight ? '#cbd5e1' : '#1e293b']} position={[0, -0.5, 0]} />
          </Canvas>
        </div>
      )}
    </div>
  );
}
