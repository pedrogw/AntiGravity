'use client';

export function FrotaAtivaWidget() {
  return (
    <div className="col-span-12 md:col-span-3 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <div className="flex justify-between items-start mb-4">
        <span className="text-blue-500 text-2xl">🚛</span>
        <span className="text-xs font-mono text-green-500">+2.4%</span>
      </div>
      <p className="text-sm font-medium text-slate-500">Frota Ativa</p>
      <h4 className="text-3xl font-mono font-bold mt-1">1.284</h4>
      <div className="mt-4 h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
        <div className="h-full bg-blue-500 w-[85%]" />
      </div>
    </div>
  )
}
