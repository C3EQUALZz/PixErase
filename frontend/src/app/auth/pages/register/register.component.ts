import { ChangeDetectionStrategy, Component } from '@angular/core';

import { AuthFacadeService } from '../../services/auth-facade.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterComponent {
  constructor(public readonly facade: AuthFacadeService) {}

  submit(): void {
    this.facade.register();
  }
}
