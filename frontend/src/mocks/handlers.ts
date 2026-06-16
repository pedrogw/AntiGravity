import { rest } from 'msw';

let fakeRefreshToken = 'fake_refresh_token_default';

export const handlers = [
  rest.post('*/auth/login', (req, res, ctx) => {
    const { email, password } = req.body as any;

    if (email === 'lojista@test.com' && password === '1234') {
      const token = 'fake_lojista_token';
      fakeRefreshToken = `refresh_${token}`;
      return res(
        ctx.status(200),
        ctx.json({
          token,
          refresh_token: fakeRefreshToken,
          user: { id: 'user-lojista', email, role: 'lojista', created_at: new Date().toISOString() }
        })
      );
    }

    if (email === 'motorista@test.com' && password === '1234') {
      const token = 'fake_motorista_token';
      fakeRefreshToken = `refresh_${token}`;
      return res(
        ctx.status(200),
        ctx.json({
          token,
          refresh_token: fakeRefreshToken,
          user: { id: 'user-motorista', email, role: 'motorista', created_at: new Date().toISOString() }
        })
      );
    }

    return res(
      ctx.status(401),
      ctx.json({ detail: 'Invalid credentials' })
    );
  }),

  rest.post('*/auth/refresh', (req, res, ctx) => {
    const { refresh_token } = req.body as any;

    if (refresh_token === fakeRefreshToken) {
      const newToken = `new_access_${Date.now()}`;
      fakeRefreshToken = `new_refresh_${Date.now()}`;
      return res(
        ctx.status(200),
        ctx.json({
          access_token: newToken,
          refresh_token: fakeRefreshToken,
          token_type: 'bearer'
        })
      );
    }

    return res(
      ctx.status(401),
      ctx.json({ detail: 'Refresh token inválido ou expirado' })
    );
  }),
];
