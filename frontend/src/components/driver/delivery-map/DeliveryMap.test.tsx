import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Delivery } from '@/domain/entities/Delivery';

vi.mock('react-leaflet', () => {
  const FakeMapContainer = ({ children, center, zoom }: Record<string, unknown>) => (
    <div data-testid="map-container" data-center={JSON.stringify(center)} data-zoom={String(zoom)}>
      {children as React.ReactNode}
    </div>
  )
  return {
    MapContainer: FakeMapContainer,
    TileLayer: () => <div data-testid="tile-layer" />,
    Marker: () => <div data-testid="marker" />,
    Circle: () => <div data-testid="circle" />,
  }
});

vi.mock('leaflet', () => ({
  default: { divIcon: vi.fn(() => ({})) },
  divIcon: vi.fn(() => ({})),
}));

vi.mock('leaflet/dist/leaflet.css', () => ({}));

import { DeliveryMap } from './DeliveryMap';

function makeDelivery(overrides: Partial<{ lat: number; lng: number }> = {}): Delivery {
  return new Delivery(
    {
      factoryId: '00000000-0000-0000-0000-000000000001',
      storeId: '00000000-0000-0000-0000-000000000002',
      driverId: '00000000-0000-0000-0000-000000000003',
      currentLat: overrides.lat,
      currentLng: overrides.lng,
    },
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  );
}

describe('DeliveryMap', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renderiza MapContainer com coordenadas do driver', () => {
    render(<DeliveryMap delivery={makeDelivery({ lat: -23.55, lng: -46.63 })} />);
    const container = screen.getByTestId('map-container');
    expect(container).toBeInTheDocument();
    expect(container).toHaveAttribute('data-center', JSON.stringify([-23.55, -46.63]));
    expect(container).toHaveAttribute('data-zoom', '14');
  });

  it('usa fallback SP quando não há coordenadas', () => {
    render(<DeliveryMap delivery={makeDelivery()} />);
    const container = screen.getByTestId('map-container');
    expect(container).toHaveAttribute('data-center', JSON.stringify([-23.5505, -46.6333]));
  });

  it('renderiza TileLayer, Marker e Circle', () => {
    render(<DeliveryMap delivery={makeDelivery({ lat: -23.55, lng: -46.63 })} />);
    expect(screen.getByTestId('tile-layer')).toBeInTheDocument();
    expect(screen.getByTestId('marker')).toBeInTheDocument();
    expect(screen.getByTestId('circle')).toBeInTheDocument();
  });
});
