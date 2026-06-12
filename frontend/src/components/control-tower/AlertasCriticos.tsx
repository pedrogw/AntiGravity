'use client';

const alerts = [
  { id: 'ALERTA #8842', title: 'SP-RJ: Quebra Mecânica', level: 'critical', action: 'RESOLVER' },
  { id: 'ALERTA #9102', title: 'Planta Curitiba: Greve Fiscal', level: 'critical', action: 'DETALHES' },
  { id: 'AVISO #7721', title: 'Bloqueio Rodoviário BR-101', level: 'warning', action: 'VER ROTA' },
] as const

export function AlertasCriticos() {
  return (
    <div className="mb-6 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-bold uppercase tracking-widest text-red-500 flex items-center gap-2">
          <span>🔴</span> Alertas Críticos (3)
        </h3>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {alerts.map((a) => (
          <div
            key={a.id}
            className={`bg-white border-l-4 shadow-sm p-4 rounded-lg flex justify-between items-center group ${
              a.level === 'critical' ? 'border-red-500' : 'border-amber-500'
            }`}
          >
            <div>
              <p className={`text-xs font-mono ${a.level === 'critical' ? 'text-red-500' : 'text-amber-500'}`}>
                {a.id}
              </p>
              <p className="text-sm font-semibold">{a.title}</p>
            </div>
            <button
              className={`text-xs px-3 py-1 rounded-full font-bold transition-all ${
                a.level === 'critical'
                  ? 'bg-red-50 text-red-600 hover:bg-red-500 hover:text-white'
                  : 'bg-amber-50 text-amber-600 hover:bg-amber-500 hover:text-white'
              }`}
            >
              {a.action}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
