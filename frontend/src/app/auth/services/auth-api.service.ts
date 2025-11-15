import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
} from '../models/auth.models';
import { AUTH_API_BASE_URL, AuthApi } from '../tokens/auth-api.token';

@Injectable({
  providedIn: 'root',
})
export class AuthApiService implements AuthApi {
  constructor(
    private readonly http: HttpClient,
    @Inject(AUTH_API_BASE_URL) private readonly baseUrl: string,
  ) {}

  login(payload: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/login`, payload);
  }

  register(payload: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.baseUrl}/register`, payload);
  }
}
