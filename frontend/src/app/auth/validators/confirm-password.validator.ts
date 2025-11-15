import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export const confirmPasswordValidator = (
  passwordKey = 'password',
  confirmPasswordKey = 'confirmPassword',
): ValidatorFn => {
  return (group: AbstractControl): ValidationErrors | null => {
    const password = group.get(passwordKey)?.value;
    const confirmation = group.get(confirmPasswordKey)?.value;

    if (!password || !confirmation) {
      return null;
    }

    return password === confirmation
      ? null
      : { passwordMismatch: true };
  };
};

