import { getRouteByRole } from '../../src/use_cases/getRouteByRole';

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
    expect(getRouteByRole('unknown')).toBe('/');
    expect(getRouteByRole('')).toBe('/');
  });
});
