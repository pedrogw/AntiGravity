'use client';

import { useEffect, useState } from 'react'
import { AuthGuard } from '@/components/AuthGuard'
import { Sidebar } from '@/components/dashboard/Sidebar'
import { JanelaRecebimento } from '@/components/dashboard/JanelaRecebimento'
import { KanbanBoard } from '@/components/dashboard/KanbanBoard'
import { StatsFooter } from '@/components/dashboard/StatsFooter'
import { ChaosDevTools } from '@/components/chaos/ChaosDevTools'
import { CriarEntregaDialog } from '@/components/dashboard/CriarEntregaDialog'
import { Button } from '@/components/ui/button'
import { useDeliveries } from '@/hooks/useDeliveries'

export default function DashboardPage() {
  const { deliveries, isLoading, error, fetchDeliveries } = useDeliveries()
  const [dialogOpen, setDialogOpen] = useState(false)

  useEffect(() => {
    fetchDeliveries()
  }, [fetchDeliveries])

  return (
    <AuthGuard>
      <div className="min-h-screen bg-[#f8f6f6] flex">
        <Sidebar />

        <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
          <JanelaRecebimento />

          <div className="px-6 pt-4 flex items-center justify-between">
            <div />
            <Button onClick={() => setDialogOpen(true)}>
              Nova Entrega
            </Button>
          </div>

          {error && (
            <div className="px-6 pt-4">
              <div className="p-3 text-sm text-red-700 bg-red-100 rounded" role="alert">
                {error}
              </div>
            </div>
          )}

          <CriarEntregaDialog open={dialogOpen} onOpenChange={setDialogOpen} />

          {isLoading ? (
            <div className="flex-1 flex items-center justify-center text-sm text-slate-400">
              Carregando...
            </div>
          ) : (
            <KanbanBoard deliveries={deliveries} />
          )}

          <StatsFooter deliveries={deliveries} />
        </main>

        <ChaosDevTools deliveries={deliveries} />
      </div>
    </AuthGuard>
  )
}
