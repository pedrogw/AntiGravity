'use client';

import { AuthGuard } from '@/components/AuthGuard'
import { ControlTowerHeader } from '@/components/control-tower/ControlTowerHeader'
import { AlertasCriticos } from '@/components/control-tower/AlertasCriticos'
import { SimuladorCaos } from '@/components/control-tower/SimuladorCaos'
import { FrotaAtivaWidget } from '@/components/control-tower/widgets/FrotaAtivaWidget'
import { StatusFabricasWidget } from '@/components/control-tower/widgets/StatusFabricasWidget'
import { RastreamentoWidget } from '@/components/control-tower/widgets/RastreamentoWidget'
import { EntregasPrazoWidget } from '@/components/control-tower/widgets/EntregasPrazoWidget'
import { CustoLogisticoWidget } from '@/components/control-tower/widgets/CustoLogisticoWidget'
import { MonitorVeiculosWidget } from '@/components/control-tower/widgets/MonitorVeiculosWidget'
import { EficienciaWidget } from '@/components/control-tower/widgets/EficienciaWidget'

export default function ControlTowerPage() {
  return (
    <AuthGuard>
      <div className="flex h-screen overflow-hidden bg-[#f8f6f6]">
        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
          <ControlTowerHeader />

          <main className="p-6">
            <AlertasCriticos />

            <div className="bento-grid">
              <FrotaAtivaWidget />
              <StatusFabricasWidget />
              <RastreamentoWidget />
              <EntregasPrazoWidget />
              <CustoLogisticoWidget />
              <MonitorVeiculosWidget />
              <EficienciaWidget />
            </div>
          </main>
        </div>

        <SimuladorCaos />
      </div>
    </AuthGuard>
  )
}
