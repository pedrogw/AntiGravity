'use client';

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { apiClient } from '@/infrastructure/api/api_client'
import { Delivery } from '@/domain/entities/Delivery'

interface Props {
  deliveries?: Delivery[]
}

const chaosActions = [
  { id: 'delay', label: 'Atrasar Entrega', eventType: 'atraso', icon: '⏱' },
  { id: 'lose', label: 'Perder Pacote', eventType: 'perda', icon: '📦' },
  { id: 'gps', label: 'Falha de GPS', eventType: 'falha_gps', icon: '📡' },
  { id: 'reroute', label: 'Redirecionar Rota', eventType: 'redirecionamento', icon: '🔄' },
] as const

const TEST_ACCOUNTS = [
  'lojista@antigravity.com',
  'motorista@antigravity.com',
  'admin@antigravity.com',
];

export function ChaosDevTools({ deliveries }: Props) {
  const [userEmail] = useState(() => {
    if (typeof window === 'undefined') return '';
    return localStorage.getItem('user_email') || '';
  });
  const [open, setOpen] = useState(false)
  const [logs, setLogs] = useState<string[]>([])
  const [selectedId, setSelectedId] = useState('')
  const [delayMinutes, setDelayMinutes] = useState(15)
  const [simLat, setSimLat] = useState('-23.5505')
  const [simLng, setSimLng] = useState('-46.6333')

  if (!TEST_ACCOUNTS.includes(userEmail)) return null;

  const triggerChaos = async (action: typeof chaosActions[number]) => {
    const deliveryId = selectedId || deliveries?.[0]?.id
    if (!deliveryId) {
      setLogs((prev) => [`[Caos] Selecione uma entrega primeiro`, ...prev])
      return
    }

    const msg = `[Caos] ${action.label} → entrega ${deliveryId.slice(0, 8)} (${new Date().toLocaleTimeString('pt-BR')})`
    try {
      await apiClient.post(`/deliveries/${deliveryId}/chaos`, {
        event_type: action.eventType,
        delay_minutes: delayMinutes,
        impact_factor: action.id === 'delay' ? 1.5 : 1.0,
      })
      setLogs((prev) => [msg, ...prev])
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { detail?: string } }; message?: string };
      const detail = axiosErr?.response?.data?.detail || axiosErr?.message || 'Erro desconhecido';
      setLogs((prev) => [`${msg} — ERRO: ${detail}`, ...prev])
    }
  }

  const updatePosition = async () => {
    const deliveryId = selectedId || deliveries?.[0]?.id
    if (!deliveryId) {
      setLogs((prev) => [`[Posição] Selecione uma entrega primeiro`, ...prev])
      return
    }

    const msg = `[Posição] Simular → ${simLat}, ${simLng} (${new Date().toLocaleTimeString('pt-BR')})`
    try {
      await apiClient.patch(`/deliveries/${deliveryId}`, { lat: Number(simLat), lng: Number(simLng) })
      setLogs((prev) => [msg, ...prev])
    } catch (err: unknown) {
      const axiosErr = err as { response?: { data?: { detail?: string } }; message?: string };
      const detail = axiosErr?.response?.data?.detail || axiosErr?.message || 'Erro desconhecido';
      setLogs((prev) => [`${msg} — ERRO: ${detail}`, ...prev])
    }
  }

  if (!open) {
    return (
      <Button
        className="fixed bottom-4 right-4 z-50 h-12 w-12 rounded-full shadow-lg"
        onClick={() => setOpen(true)}
        title="Abrir Chaos DevTools"
      >
        ⚡
      </Button>
    )
  }

  return (
    <Card className="fixed bottom-4 right-4 z-50 w-80 shadow-xl">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm">Chaos DevTools</CardTitle>
        <Button variant="ghost" size="sm" onClick={() => setOpen(false)}>
          ✕
        </Button>
      </CardHeader>
      <CardContent className="space-y-3">
        {deliveries && deliveries.length > 0 && (
          <div>
            <label className="text-xs text-muted-foreground">Entrega</label>
            <select
              className="flex h-8 w-full rounded-md border border-input bg-transparent px-2 text-xs"
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
            >
              <option value="">Primeira disponível</option>
              {deliveries.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.id?.slice(0, 8)} — {d.status}
                </option>
              ))}
            </select>
          </div>
        )}

        <div>
          <label className="text-xs text-muted-foreground">Atraso (min)</label>
          <Input
            type="number"
            value={delayMinutes}
            onChange={(e) => setDelayMinutes(Number(e.target.value))}
            className="h-8 text-xs"
            min={0}
          />
        </div>

        <div className="grid grid-cols-2 gap-2">
          {chaosActions.map((action) => (
            <Button
              key={action.id}
              variant="destructive"
              size="sm"
              onClick={() => triggerChaos(action)}
            >
              {action.icon} {action.label}
            </Button>
          ))}
        </div>

        <div className="border-t pt-2">
          <div className="text-xs font-medium text-muted-foreground mb-1">Simular Posição</div>
          <div className="flex gap-2">
            <Input
              type="text"
              value={simLat}
              onChange={(e) => setSimLat(e.target.value)}
              className="h-8 text-xs flex-1"
              placeholder="Latitude"
            />
            <Input
              type="text"
              value={simLng}
              onChange={(e) => setSimLng(e.target.value)}
              className="h-8 text-xs flex-1"
              placeholder="Longitude"
            />
          </div>
          <Button variant="outline" size="sm" className="w-full mt-1" onClick={updatePosition}>
            Atualizar
          </Button>
        </div>

        {logs.length > 0 && (
          <div className="space-y-1">
            <div className="text-xs font-medium text-muted-foreground">Log</div>
            <div className="max-h-32 overflow-auto space-y-0.5">
              {logs.map((log, i) => (
                <div key={i} className="text-xs text-destructive font-mono">
                  {log}
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
