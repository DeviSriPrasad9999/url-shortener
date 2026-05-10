import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

import { UrlShortenerService } from '../services/url-shortener.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [ReactiveFormsModule]
})
export class HomeComponent {
  private readonly fb = inject(FormBuilder);
  private readonly urlShortenerService = inject(UrlShortenerService);

  readonly urlForm = this.fb.group({
    url: ['', [Validators.required, Validators.pattern(/^https?:\/\/.+/)]]
  });

  readonly isLoading = signal(false);
  readonly shortenedUrl = signal('');
  readonly originalUrl = signal('');
  readonly copySuccess = signal(false);
  readonly errorMessage = signal('');

  get urlControl() {
    return this.urlForm.get('url');
  }

  onSubmit(): void {
    if (this.urlForm.invalid) {
      this.urlForm.markAllAsTouched();
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set('');
    this.originalUrl.set(this.urlControl!.value!);

    this.urlShortenerService.shortenUrl(this.originalUrl()).subscribe({
      next: (response) => {
        this.shortenedUrl.set(response.shortUrl);
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
        this.errorMessage.set('Failed to shorten URL. Please try again.');
      }
    });
  }

  copyToClipboard(): void {
    navigator.clipboard.writeText(this.shortenedUrl()).then(() => {
      this.copySuccess.set(true);
      setTimeout(() => this.copySuccess.set(false), 2000);
    });
  }

  reset(): void {
    this.urlForm.reset();
    this.shortenedUrl.set('');
    this.originalUrl.set('');
    this.errorMessage.set('');
  }
}

