import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { Factory, Store } from '../../domain/entities/Place';
import { Coordinates } from '../../domain/value_objects/Coordinates';
import { ApiError } from '../../domain/errors/ApiError';
import { NetworkError } from '../../domain/errors/NetworkError';
import { apiClient } from '../api/api_client';
import { AxiosError } from 'axios';

interface FactoryResponse {
  id: string;
  name: string;
  lat: number;
  lng: number;
}

interface StoreResponse {
  id: string;
  name: string;
  lat: number;
  lng: number;
  owner_id: string;
}

export class ApiPlaceRepository implements PlaceRepositoryProtocol {
  async createFactory(name: string, location: Coordinates): Promise<Factory> {
    try {
      const { data } = await apiClient.post<FactoryResponse>('/places/factories', {
        name,
        lat: location.lat,
        lng: location.lng,
      });
      return new Factory(
        { name: data.name, location: new Coordinates({ lat: data.lat, lng: data.lng }) },
        data.id,
      );
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response) {
          throw new ApiError(error.response.status, error.message);
        }
        throw new NetworkError();
      }
      throw error;
    }
  }

  async createStore(name: string, location: Coordinates, ownerId: string): Promise<Store> {
    try {
      const { data } = await apiClient.post<StoreResponse>('/places/stores', {
        name,
        lat: location.lat,
        lng: location.lng,
        owner_id: ownerId,
      });
      return new Store(
        {
          name: data.name,
          location: new Coordinates({ lat: data.lat, lng: data.lng }),
          ownerId: data.owner_id,
        },
        data.id,
      );
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response) {
          throw new ApiError(error.response.status, error.message);
        }
        throw new NetworkError();
      }
      throw error;
    }
  }
}
