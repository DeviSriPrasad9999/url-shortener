import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';

import { ShortenedUrl, UrlShortenerService } from '../services/url-shortener.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [DatePipe, RouterLink]
})
export class DashboardComponent {
  private readonly urlShortenerService = inject(UrlShortenerService);

  readonly urlHistory = signal<ShortenedUrl[]>(this.urlShortenerService.getRecentLinks());
  readonly totalUrls = computed(() => this.urlHistory().length);
  readonly latestCreatedAt = computed(() => this.urlHistory()[0]?.createdAt ?? null);
  readonly copySuccess = signal<string | null>(null);

  copyToClipboard(shortCode: string): void {
    const shortUrl = this.urlShortenerService.buildShortUrl(shortCode);
    navigator.clipboard.writeText(shortUrl).then(() => {
      this.copySuccess.set(shortCode);
      setTimeout(() => this.copySuccess.set(null), 2000);
    });
  }

  openUrl(shortCode: string): void {
    window.open(this.urlShortenerService.buildShortUrl(shortCode), '_blank', 'noopener,noreferrer');
  }

  deleteUrl(shortCode: string): void {
    this.urlShortenerService.removeRecentLink(shortCode);
    this.urlHistory.update(links => links.filter(url => url.shortCode !== shortCode));
  }
}

