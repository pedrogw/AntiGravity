'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { isTokenExpired } from '../utils/jwt';

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [isAuthorized] = useState(() => {
    if (typeof window === 'undefined') return false;
    const token = localStorage.getItem('token');
    return !!token && !isTokenExpired(token);
  });

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (!token || isTokenExpired(token)) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
      }
      router.push('/');
    }
  }, [router]);

  if (!isAuthorized) {
    return <div>Carregando...</div>;
  }

  return <>{children}</>;
}
