import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';

import { ShortenedUrl, UrlShortenerService } from '../services/url-shortener.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatTooltipModule,
    RouterLink
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  displayedColumns: string[] = ['shortCode', 'originalUrl', 'createdAt', 'actions'];
  isLoading = false;
  urlHistory: ShortenedUrl[] = [];

  constructor(
    private snackBar: MatSnackBar,
    private urlShortenerService: UrlShortenerService
  ) {
    this.urlHistory = this.urlShortenerService.getRecentLinks();
  }

  copyToClipboard(shortCode: string): void {
    const shortUrl = this.urlShortenerService.buildShortUrl(shortCode);
    navigator.clipboard.writeText(shortUrl).then(() => {
      this.snackBar.open('URL copied to clipboard!', 'Close', {
        duration: 2000
      });
    });
  }

  openUrl(shortCode: string): void {
    window.open(this.urlShortenerService.buildShortUrl(shortCode), '_blank');
  }

  deleteUrl(shortCode: string): void {
    this.urlShortenerService.removeRecentLink(shortCode);
    this.urlHistory = this.urlHistory.filter(url => url.shortCode !== shortCode);
    this.snackBar.open('Removed from recent links', 'Close', {
      duration: 3000
    });
  }

  getTotalUrls(): number {
    return this.urlHistory.length;
  }

  getLatestCreatedAt(): string | null {
    return this.urlHistory[0]?.createdAt ?? null;
  }
}
