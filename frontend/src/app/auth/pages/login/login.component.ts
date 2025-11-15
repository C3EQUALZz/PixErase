import { ChangeDetectionStrategy, Component } from '@angular/core';

import { AuthFacadeService } from '../../services/auth-facade.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginComponent {
  constructor(public readonly facade: AuthFacadeService) {}

  submit(): void {
    this.facade.login();
  }
}
