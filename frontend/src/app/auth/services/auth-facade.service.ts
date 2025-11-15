import { HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Router } from '@angular/router';
import {
  FormBuilder,
  Validators,
  NonNullableFormBuilder,
} from '@angular/forms';
import { BehaviorSubject, Observable, finalize, take } from 'rxjs';

import {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
} from '../models/auth.models';
import { AUTH_API, AuthApi } from '../tokens/auth-api.token';
import { confirmPasswordValidator } from '../validators/confirm-password.validator';
import { AuthSessionService } from './auth-session.service';

type LoginForm = ReturnType<AuthFacadeService['createLoginForm']>;
type RegisterForm = ReturnType<AuthFacadeService['createRegisterForm']>;

@Injectable({
  providedIn: 'root',
})
export class AuthFacadeService {
  private readonly fb: NonNullableFormBuilder = inject(FormBuilder).nonNullable;
  private readonly api = inject<AuthApi>(AUTH_API);
  private readonly router = inject(Router);
  private readonly session = inject(AuthSessionService);

  private readonly loadingSubject = new BehaviorSubject(false);
  private readonly errorSubject = new BehaviorSubject<string | null>(null);

  readonly loading$ = this.loadingSubject.asObservable();
  readonly error$ = this.errorSubject.asObservable();

  readonly loginForm: LoginForm = this.createLoginForm();
  readonly registerForm: RegisterForm = this.createRegisterForm();

  login(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.executeRequest(this.api.login(this.loginForm.getRawValue()));
  }

  register(): void {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    const { confirmPassword, ...payload } = this.registerForm.getRawValue();
    this.executeRequest(this.api.register(payload));
  }

  resetErrors(): void {
    this.errorSubject.next(null);
  }

  private createLoginForm() {
    return this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  private createRegisterForm() {
    return this.fb.group(
      {
        fullName: ['', [Validators.required, Validators.minLength(2)]],
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        confirmPassword: ['', [Validators.required]],
      },
      { validators: confirmPasswordValidator() },
    );
  }

  private executeRequest(stream: Observable<AuthResponse>): void {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    stream
      .pipe(
        take(1),
        finalize(() => this.loadingSubject.next(false)),
      )
      .subscribe({
        next: (response) => this.handleAuthSuccess(response),
        error: (err) => this.errorSubject.next(this.extractErrorMessage(err)),
      });
  }

  private handleAuthSuccess(response: AuthResponse): void {
    this.session.persistUserId(response.id);
    this.router.navigateByUrl('/');
  }

  private extractErrorMessage(error: unknown): string {
    if (error instanceof HttpErrorResponse) {
      const message =
        (error.error && (error.error.message ?? error.error.detail)) ??
        error.message;
      return message ?? 'Сервис временно недоступен.';
    }

    return 'Не удалось выполнить запрос. Попробуйте позже.';
  }
}
