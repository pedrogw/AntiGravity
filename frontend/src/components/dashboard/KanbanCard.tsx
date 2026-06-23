'use client';

import { useState, useEffect } from 'react'
import { Delivery } from '@/domain/entities/Delivery'

const statusLabel: Record<string, string> = {
  pendente: 'Pendente',
  em_transito: 'Em Trânsito',
  em_rota: 'Em Rota',
  entregue: 'Entregue',
  concluida: 'Concluída',
  atrasada: 'Atrasada',
  cancelada: 'Cancelada',
}

interface Props {
  delivery: Delivery
  column: 'transit' | 'window' | 'received'
}

export function KanbanCard({ delivery, column }: Props) {
  const [now, setNow] = useState(Date.now)

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 30000)
    return () => clearInterval(timer)
  }, [])

  if (column === 'transit') {
    return (
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-blue-400/50 transition-all group">
        <div className="flex justify-between items-start mb-3">
          <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">
            #{delivery.id?.slice(0, 8)}
          </span>
          <span className="text-slate-300 group-hover:text-blue-500 transition-colors text-lg">🚛</span>
        </div>
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-slate-500">
            <span className="text-xs">🕐</span>
            <span className="text-sm font-medium">
              ETA: {delivery.etaCurrent ? new Date(delivery.etaCurrent).toLocaleTimeString('pt-BR') : '—'}
            </span>
          </div>
          <div className="flex items-center gap-2 text-slate-500">
            <span className="text-xs">📍</span>
            <span className="text-sm">{delivery.storeId.slice(0, 8)}</span>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center">
          <div className="flex -space-x-2">
            <div className="w-6 h-6 rounded-full border-2 border-white bg-blue-100 flex items-center justify-center text-[10px] font-bold text-blue-700">
              {delivery.driverId.slice(0, 2)}
            </div>
          </div>
          <span className="text-[10px] font-bold text-slate-400 uppercase">Prioridade Alta</span>
        </div>
      </div>
    )
  }

  if (column === 'window') {
    const progress = delivery.etaCurrent
      ? Math.max(0, Math.min(Math.floor((now - new Date(delivery.etaCurrent).getTime()) / 60000), 100))
      : 0
    const dockNumber = (delivery.id?.charCodeAt(0) || 1) % 8 + 1

    return (
      <div className="bg-white p-4 rounded-xl border-l-4 border-l-[#ec5b13] border border-slate-200 shadow-md">
        <div className="flex justify-between items-start mb-3">
          <span className="text-xs font-bold text-[#ec5b13] bg-[#ec5b13]/10 px-2 py-1 rounded">
            #{delivery.id?.slice(0, 8)}
          </span>
          <span className="px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 text-[10px] font-bold uppercase">
            {delivery.status === 'atrasada' ? 'Atrasado' : 'Descarregando'}
          </span>
        </div>
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-slate-500">
            <span className="text-xs">🏭</span>
            <span className="text-sm font-bold text-slate-700">DOCA 0{dockNumber}</span>
          </div>
          <div className="flex items-center gap-2 text-slate-500">
            <span className="text-xs">⏱</span>
            <span className="text-sm">Tempo: {progress} min</span>
          </div>
        </div>
        <div className="mt-4 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
          <div
            className="bg-[#ec5b13] h-full rounded-full transition-all"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
        </div>
      </div>
    )
  }

  const receivedDock = (delivery.id?.charCodeAt(delivery.id.length - 1) || 1) % 5 + 1

  return (
    <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 opacity-80">
      <div className="flex justify-between items-start mb-3">
        <span className="text-xs font-bold text-slate-500 bg-slate-200 px-2 py-1 rounded">
          #{delivery.id?.slice(0, 8)}
        </span>
        <span className="text-emerald-500 text-lg">✓</span>
      </div>
      <div className="space-y-1">
        <p className="text-sm font-semibold text-slate-700">
          {delivery.etaCurrent
            ? `Concluído às ${new Date(delivery.etaCurrent).toLocaleTimeString('pt-BR')}`
            : statusLabel[delivery.status] || delivery.status}
        </p>
        <p className="text-xs text-slate-500">Docas: 0{receivedDock}</p>
      </div>
    </div>
  )
}
