'use client';

import { Delivery } from '@/domain/entities/Delivery'

interface Props {
  delivery: Delivery
}

export function EtaDisplay({ delivery }: Props) {
  const eta = delivery.etaCurrent
    ? new Date(delivery.etaCurrent).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    : '—'

  return (
    <div className="text-center">
      <p className="text-slate-500 text-sm font-medium mb-2 uppercase tracking-tight">ETA Atual</p>
      <h2 className="text-7xl font-mono font-bold text-slate-900">{eta}</h2>
    </div>
  )
}
