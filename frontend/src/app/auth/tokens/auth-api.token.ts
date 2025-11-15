import { InjectionToken, inject } from '@angular/core';

import {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
} from '../models/auth.models';
import { AuthApiService } from '../services/auth-api.service';

export interface AuthApi {
  login(payload: LoginRequest): import('rxjs').Observable<AuthResponse>;
  register(payload: RegisterRequest): import('rxjs').Observable<AuthResponse>;
}

export const AUTH_API = new InjectionToken<AuthApi>('AUTH_API', {
  providedIn: 'root',
  factory: () => inject(AuthApiService),
});

export const AUTH_API_BASE_URL = new InjectionToken<string>(
  'AUTH_API_BASE_URL',
  {
    providedIn: 'root',
    factory: () => '/api/auth',
  },
);

