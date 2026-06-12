'use client';

export function RastreamentoWidget() {
  return (
    <div className="col-span-12 md:col-span-6 row-span-2 bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="p-4 border-b border-slate-200 flex justify-between items-center">
        <h4 className="text-sm font-bold flex items-center gap-2">
          <span className="text-blue-500 text-lg">🗺️</span> Rastreamento em Tempo Real
        </h4>
        <div className="flex gap-2">
          <button className="text-[10px] font-mono border border-slate-300 px-2 py-0.5 rounded hover:bg-slate-50">
            FROTA_A
          </button>
          <button className="text-[10px] font-mono border border-slate-300 px-2 py-0.5 rounded hover:bg-slate-50">
            FROTA_B
          </button>
        </div>
      </div>
      <div className="flex-1 bg-slate-200 relative min-h-[300px]">
        <div className="absolute top-4 left-4 bg-white/90 p-2 rounded shadow-lg text-[10px] font-mono flex items-center gap-2">
          <span className="text-blue-500">📍</span>
          LAT: -23.5505 | LONG: -46.6333
        </div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-[#ec5b13] text-3xl drop-shadow-md">
          📍
        </div>
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-slate-300 flex items-center justify-center">
          <div className="text-center text-slate-400">
            <div className="text-lg">Mapa Logístico</div>
            <div className="text-xs font-mono mt-1">São Paulo, Brazil</div>
          </div>
        </div>
      </div>
    </div>
  )
}
