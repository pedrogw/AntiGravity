'use client';

const vehicles = [
  { id: '#TRK-774', driver: 'R. Santos', cargo: 'Perecíveis', status: 'EM ROTA', statusColor: 'green', progress: 78 },
  { id: '#TRK-812', driver: 'M. Lima', cargo: 'Eletrônicos', status: 'PARADO', statusColor: 'amber', progress: 45 },
  { id: '#TRK-233', driver: 'J. Ferreira', cargo: 'Automotivo', status: 'COLETA', statusColor: 'blue', progress: 10 },
] as const

const statusStyles: Record<string, string> = {
  green: 'bg-green-100 text-green-700',
  amber: 'bg-amber-100 text-amber-700',
  blue: 'bg-blue-100 text-blue-700',
}

const barStyles: Record<string, string> = {
  green: 'bg-blue-500',
  amber: 'bg-amber-500',
  blue: 'bg-slate-400',
}

export function MonitorVeiculosWidget() {
  return (
    <div className="col-span-12 md:col-span-8 bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-4 border-b border-slate-200 flex justify-between items-center">
        <h4 className="text-sm font-bold flex items-center gap-2">
          Monitor de Veículos (High Priority)
        </h4>
        <span className="text-[10px] font-mono text-slate-400 flex items-center gap-1">
          SYNC: AGORA
        </span>
      </div>
      <table className="w-full text-left text-xs">
        <thead className="bg-slate-50 text-slate-500 uppercase">
          <tr>
            <th className="px-4 py-2 font-semibold">ID</th>
            <th className="px-4 py-2 font-semibold">Condutor</th>
            <th className="px-4 py-2 font-semibold">Carga</th>
            <th className="px-4 py-2 font-semibold">Status</th>
            <th className="px-4 py-2 font-semibold">Progresso</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {vehicles.map((v) => (
            <tr key={v.id}>
              <td className="px-4 py-3 font-mono">{v.id}</td>
              <td className="px-4 py-3">{v.driver}</td>
              <td className="px-4 py-3">{v.cargo}</td>
              <td className="px-4 py-3">
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${statusStyles[v.statusColor]}`}>
                  {v.status}
                </span>
              </td>
              <td className="px-4 py-3">
                <div className="w-24 h-1.5 bg-slate-100 rounded-full">
                  <div className={`h-full ${barStyles[v.statusColor]} rounded-full`} style={{ width: `${v.progress}%` }} />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
