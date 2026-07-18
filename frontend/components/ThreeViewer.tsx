'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Canvas, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { RotateCcw, Box, Disc, Maximize2, Minimize2, Loader2, AlertTriangle } from 'lucide-react';

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
    setResetKey(prev => prev + 1);
  };
  
  const toggleFullscreen = () => {
    if (!containerRef.current) return;
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().then(() => {
        setIsFullscreen(true);
      }).catch(err => {
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
  
  return (
    <div 
      ref={containerRef} 
      className={`w-full bg-slate-950 border border-slate-900 rounded-2xl overflow-hidden relative transition-all duration-300 flex flex-col ${
        isFullscreen ? 'h-screen w-screen rounded-none border-none' : 'aspect-video'
      }`}
    >
      {/* Top Controls Bar */}
      <div className="absolute top-4 left-4 right-4 flex items-center justify-between z-10 pointer-events-none">
        <div className="flex bg-slate-900/90 border border-slate-800 rounded-lg p-1 pointer-events-auto">
          <button 
            onClick={() => setViewMode('mesh')}
            className={`flex items-center space-x-1 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              viewMode === 'mesh' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Box size={14} />
            <span>Mesh</span>
          </button>
          <button 
            onClick={() => setViewMode('pointcloud')}
            className={`flex items-center space-x-1 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
              viewMode === 'pointcloud' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Disc size={14} />
            <span>Point Cloud</span>
          </button>
        </div>
        
        <div className="flex space-x-2 pointer-events-auto">
          <button 
            onClick={resetCamera}
            className="flex items-center justify-center w-8 h-8 rounded-lg bg-slate-900/90 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700 transition-all"
            title="Reset Camera"
          >
            <RotateCcw size={15} />
          </button>
          <button 
            onClick={toggleFullscreen}
            className="flex items-center justify-center w-8 h-8 rounded-lg bg-slate-900/90 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700 transition-all"
            title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
          >
            {isFullscreen ? <Minimize2 size={15} /> : <Maximize2 size={15} />}
          </button>
        </div>
      </div>
      
      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 bg-slate-950/80 flex flex-col items-center justify-center z-20">
          <Loader2 className="w-8 h-8 text-blue-500 animate-spin mb-2" />
          <p className="text-xs font-medium text-slate-400">Loading 3D asset...</p>
        </div>
      )}
      
      {/* Error Overlay */}
      {error && (
        <div className="absolute inset-0 bg-slate-950/90 flex flex-col items-center justify-center p-6 text-center z-20">
          <AlertTriangle className="w-10 h-10 text-red-500 mb-2" />
          <p className="text-sm font-semibold text-slate-200">{error}</p>
          <p className="text-xs text-slate-500 mt-1">Please try re-generating or check the backend logs.</p>
        </div>
      )}
      
      {/* 3D Canvas */}
      {!error && (
        <div className="flex-grow w-full h-full">
          <Canvas key={resetKey} gl={{ antialias: true }} camera={{ fov: 45, near: 0.1, far: 1000 }}>
            <ambientLight intensity={1.5} />
            <directionalLight position={[10, 10, 10]} intensity={1.5} />
            <directionalLight position={[-10, -10, -10]} intensity={0.5} />
            
            {activeObject && <primitive object={activeObject} />}
            
            <CameraAutoFitter object={activeObject} />
            <OrbitControls makeDefault enableDamping dampingFactor={0.05} />
            <gridHelper args={[20, 20, '#1e293b', '#0f172a']} position={[0, -0.5, 0]} />
          </Canvas>
        </div>
      )}
    </div>
  );
}
