'use client';

import { useState } from 'react'
import { apiClient } from '@/infrastructure/api/api_client'

interface Props {
  deliveryId: string
}

export function ChaosReportButton({ deliveryId }: Props) {
  const [loading, setLoading] = useState(false)
  const [done, setDone] = useState(false)
  const [error, setError] = useState(false)

  const handleReport = async () => {
    setLoading(true)
    setError(false)
    try {
      await apiClient.post(`/deliveries/${deliveryId}/chaos`, {
        event_type: 'reporte_motorista',
        delay_minutes: 0,
        impact_factor: 1.0,
      })
      setDone(true)
      setTimeout(() => setDone(false), 3000)
    } catch {
      setError(true)
      setTimeout(() => setError(false), 3000)
    } finally {
      setLoading(false)
    }
  }

  const feedback = error ? 'Falha ao reportar' : done ? 'Reportado ✓' : 'Reportar Evento (Caos)'
  const bg = error ? 'bg-red-600 hover:bg-red-700' : 'bg-[#F97316] hover:bg-[#ec5b13]'

  return (
    <button
      onClick={handleReport}
      disabled={loading}
      className={`w-full ${bg} transition-colors text-white py-5 rounded-2xl flex items-center justify-center gap-3 shadow-lg shadow-orange-500/20 active:scale-[0.98] disabled:opacity-60 font-bold`}
    >
      <span>⚠️</span>
      <span className="text-lg">{feedback}</span>
    </button>
  )
}
