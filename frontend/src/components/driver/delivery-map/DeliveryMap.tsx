'use client';

import { MapContainer, TileLayer, Marker, Circle } from 'react-leaflet'
import { Delivery } from '@/domain/entities/Delivery'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const driverIcon = L.divIcon({
  className: '',
  html: '<div style="background-color:#3B82F6;width:24px;height:24px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3)"></div>',
  iconSize: [24, 24],
  iconAnchor: [12, 12],
})

interface Props {
  delivery: Delivery
}

export function DeliveryMap({ delivery }: Props) {
  const lat = delivery.currentLat ?? -23.5505
  const lng = delivery.currentLng ?? -46.6333
  const position: [number, number] = [lat, lng]

  return (
    <div className="w-full h-48 rounded-2xl overflow-hidden">
      <MapContainer
        center={position}
        zoom={14}
        className="w-full h-full"
        zoomControl={false}
        dragging={false}
        scrollWheelZoom={false}
        touchZoom={false}
        doubleClickZoom={false}
        keyboard={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position} icon={driverIcon} />
        <Circle center={position} radius={50} pathOptions={{ color: '#3B82F6', fillOpacity: 0.1 }} />
      </MapContainer>
    </div>
  )
}
