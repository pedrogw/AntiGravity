import { Entity } from './Entity';

export type UserRole = 'lojista' | 'motorista';

export interface UserProps {
  email: string;
  role: UserRole;
  createdAt?: Date;
}

export class User extends Entity<UserProps> {
  constructor(props: UserProps, id?: string) {
    super(props, id);
  }

  get email(): string {
    return this.props.email;
  }

  get role(): UserRole {
    return this.props.role;
  }

  get createdAt(): Date | undefined {
    return this.props.createdAt;
  }

  public isMotorista(): boolean {
    return this.props.role === 'motorista';
  }

  public isLojista(): boolean {
    return this.props.role === 'lojista';
  }
}
