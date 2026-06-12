'use client';

import { Delivery } from '@/domain/entities/Delivery'
import { EtaDisplay } from './EtaDisplay'
import { MapPlaceholder } from './MapPlaceholder'
import { SafeCheckToggle } from './SafeCheckToggle'
import { ChaosReportButton } from './ChaosReportButton'

interface Props {
  delivery: Delivery
}

export function ActiveDeliveryView({ delivery }: Props) {
  return (
    <div className="flex-1 flex flex-col gap-6">
      <div className="flex-1 flex flex-col items-center justify-center gap-8 bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
        <EtaDisplay delivery={delivery} />
        <MapPlaceholder delivery={delivery} />
        {delivery.id && <ChaosReportButton deliveryId={delivery.id} />}
      </div>
      <SafeCheckToggle />
    </div>
  )
}
