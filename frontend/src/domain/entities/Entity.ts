export abstract class Entity<T> {
  public readonly id: string;
  protected props: T;

  constructor(props: T, id?: string) {
    this.id = id ? id : crypto.randomUUID();
    this.props = props;
  }
}
