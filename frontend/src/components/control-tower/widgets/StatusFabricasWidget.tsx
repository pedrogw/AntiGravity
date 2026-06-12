'use client';

export function StatusFabricasWidget() {
  return (
    <div className="col-span-12 md:col-span-3 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <div className="flex justify-between items-start mb-4">
        <span className="text-[#ec5b13] text-2xl">🏭</span>
        <span className="text-xs font-mono text-green-500">+0.1%</span>
      </div>
      <p className="text-sm font-medium text-slate-500">Status Fábricas</p>
      <h4 className="text-3xl font-mono font-bold mt-1">98.5%</h4>
      <div className="mt-4 flex gap-1">
        <div className="h-2 flex-1 bg-green-500 rounded-sm" />
        <div className="h-2 flex-1 bg-green-500 rounded-sm" />
        <div className="h-2 flex-1 bg-green-500 rounded-sm" />
        <div className="h-2 flex-1 bg-red-500 rounded-sm" />
      </div>
    </div>
  )
}
