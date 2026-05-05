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
          access_token: 'fake_lojista_token',
          role: 'lojista'
        })
      );
    }

    // Simulate motorista
    if (email === 'motorista@test.com' && password === '1234') {
      return res(
        ctx.status(200),
        ctx.json({
          access_token: 'fake_motorista_token',
          role: 'motorista'
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
