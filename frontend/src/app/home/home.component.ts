import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';

import { UrlShortenerService } from '../services/url-shortener.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatTooltipModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  urlForm: FormGroup;
  isLoading = false;
  shortenedUrl = '';
  originalUrl = '';

  constructor(
    private fb: FormBuilder,
    private urlShortenerService: UrlShortenerService,
    private snackBar: MatSnackBar
  ) {
    this.urlForm = this.fb.group({
      url: ['', [Validators.required, Validators.pattern(/^https?:\/\/.+/)]]
    });
  }

  onSubmit(): void {
    if (this.urlForm.invalid) {
      return;
    }

    this.isLoading = true;
    this.originalUrl = this.urlForm.get('url')?.value;
    
    this.urlShortenerService.shortenUrl(this.originalUrl).subscribe({
      next: (response) => {
        this.shortenedUrl = response.shortUrl;
        this.isLoading = false;
        this.snackBar.open('URL shortened successfully!', 'Close', {
          duration: 3000
        });
      },
      error: (error) => {
        this.isLoading = false;
        this.snackBar.open('Failed to shorten URL. Please try again.', 'Close', {
          duration: 3000
        });
        console.error('Error shortening URL:', error);
      }
    });
  }

  copyToClipboard(): void {
    navigator.clipboard.writeText(this.shortenedUrl).then(() => {
      this.snackBar.open('URL copied to clipboard!', 'Close', {
        duration: 2000
      });
    });
  }

  resetForm(): void {
    this.urlForm.reset();
    this.shortenedUrl = '';
    this.originalUrl = '';
  }
}
