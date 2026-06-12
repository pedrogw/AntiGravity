'use client';

import { Delivery } from '@/domain/entities/Delivery'
import { KanbanCard } from './KanbanCard'

interface Props {
  deliveries: Delivery[]
}

export function KanbanBoard({ deliveries }: Props) {
  const transit = deliveries.filter((d) => d.status === 'em_transito' || d.status === 'em_rota')
  const window_ = deliveries.filter((d) => d.status === 'atrasada' || d.status === 'pendente').slice(0, 2)
  const received = deliveries.filter((d) => d.status === 'entregue' || d.status === 'concluida')

  const columns = [
    {
      key: 'transit' as const,
      title: 'A Caminho',
      color: 'bg-blue-500',
      count: transit.length,
      items: transit,
    },
    {
      key: 'window' as const,
      title: 'Na Janela',
      color: 'bg-[#ec5b13]',
      count: window_.length,
      items: window_,
    },
    {
      key: 'received' as const,
      title: 'Recebido',
      color: 'bg-emerald-500',
      count: received.length,
      items: received,
    },
  ]

  return (
    <section className="flex-1 p-6 overflow-x-auto custom-scrollbar">
      <div className="max-w-7xl mx-auto h-full flex gap-6 min-w-[900px]">
        {columns.map((col) => (
          <div key={col.key} className="flex-1 flex flex-col gap-4">
            <div className="flex items-center justify-between px-2">
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${col.color}`} />
                <h3 className="font-bold text-slate-700 uppercase tracking-wide text-sm">
                  {col.title}
                </h3>
                <span className="bg-slate-200 text-slate-600 text-xs px-2 py-0.5 rounded-full font-bold">
                  {col.count}
                </span>
              </div>
              <span className="text-slate-400 cursor-pointer hover:text-slate-600 text-lg">⋯</span>
            </div>

            <div className="flex flex-col gap-3">
              {col.items.length === 0 && (
                <div className="text-sm text-slate-400 text-center py-8">
                  Nenhuma entrega
                </div>
              )}
              {col.items.map((d) => (
                <KanbanCard key={d.id} delivery={d} column={col.key} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
