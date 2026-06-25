'use client';

import { useState, useCallback } from 'react'
import { MapContainer, TileLayer, Marker, Circle, useMapEvents } from 'react-leaflet'
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
  onPositionChange?: (lat: number, lng: number) => void
}

function MapClickHandler({ onClick }: { onClick?: (lat: number, lng: number) => void }) {
  useMapEvents({
    click(e) {
      onClick?.(e.latlng.lat, e.latlng.lng)
    },
  })
  return null
}

export function DeliveryMap({ delivery, onPositionChange }: Props) {
  const [pos, setPos] = useState<[number, number]>(() => [
    delivery.currentLat ?? -23.5505,
    delivery.currentLng ?? -46.6333,
  ])

  const handleDragEnd = useCallback((e: L.LeafletEvent) => {
    const marker = e.target
    const newPos = marker.getLatLng()
    setPos([newPos.lat, newPos.lng])
    onPositionChange?.(newPos.lat, newPos.lng)
  }, [onPositionChange])

  const handleMapClick = useCallback((lat: number, lng: number) => {
    setPos([lat, lng])
    onPositionChange?.(lat, lng)
  }, [onPositionChange])

  return (
    <div className="w-full h-48 rounded-2xl overflow-hidden">
      <MapContainer
        center={pos}
        zoom={14}
        className="w-full h-full"
        zoomControl={false}
        dragging={!!onPositionChange}
        scrollWheelZoom={!!onPositionChange}
        touchZoom={!!onPositionChange}
        doubleClickZoom={!!onPositionChange}
        keyboard={!!onPositionChange}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapClickHandler onClick={onPositionChange ? handleMapClick : undefined} />
        <Marker
          position={pos}
          icon={driverIcon}
          draggable={!!onPositionChange}
          eventHandlers={onPositionChange ? { dragend: handleDragEnd } : undefined}
        />
        <Circle center={pos} radius={50} pathOptions={{ color: '#3B82F6', fillOpacity: 0.1 }} />
      </MapContainer>
    </div>
  )
}
