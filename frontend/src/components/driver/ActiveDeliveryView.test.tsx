import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ActiveDeliveryView } from './ActiveDeliveryView';
import { Delivery } from '@/domain/entities/Delivery';

function makeDelivery(overrides: Partial<{ status: string; id: string }> = {}): Delivery {
  return new Delivery(
    {
      factoryId: '00000000-0000-0000-0000-000000000001',
      storeId: '00000000-0000-0000-0000-000000000002',
      driverId: '00000000-0000-0000-0000-000000000003',
      status: overrides.status || 'pendente',
    },
    overrides.id || 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  );
}

describe('ActiveDeliveryView', () => {
  it('renderiza SafeCheckToggle', () => {
    render(<ActiveDeliveryView delivery={makeDelivery()} />);
    expect(screen.getByText(/Safe-Check/i)).toBeInTheDocument();
  });

  it('mostra "Concluir Entrega" quando status é em_transito e onComplete existe', () => {
    render(
      <ActiveDeliveryView
        delivery={makeDelivery({ status: 'em_transito' })}
        onComplete={vi.fn()}
      />,
    );
    expect(screen.getByText('Concluir Entrega')).toBeInTheDocument();
  });

  it('chama onComplete ao clicar em "Concluir Entrega"', () => {
    const onComplete = vi.fn();
    render(
      <ActiveDeliveryView
        delivery={makeDelivery({ status: 'em_transito' })}
        onComplete={onComplete}
      />,
    );
    fireEvent.click(screen.getByText('Concluir Entrega'));
    expect(onComplete).toHaveBeenCalledTimes(1);
  });

  it('não mostra "Concluir Entrega" quando status não é em_transito', () => {
    render(
      <ActiveDeliveryView
        delivery={makeDelivery({ status: 'aceita' })}
        onComplete={vi.fn()}
      />,
    );
    expect(screen.queryByText('Concluir Entrega')).not.toBeInTheDocument();
  });

  it('não mostra "Concluir Entrega" quando onComplete não é fornecido', () => {
    render(
      <ActiveDeliveryView delivery={makeDelivery({ status: 'em_transito' })} />,
    );
    expect(screen.queryByText('Concluir Entrega')).not.toBeInTheDocument();
  });

  it('renderiza sem erro quando storeLocation é fornecido', () => {
    const storeLocation = { lat: -23.56, lng: -46.64 };
    render(
      <ActiveDeliveryView
        delivery={makeDelivery({ status: 'em_transito' })}
        onComplete={vi.fn()}
        storeLocation={storeLocation}
      />,
    );
    expect(screen.getByText(/Safe-Check/i)).toBeInTheDocument();
  });
});
