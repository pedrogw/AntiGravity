import type { UserRole } from '@/domain/entities/User';

const ROUTE_BY_ROLE: Record<UserRole, string> = {
  lojista: '/dashboard',
  motorista: '/drive',
};

export function getRouteByRole(role: UserRole): string {
  return ROUTE_BY_ROLE[role] ?? '/';
}
