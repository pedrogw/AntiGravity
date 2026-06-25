'use client';

import { useState } from 'react'
import { apiClient } from '@/infrastructure/api/api_client'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog'

interface ProblemType {
  type: string
  label: string
  description: string
  delayMinutes: number
  impactFactor: number
}

const PROBLEM_TYPES: ProblemType[] = [
  { type: 'reporte_transito', label: 'Trânsito', description: 'Trânsito intenso ou congestionamento', delayMinutes: 15, impactFactor: 1.5 },
  { type: 'reporte_acidente', label: 'Acidente', description: 'Acidente na via', delayMinutes: 45, impactFactor: 2.5 },
  { type: 'reporte_mecanico', label: 'Mecânico', description: 'Problema mecânico no veículo', delayMinutes: 30, impactFactor: 2.0 },
  { type: 'reporte_clima', label: 'Clima', description: 'Condições climáticas adversas', delayMinutes: 20, impactFactor: 1.3 },
  { type: 'reporte_estrada_bloqueada', label: 'Estrada bloqueada', description: 'Estrada interditada ou bloqueada', delayMinutes: 40, impactFactor: 2.0 },
  { type: 'reporte_outro', label: 'Outro', description: 'Outro tipo de problema', delayMinutes: 5, impactFactor: 1.1 },
]

interface Props {
  deliveryId: string
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function ReportProblemDialog({ deliveryId, open, onOpenChange }: Props) {
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (problem: ProblemType) => {
    setLoading(true)
    setError(null)
    try {
      await apiClient.post(`/deliveries/${deliveryId}/chaos`, {
        event_type: problem.type,
        delay_minutes: problem.delayMinutes,
        impact_factor: problem.impactFactor,
      })
      setSubmitted(true)
      setTimeout(() => {
        onOpenChange(false)
        setSubmitted(false)
      }, 2000)
    } catch {
      setError('Falha ao reportar problema. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Reportar Problema</DialogTitle>
          <DialogDescription>
            Selecione o tipo de problema encontrado na entrega.
          </DialogDescription>
        </DialogHeader>
        {submitted ? (
          <div className="py-8 text-center text-green-600 font-medium">
            Problema reportado com sucesso ✓
          </div>
        ) : (
          <div className="grid gap-2">
            {PROBLEM_TYPES.map((p) => (
              <button
                key={p.type}
                onClick={() => handleSubmit(p)}
                disabled={loading}
                className="w-full text-left p-3 rounded-lg border border-slate-200 hover:border-slate-400 hover:bg-slate-50 transition-colors disabled:opacity-50"
              >
                <div className="font-medium text-sm">{p.label}</div>
                <div className="text-xs text-slate-500">{p.description}</div>
              </button>
            ))}
            {error && (
              <div className="text-sm text-red-600 text-center mt-2">{error}</div>
            )}
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
