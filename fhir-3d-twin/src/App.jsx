import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, Grid } from '@react-three/drei';
import { HumanBody } from './components/HumanBody';
import { DataPanel } from './components/DataPanel';

export default function App() {
  // Default static state structure
  const [clinicalData, setClinicalData] = useState({
    vitals: { heartRate: '--', bloodPressure: '--', spo2: '--' },
    conditions: [],
    highlighted_meshes: [],
  });
  const [status, setStatus] = useState('DISCONNECTED');

  useEffect(() => {
    let socket;
    let reconnectInterval;

    const connect = () => {
      console.log("Attempting interface handshake...");
      socket = new WebSocket('ws://localhost:8765');

      socket.onopen = () => {
        setStatus('CONNECTED');
        console.log("Secure WebSocket Connection Established.");
      };

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          setClinicalData(payload);
        } catch (err) {
          console.error("Mangled packet received:", err);
        }
      };

      socket.onclose = () => {
        setStatus('RECONNECTING');
        console.warn("Socket dropped. Attempting reconnect in 3s...");
        reconnectInterval = setTimeout(connect, 3000);
      };

      socket.onerror = (err) => {
        console.error("WebSocket Link Failure:", err);
      };
    };

    connect();

    return () => {
      if (socket) socket.close();
      clearTimeout(reconnectInterval);
    };
  }, []);

  return (
    <div className="flex w-screen h-screen bg-slate-950 text-slate-100 overflow-hidden selection:bg-sky-500/30 font-sans">
      
      {/* Status HUD Overlay Top Left */}
      <div className="absolute top-6 left-6 z-20 pointer-events-none backdrop-blur-md bg-slate-900/40 border border-white/5 px-4 py-2 rounded-md flex items-center gap-3">
        <div className={`w-2 h-2 rounded-full animate-pulse ${status === 'CONNECTED' ? 'bg-emerald-400 shadow-[0_0_8px_#10b981]' : 'bg-amber-400 shadow-[0_0_8px_#f59e0b]'}`} />
        <span className="text-xs font-mono tracking-[0.2em] text-slate-400">LINK_STATUS: {status}</span>
      </div>

      {/* LEFT/CENTER: 70% Width - DigitalTwinCanvas */}
      <main className="relative w-[70%] h-full flex-shrink-0 border-r border-white/5">
        
        {/* Technical Grid Overlay layer */}
        <div className="absolute inset-0 pointer-events-none z-10"
          style={{
            backgroundImage: 'radial-gradient(circle at center, rgba(14,165,233,0.05) 0%, transparent 60%)'
          }}
        />

        <Canvas camera={{ position: [0, 1.5, 5], fov: 45 }}>
          <color attach="background" args={['#020617']} />
          <fog attach="fog" args={['#020617', 2, 15]} />
          
          <ambientLight intensity={0.2} />
          <directionalLight position={[10, 10, 5]} intensity={0.6} />
          
          <Grid
            position={[0, -3.5, 0]}
            args={[20, 20]}
            cellSize={1}
            cellThickness={0.5}
            cellColor="#1e293b"
            sectionSize={4}
            sectionThickness={1}
            sectionColor="#334155"
            fadeDistance={25}
          />
          
          <HumanBody highlightedMeshes={clinicalData.highlighted_meshes} />
          
          <OrbitControls 
            enablePan={false} 
            maxPolarAngle={Math.PI / 2 + 0.1}
            minDistance={3}
            maxDistance={10}
          />
        </Canvas>
      </main>

      {/* RIGHT: 30% Width - ClinicalPanel Data Readout */}
      <aside className="w-[30%] h-full relative z-20">
        {/* Directly pass received consolidated state to standard component */}
        <DataPanel 
          vitals={clinicalData.vitals} 
          conditions={clinicalData.conditions} 
        />
      </aside>

    </div>
  );
}
