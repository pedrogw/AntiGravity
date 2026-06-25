import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

const mockPush = vi.fn();

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
  usePathname: () => '/dashboard',
}));

vi.mock('../../infrastructure/di/factories', () => ({
  makeLogoutUseCase: vi.fn(() => ({ execute: vi.fn() })),
}));

import { Sidebar } from './Sidebar';

describe('Sidebar badge', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('deve exibir badge quando criticalAlertsCount > 0', () => {
    render(<Sidebar criticalAlertsCount={3} />);
    expect(screen.getByText('3')).toBeTruthy();
  });

  it('deve exibir 99+ quando criticalAlertsCount > 99', () => {
    render(<Sidebar criticalAlertsCount={150} />);
    expect(screen.getByText('99+')).toBeTruthy();
  });

  it('não deve exibir badge quando criticalAlertsCount é 0', () => {
    render(<Sidebar criticalAlertsCount={0} />);
    expect(screen.queryByText('3')).toBeNull();
  });

  it('não deve exibir badge quando prop não fornecida', () => {
    render(<Sidebar />);
    expect(screen.queryByText('3')).toBeNull();
  });
});
