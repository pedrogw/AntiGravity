import { rest } from 'msw';

export const handlers = [
  // Mock login endpoint
  rest.post('*/auth/login', (req, res, ctx) => {
    const { email, password } = req.body as any;
    
    // Simulate lojista
    if (email === 'lojista@test.com' && password === '1234') {
      return res(
        ctx.status(200),
        ctx.json({
          token: 'fake_lojista_token',
          user: { id: 'user-lojista', email, role: 'lojista', created_at: new Date().toISOString() }
        })
      );
    }

    // Simulate motorista
    if (email === 'motorista@test.com' && password === '1234') {
      return res(
        ctx.status(200),
        ctx.json({
          token: 'fake_motorista_token',
          user: { id: 'user-motorista', email, role: 'motorista', created_at: new Date().toISOString() }
        })
      );
    }

    // Invalid credentials
    return res(
      ctx.status(401),
      ctx.json({ detail: 'Invalid credentials' })
    );
  }),
];
