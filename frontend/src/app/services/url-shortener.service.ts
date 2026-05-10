import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export interface ShortenRequest {
  url: string;
}

export interface ShortenResponse {
  short_code: string;
}

export interface ShortenedUrl {
  shortCode: string;
  shortUrl: string;
  originalUrl: string;
  createdAt: string;
}

@Injectable({
  providedIn: 'root'
})
export class UrlShortenerService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = '/api/shorten/';
  private readonly recentLinksKey = 'url-shortener.recent-links';

  shortenUrl(url: string): Observable<ShortenedUrl> {
    const request: ShortenRequest = { url };

    return this.http.post<ShortenResponse>("http://localhost:9000/shorten/", request).pipe(
      map((response) => {
        const shortenedUrl: ShortenedUrl = {
          shortCode: response.short_code,
          shortUrl: `${this.getRedirectOrigin()}/${response.short_code}`,
          originalUrl: url,
          createdAt: new Date().toISOString()
        };

        this.saveRecentLink(shortenedUrl);
        return shortenedUrl;
      }),
      catchError(this.handleError)
    );
  }

  getRecentLinks(): ShortenedUrl[] {
    const rawLinks = localStorage.getItem(this.recentLinksKey);

    if (!rawLinks) {
      return [];
    }

    try {
      const links = JSON.parse(rawLinks) as ShortenedUrl[];
      return Array.isArray(links) ? links : [];
    } catch {
      return [];
    }
  }

  removeRecentLink(shortCode: string): void {
    const links = this.getRecentLinks().filter((link) => link.shortCode !== shortCode);
    localStorage.setItem(this.recentLinksKey, JSON.stringify(links));
  }

  buildShortUrl(shortCode: string): string {
    return `${this.getRedirectOrigin()}/${shortCode}`;
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client error: ${error.error.message}`;
    } else {
      errorMessage = `Server error: ${error.status} - ${error.message}`;
    }

    console.error('URL Shortener Service Error:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }

  private saveRecentLink(link: ShortenedUrl): void {
    const existingLinks = this.getRecentLinks().filter((item) => item.shortCode !== link.shortCode);
    const nextLinks = [link, ...existingLinks].slice(0, 20);
    localStorage.setItem(this.recentLinksKey, JSON.stringify(nextLinks));
  }

  private getRedirectOrigin(): string {
    const { protocol, hostname, port } = window.location;

    if ((hostname === 'localhost' || hostname === '127.0.0.1') && port === '9000') {
      return `${protocol}//${hostname}:9000`;
    }

    return window.location.origin;
  }
}
