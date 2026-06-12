'use client';

export function EficienciaWidget() {
  return (
    <div className="col-span-12 md:col-span-4 bg-[#ec5b13] text-white p-6 rounded-xl shadow-lg flex flex-col justify-between">
      <div>
        <p className="text-xs font-mono uppercase opacity-80 tracking-widest flex items-center gap-2">
          🌿 Eficiência Energética
        </p>
        <h4 className="text-4xl font-mono font-bold mt-2">82%</h4>
      </div>
      <div className="mt-8 space-y-3">
        <div className="flex justify-between text-xs border-b border-white/20 pb-2">
          <span>Redução CO₂</span>
          <span className="font-mono">14.2t</span>
        </div>
        <div className="flex justify-between text-xs border-b border-white/20 pb-2">
          <span>Frota Elétrica</span>
          <span className="font-mono">128 un.</span>
        </div>
      </div>
      <button className="mt-6 w-full py-2 bg-white text-[#ec5b13] font-bold rounded-lg text-sm hover:bg-slate-100 transition-colors flex items-center justify-center gap-2">
        📄 RELATÓRIO ESG
      </button>
    </div>
  )
}
