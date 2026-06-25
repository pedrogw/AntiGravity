'use client';

import { Delivery } from '@/domain/entities/Delivery'
import { EtaDisplay } from './EtaDisplay'
import { MapPlaceholder } from './MapPlaceholder'
import { SafeCheckToggle } from './SafeCheckToggle'
import { ChaosReportButton } from './ChaosReportButton'
import { DeliveryCard } from './DeliveryCard'

interface Props {
  delivery: Delivery
  onAccept?: (id: string) => void
  onStartRoute?: (id: string) => void
  onComplete?: (id: string) => void
  onReportProblem?: (id: string) => void
}

export function ActiveDeliveryView({
  delivery,
  onAccept,
  onStartRoute,
  onComplete,
  onReportProblem,
}: Props) {
  return (
    <div className="flex-1 flex flex-col gap-6">
      <div className="flex-1 flex flex-col items-center justify-center gap-8 bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
        <EtaDisplay delivery={delivery} />
        <MapPlaceholder delivery={delivery} />
        {delivery.id && <ChaosReportButton deliveryId={delivery.id} />}
      </div>
      <DeliveryCard
        delivery={delivery}
        onAccept={onAccept || (() => {})}
        onStartRoute={onStartRoute || (() => {})}
        onComplete={onComplete}
        onReportProblem={onReportProblem || (() => {})}
      />
      <SafeCheckToggle />
    </div>
  )
}
