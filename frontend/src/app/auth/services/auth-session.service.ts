import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class AuthSessionService {
  private readonly storageKey = 'pixerase.auth.userId';
  private readonly platformId = inject(PLATFORM_ID);

  private get isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  persistUserId(id: string): void {
    if (!this.isBrowser) {
      return;
    }

    localStorage.setItem(this.storageKey, id);
  }

  getUserId(): string | null {
    if (!this.isBrowser) {
      return null;
    }

    return localStorage.getItem(this.storageKey);
  }

  clear(): void {
    if (!this.isBrowser) {
      return;
    }

    localStorage.removeItem(this.storageKey);
  }
}

