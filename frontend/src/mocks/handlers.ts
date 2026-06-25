import { http, HttpResponse } from 'msw';

let fakeRefreshToken = 'fake_refresh_token_default';

export const handlers = [
  http.post('*/auth/login', async ({ request }) => {
    const { email, password } = await request.json() as { email: string; password: string };

    if (email === 'lojista@test.com' && password === '1234') {
      const token = 'fake_lojista_token';
      fakeRefreshToken = `refresh_${token}`;
      return HttpResponse.json({
        token,
        refresh_token: fakeRefreshToken,
        user: { id: 'user-lojista', email, role: 'lojista', created_at: new Date().toISOString() }
      }, { status: 200 });
    }

    if (email === 'motorista@test.com' && password === '1234') {
      const token = 'fake_motorista_token';
      fakeRefreshToken = `refresh_${token}`;
      return HttpResponse.json({
        token,
        refresh_token: fakeRefreshToken,
        user: { id: 'user-motorista', email, role: 'motorista', created_at: new Date().toISOString() }
      }, { status: 200 });
    }

    return HttpResponse.json(
      { detail: 'Invalid credentials' },
      { status: 401 }
    );
  }),

  http.post('*/auth/refresh', async ({ request }) => {
    const { refresh_token } = await request.json() as { refresh_token: string };

    if (refresh_token === fakeRefreshToken) {
      const newToken = `new_access_${Date.now()}`;
      fakeRefreshToken = `new_refresh_${Date.now()}`;
      return HttpResponse.json({
        access_token: newToken,
        refresh_token: fakeRefreshToken,
        token_type: 'bearer'
      }, { status: 200 });
    }

    return HttpResponse.json(
      { detail: 'Refresh token inválido ou expirado' },
      { status: 401 }
    );
  }),
];
