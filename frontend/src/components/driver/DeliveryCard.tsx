'use client';

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
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

const statusActions: Record<string, string> = {
  pendente: 'em_transito',
  em_transito: 'entregue',
  em_rota: 'entregue',
}

interface Props {
  delivery: Delivery
  onStartRoute: (id: string) => void
  onComplete?: (id: string) => void
  onReportProblem: (id: string) => void
}

export function DeliveryCard({ delivery, onStartRoute, onComplete, onReportProblem }: Props) {
  const deliveryId = delivery.id

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">Entrega #{deliveryId?.slice(0, 8) || '...'}</CardTitle>
          <Badge>{statusLabel[delivery.status] || delivery.status}</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-muted-foreground">Fábrica</span>
          <span className="font-medium">{delivery.factoryId.slice(0, 8)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted-foreground">Loja</span>
          <span className="font-medium">{delivery.storeId.slice(0, 8)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted-foreground">ETA</span>
          <span className="font-medium">
            {delivery.etaCurrent
              ? new Date(delivery.etaCurrent).toLocaleTimeString('pt-BR')
              : '—'}
          </span>
        </div>
        {delivery.departedAt && (
          <div className="flex justify-between">
            <span className="text-muted-foreground">Partida</span>
            <span className="font-medium">
              {new Date(delivery.departedAt).toLocaleTimeString('pt-BR')}
            </span>
          </div>
        )}
      </CardContent>
      <CardFooter className="gap-2 flex-wrap">
        {delivery.status === 'pendente' && deliveryId && (
          <Button size="sm" onClick={() => onStartRoute(deliveryId)}>
            Iniciar Rota
          </Button>
        )}
        {delivery.status === 'em_transito' && deliveryId && onComplete && (
          <Button size="sm" variant="default" onClick={() => onComplete(deliveryId)}>
            Concluir Entrega
          </Button>
        )}
        {deliveryId && (
          <Button
            size="sm"
            variant="outline"
            onClick={() => onReportProblem(deliveryId)}
          >
            Reportar Problema
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}
