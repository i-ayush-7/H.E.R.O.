import React from 'react';
import { Activity, Heart, Wind, AlertTriangle, ChevronRight } from 'lucide-react';

export function DataPanel({ vitals = {}, conditions = [] }) {
  return (
    <div className="h-full w-full p-8 bg-slate-900/50 backdrop-blur-lg flex flex-col gap-8 border-l border-white/5 overflow-y-auto">
      
      {/* Header Row */}
      <div className="flex justify-between items-start mb-2">
        <div className="flex flex-col">
          <h2 className="text-sm font-mono tracking-[.3em] text-sky-400 uppercase mb-1 flex items-center gap-2">
            <Activity className="w-4 h-4" /> Digital Twin
          </h2>
          <h1 className="text-2xl font-bold tracking-tight text-white font-sans">Patient Vitals</h1>
        </div>
        <div className="text-[10px] font-mono text-slate-500 border border-slate-800 px-2 py-1 rounded">
          REF_312-X
        </div>
      </div>

      <hr className="border-white/5 w-full" />

      {/* Section 1: Dynamic Vitals from Stream */}
      <section className="flex flex-col gap-4">
        <header className="flex items-center gap-2">
          <Heart className="w-4 h-4 text-slate-400" />
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Biometric Feed</h3>
        </header>

        <div className="grid grid-cols-2 gap-4">
          
          {/* Card Metric: Heart Rate */}
          <div className="bg-white/[0.02] border border-white/5 rounded-xl p-4 relative group hover:border-white/10 transition-all">
            <p className="text-[10px] uppercase font-medium tracking-widest text-slate-500 mb-2">Heart Rate</p>
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-light text-white tabular-nums">{vitals.heartRate}</span>
              <span className="text-xs text-slate-500">BPM</span>
            </div>
          </div>

          {/* Card Metric: SpO2 */}
          <div className="bg-white/[0.02] border border-white/5 rounded-xl p-4 group hover:border-white/10 transition-all">
            <p className="text-[10px] uppercase font-medium tracking-widest text-slate-500 mb-2 flex items-center gap-1">
               <Wind className="w-3 h-3" /> SpO2
            </p>
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-light text-sky-300 tabular-nums">{vitals.spo2}</span>
              <span className="text-xs text-slate-500">%</span>
            </div>
          </div>

          {/* Spanning Card: BP */}
          <div className="bg-white/[0.02] border border-white/5 rounded-xl p-4 col-span-2 relative overflow-hidden group hover:border-white/10 transition-all">
            <div className="absolute right-4 top-1/2 -translate-y-1/2 w-1 h-8 bg-white/5 rounded-full" />
            <p className="text-[10px] uppercase font-medium tracking-widest text-slate-500 mb-2">Arterial Pressure</p>
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-light text-white tracking-wide tabular-nums">{vitals.bloodPressure}</span>
              <span className="text-xs text-slate-500 ml-1">mmHg</span>
            </div>
          </div>

        </div>
      </section>

      {/* Section 2: Conditions and Alerts */}
      <section className="flex flex-col gap-4 flex-grow">
        <header className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-400/70" />
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Active Diagnoses</h3>
        </header>

        <div className="flex flex-col gap-3">
          {conditions.length > 0 ? (
            conditions.map((cond, i) => (
              <div key={i} className="flex items-center justify-between bg-white/[0.02] hover:bg-white/[0.04] border border-white/5 px-4 py-3 rounded-lg transition-colors cursor-pointer group">
                <div className="flex items-center gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)] group-hover:scale-125 transition-transform" />
                  <span className="text-sm text-slate-200 font-medium">{cond}</span>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-white transition-colors" />
              </div>
            ))
          ) : (
            <div className="border border-dashed border-slate-800 rounded-lg p-6 text-center">
              <p className="text-xs text-slate-500 italic">Waiting for diagnostic stream...</p>
            </div>
          )}
        </div>
      </section>

      {/* Footer Branding */}
      <div className="mt-auto border-t border-white/5 pt-6 flex items-center justify-between opacity-50">
         <span className="text-[9px] font-mono tracking-widest uppercase">Secure SHARP Socket v2.4</span>
         <div className="h-1 w-12 bg-gradient-to-r from-sky-500 to-indigo-600 rounded-full" />
      </div>
    </div>
  );
}
