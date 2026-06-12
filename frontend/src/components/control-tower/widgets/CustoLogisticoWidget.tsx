'use client';

export function CustoLogisticoWidget() {
  return (
    <div className="col-span-12 md:col-span-3 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <p className="text-sm font-medium text-slate-500 mb-2">Custo Logístico/Km</p>
      <h4 className="text-3xl font-mono font-bold">R$ 4.12</h4>
      <div className="mt-4 h-1 w-full bg-slate-100 rounded-full">
        <div className="h-full bg-[#ec5b13] w-[60%]" />
      </div>
    </div>
  )
}
