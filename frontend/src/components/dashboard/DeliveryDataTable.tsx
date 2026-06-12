'use client';

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
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

const statusVariant: Record<string, 'default' | 'secondary' | 'success' | 'warning' | 'destructive'> = {
  pendente: 'secondary',
  em_rota: 'default',
  em_transito: 'default',
  entregue: 'success',
  concluida: 'success',
  atrasada: 'destructive',
  cancelada: 'secondary',
}

interface Props {
  deliveries: Delivery[]
}

export function DeliveryDataTable({ deliveries }: Props) {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Fábrica</TableHead>
            <TableHead>Loja</TableHead>
            <TableHead>Motorista</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>ETA</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {deliveries.length === 0 && (
            <TableRow>
              <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                Nenhuma entrega encontrada
              </TableCell>
            </TableRow>
          )}
          {deliveries.map((d) => (
            <TableRow key={d.id}>
              <TableCell className="font-mono text-xs">{d.id?.slice(0, 8)}</TableCell>
              <TableCell>{d.factoryId.slice(0, 8)}</TableCell>
              <TableCell>{d.storeId.slice(0, 8)}</TableCell>
              <TableCell>{d.driverId.slice(0, 8)}</TableCell>
              <TableCell>
                <Badge variant={statusVariant[d.status] || 'secondary'}>
                  {statusLabel[d.status] || d.status}
                </Badge>
              </TableCell>
              <TableCell className="text-muted-foreground">
                {d.etaCurrent
                  ? new Date(d.etaCurrent).toLocaleTimeString('pt-BR')
                  : '—'}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
