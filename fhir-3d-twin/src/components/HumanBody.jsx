import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

export function HumanBody({ highlightedMeshes = [] }) {
  const groupRef = useRef();

  // Constant rotation for technical scanning effect
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.005;
    }
  });

  const isLungsHighlighted = highlightedMeshes.includes('Lungs');
  const isHeartHighlighted = highlightedMeshes.includes('Heart');

  // Aesthetics
  const defaultMat = (
    <meshStandardMaterial 
      color="#0ea5e9" 
      wireframe 
      transparent 
      opacity={0.2} 
    />
  );

  // Pulsing emissive setup
  const alertMat = (color) => (
    <meshStandardMaterial 
      color={color} 
      emissive={color} 
      emissiveIntensity={1.2}
      wireframe 
      transparent 
      opacity={0.8} 
    />
  );

  return (
    <group ref={groupRef} position={[0, -0.5, 0]}>
      {/* Body Core Placeholder - Box for torso as requested */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[1.2, 2.5, 0.6]} />
        {defaultMat}
      </mesh>
      
      {/* Neck and Head */}
      <mesh position={[0, 1.7, 0]}>
        <sphereGeometry args={[0.4, 12, 12]} />
        {defaultMat}
      </mesh>

      {/* Critical Organ Highlight Areas */}
      {/* Heart Component */}
      <mesh position={[-0.2, 0.4, 0.35]}>
        <sphereGeometry args={[0.15, 16, 16]} />
        {isHeartHighlighted ? alertMat('#ef4444') : defaultMat}
      </mesh>

      {/* Lungs Components - Dual spheres */}
      <mesh position={[0.35, 0.3, 0.2]}>
        <sphereGeometry args={[0.25, 16, 16]} />
        {isLungsHighlighted ? alertMat('#f97316') : defaultMat} {/* Orange/Red pulse */}
      </mesh>
      <mesh position={[-0.35, 0.3, 0.2]}>
        <sphereGeometry args={[0.25, 16, 16]} />
        {isLungsHighlighted ? alertMat('#f97316') : defaultMat}
      </mesh>

      {/* Abstracted Legs for scale */}
      <mesh position={[0.3, -2, 0]}>
        <cylinderGeometry args={[0.15, 0.15, 1.5, 8]} />
        {defaultMat}
      </mesh>
      <mesh position={[-0.3, -2, 0]}>
        <cylinderGeometry args={[0.15, 0.15, 1.5, 8]} />
        {defaultMat}
      </mesh>
    </group>
  );
}
