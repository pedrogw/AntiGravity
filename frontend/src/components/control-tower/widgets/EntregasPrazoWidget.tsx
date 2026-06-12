'use client';

export function EntregasPrazoWidget() {
  return (
    <div className="col-span-12 md:col-span-3 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <p className="text-sm font-medium text-slate-500 mb-2">Entregas no Prazo</p>
      <h4 className="text-3xl font-mono font-bold text-[#ec5b13]">94.2%</h4>
      <p className="text-xs text-red-500 mt-2 flex items-center gap-1 font-mono">
        <span>📉</span> -0.5% (24h)
      </p>
    </div>
  )
}
