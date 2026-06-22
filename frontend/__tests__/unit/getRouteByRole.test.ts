import { getRouteByRole } from '../../src/lib/routes';
import type { UserRole } from '../../src/domain/entities/User';

describe('getRouteByRole (Autenticação e Roteamento)', () => {
  it('deve retornar a rota /dashboard se a role for lojista', () => {
    const route = getRouteByRole('lojista');
    expect(route).toBe('/dashboard');
  });

  it('deve retornar a rota /drive se a role for motorista', () => {
    const route = getRouteByRole('motorista');
    expect(route).toBe('/drive');
  });

  it('deve retornar a rota / para roles desconhecidas ou vazias', () => {
    expect(getRouteByRole('unknown' as UserRole)).toBe('/');
    expect(getRouteByRole('' as UserRole)).toBe('/');
  });
});
