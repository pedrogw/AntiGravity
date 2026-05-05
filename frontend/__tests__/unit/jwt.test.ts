import { isTokenExpired } from '../../src/utils/jwt';

describe('JWT Util', () => {
  it('deve retornar true para tokens nulos ou vazios', () => {
    expect(isTokenExpired(null)).toBe(true);
    expect(isTokenExpired('')).toBe(true);
  });

  it('deve retornar true para tokens malformados', () => {
    expect(isTokenExpired('invalid.token')).toBe(true);
    expect(isTokenExpired('not_a_token')).toBe(true);
  });

  it('deve retornar false para token válido e não expirado', () => {
    const futureTime = Math.floor(Date.now() / 1000) + 3600; // 1h no futuro
    const payload = Buffer.from(JSON.stringify({ exp: futureTime })).toString('base64');
    const fakeToken = `header.${payload}.signature`;

    expect(isTokenExpired(fakeToken)).toBe(false);
  });

  it('deve retornar true para token com data no passado', () => {
    const pastTime = Math.floor(Date.now() / 1000) - 3600; // 1h no passado
    const payload = Buffer.from(JSON.stringify({ exp: pastTime })).toString('base64');
    const fakeToken = `header.${payload}.signature`;

    expect(isTokenExpired(fakeToken)).toBe(true);
  });
});
