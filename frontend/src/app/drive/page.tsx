'use client';

import { useEffect, useCallback, useState } from 'react'
import { useRouter } from 'next/navigation'
import { AuthGuard } from '@/components/AuthGuard'
import { ActiveDeliveryView } from '@/components/driver/ActiveDeliveryView'
import { BottomNav } from '@/components/driver/BottomNav'
import { DeliveryCard } from '@/components/driver/DeliveryCard'
import { ChaosDevTools } from '@/components/chaos/ChaosDevTools'
import { useDeliveries } from '@/hooks/useDeliveries'
import { makeLogoutUseCase } from '@/infrastructure/di/factories'

export default function DrivePage() {
  const { deliveries, isLoading, error, fetchDeliveries, updateDeliveryStatus } = useDeliveries()
  const router = useRouter()
  const [toast, setToast] = useState('')

  useEffect(() => {
    fetchDeliveries()
  }, [fetchDeliveries])

  const handleLogout = useCallback(async () => {
    try {
      const logout = makeLogoutUseCase()
      await logout.execute()
    } catch {
      // Logout failure is non-critical; still redirect
    }
    localStorage.removeItem('user_email')
    router.push('/')
  }, [router])

  const showToast = (msg: string) => {
    setToast(msg)
    setTimeout(() => setToast(''), 3000)
  }

  const handleAcceptDelivery = async (id: string) => {
    try {
      await updateDeliveryStatus(id, 'aceita')
      showToast(`Oferta aceita: ${id.slice(0, 8)}`)
    } catch {
      showToast('Erro ao aceitar oferta')
    }
  }

  const handleStartRoute = async (id: string) => {
    try {
      await updateDeliveryStatus(id, 'em_transito')
      showToast(`Rota iniciada: ${id.slice(0, 8)}`)
    } catch {
      showToast('Erro ao iniciar rota')
    }
  }

  const handleCompleteDelivery = async (id: string) => {
    try {
      await updateDeliveryStatus(id, 'entregue')
      showToast(`Entrega concluída: ${id.slice(0, 8)}`)
    } catch {
      showToast('Erro ao concluir entrega')
    }
  }

  const activeDelivery = deliveries.find((d) => d.status === 'em_transito' || d.status === 'em_rota')
  const pendingDeliveries = deliveries.filter((d) => d.status === 'pendente' || d.status === 'aceita')

  return (
    <AuthGuard>
      <div className="min-h-screen bg-[#EFF6FF] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 pt-6 pb-2">
          <div>
            <h1 className="text-xs uppercase tracking-widest text-slate-500 font-bold">
              AntiGravity
            </h1>
            <p className="text-lg font-bold">Olá, Motorista</p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleLogout}
              className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
            >
              Sair
            </button>
            <div className="bg-white/50 p-2 rounded-full">
              <span>🔔</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <main className="flex-1 flex flex-col px-6 gap-6 max-w-md mx-auto w-full pb-4">
          {error && (
            <div className="p-3 text-sm text-red-700 bg-red-100 rounded" role="alert">
              {error}
            </div>
          )}

          {isLoading ? (
            <div className="flex-1 flex items-center justify-center text-sm text-slate-400">
              Carregando...
            </div>
          ) : activeDelivery ? (
            <div className="space-y-4">
              <ActiveDeliveryView delivery={activeDelivery} />
              <DeliveryCard
                delivery={activeDelivery}
                onAccept={handleAcceptDelivery}
                onStartRoute={handleStartRoute}
                onComplete={handleCompleteDelivery}
                onReportProblem={() => showToast('Problema reportado à central')}
              />
            </div>
          ) : pendingDeliveries.length > 0 ? (
            <div className="space-y-3">
              <h2 className="text-base font-semibold text-slate-700">Entregas Pendentes</h2>
              {pendingDeliveries.map((d) => (
                <DeliveryCard
                  key={d.id}
                  delivery={d}
                  onAccept={handleAcceptDelivery}
                  onStartRoute={handleStartRoute}
                  onComplete={handleCompleteDelivery}
                  onReportProblem={() => showToast('Problema reportado à central')}
                />
              ))}
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-sm text-slate-400">
              Nenhuma entrega atribuída
            </div>
          )}
        </main>

        {/* Bottom Navigation */}
        <BottomNav />

        {/* Toast */}
        {toast && (
          <div className="fixed bottom-32 left-1/2 -translate-x-1/2 z-50 px-4 py-2 bg-foreground text-background text-sm rounded-md shadow-lg">
            {toast}
          </div>
        )}

        <ChaosDevTools deliveries={deliveries} />
      </div>
    </AuthGuard>
  )
}
