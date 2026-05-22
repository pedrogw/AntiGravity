export interface CoordinatesProps {
  lat: number;
  lng: number;
}

export class Coordinates {
  public readonly lat: number;
  public readonly lng: number;

  constructor(props: CoordinatesProps) {
    this.lat = props.lat;
    this.lng = props.lng;
  }
}
