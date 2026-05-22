export class AppError extends Error {
  public readonly name: string;

  constructor(message: string, name: string = 'AppError') {
    super(message);
    this.name = name;
    // Set the prototype explicitly to ensure instanceof works correctly in TypeScript
    Object.setPrototypeOf(this, new.target.prototype);
  }
}
