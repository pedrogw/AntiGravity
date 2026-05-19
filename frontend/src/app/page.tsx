'use client';

import { useAuth } from '../hooks/useAuth';
import { LoginForm } from '../components/LoginForm';

export default function Home() {
  const { login, isLoading, error } = useAuth();

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <LoginForm 
        onSubmit={login} 
        isLoading={isLoading} 
        error={error} 
      />
    </main>
  );
}
