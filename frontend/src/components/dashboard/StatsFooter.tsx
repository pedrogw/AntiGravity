'use client';

import { Delivery } from '@/domain/entities/Delivery'

interface Props {
  deliveries: Delivery[]
}

export function StatsFooter({ deliveries }: Props) {
  const total = deliveries.length
  const received = deliveries.filter((d) => d.status === 'entregue' || d.status === 'concluida').length
  const active = deliveries.filter((d) => d.status === 'em_transito' || d.status === 'em_rota').length
  const dockPct = total > 0 ? Math.round((active / total) * 100) : 0

  return (
    <footer className="bg-white border-t border-slate-200 px-6 py-3 flex justify-between items-center text-xs font-medium text-slate-500">
      <div className="flex gap-6">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#ec5b13]" />
          <span>Ocupação das Docas: {dockPct}%</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-500" />
          <span>Entregues: {received}</span>
        </div>
      </div>
      <div>
        <span>Última atualização: {new Date().toLocaleString('pt-BR', { hour: '2-digit', minute: '2-digit' })}</span>
      </div>
    </footer>
  )
}
