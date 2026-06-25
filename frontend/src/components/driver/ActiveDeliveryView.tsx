'use client';

import dynamic from 'next/dynamic'
import { Delivery } from '@/domain/entities/Delivery'
import { EtaDisplay } from './EtaDisplay'
import { SafeCheckToggle } from './SafeCheckToggle'
import { DeliveryCard } from './DeliveryCard'

const DeliveryMap = dynamic(
  () => import('./delivery-map/DeliveryMap').then((m) => m.DeliveryMap),
  { ssr: false },
)

interface StoreLocation {
  lat: number
  lng: number
}

interface Props {
  delivery: Delivery
  onAccept?: (id: string) => void
  onStartRoute?: (id: string) => void
  onComplete?: (id: string) => void
  onCancel?: (id: string) => void
  onPositionChange?: (lat: number, lng: number) => void
  storeLocation?: StoreLocation
}

export function ActiveDeliveryView({
  delivery,
  onAccept,
  onStartRoute,
  onComplete,
  onCancel,
  onPositionChange,
  storeLocation,
}: Props) {
  return (
    <div className="flex-1 flex flex-col gap-6">
      <div className="flex-1 flex flex-col items-center justify-center gap-8 bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
        <EtaDisplay delivery={delivery} />
        <DeliveryMap delivery={delivery} onPositionChange={onPositionChange} storeLocation={storeLocation} />
      </div>
      <DeliveryCard
        delivery={delivery}
        onAccept={onAccept || (() => {})}
        onStartRoute={onStartRoute || (() => {})}
        onComplete={onComplete}
        onCancel={onCancel}
      />
      <SafeCheckToggle />
    </div>
  )
}
