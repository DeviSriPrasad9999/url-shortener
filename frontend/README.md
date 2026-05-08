# URL Shortener Frontend

A modern, responsive Angular 20 frontend for the URL shortener microservice application. Built with Angular Material for a beautiful and accessible user interface.

## Features

- **Modern UI/UX**: Built with Angular Material components for a professional look
- **Responsive Design**: Fully responsive design that works on all devices
- **URL Shortening**: Simple and intuitive URL shortening interface
- **Dashboard**: Analytics dashboard with URL history and statistics
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Form Validation**: Robust form validation with real-time feedback
- **Copy to Clipboard**: One-click URL copying functionality
- **Mobile Optimized**: Touch-friendly interface for mobile devices

## Technology Stack

- **Angular 20**: Latest version of Angular with standalone components
- **Angular Material**: UI component library for modern design
- **TypeScript**: Type-safe JavaScript superset
- **SCSS**: Enhanced CSS with variables and mixins
- **RxJS**: Reactive programming for async operations
- **Nginx**: Production-ready web server

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── home/                 # URL shortener component
│   │   │   └── dashboard/            # Analytics dashboard
│   │   ├── services/
│   │   │   └── url-shortener.service.ts # API integration service
│   │   ├── app.component.ts          # Root component
│   │   ├── app.config.ts             # Angular configuration
│   │   └── app.routes.ts             # Routing configuration
│   ├── styles.scss                   # Global styles
│   └── index.html                    # Main HTML file
├── Dockerfile                        # Docker configuration
├── nginx.conf                        # Nginx configuration
├── package.json                      # Dependencies and scripts
└── angular.json                      # Angular CLI configuration
```

## Getting Started

### Prerequisites

- Node.js 20 or higher
- Angular CLI 20 or higher

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run start
```

3. Open your browser and navigate to `http://localhost:4200`

### Available Scripts

- `npm run start` - Start development server
- `npm run build` - Build for production
- `npm run watch` - Build and watch for changes
- `npm run test` - Run unit tests

## API Integration

The frontend integrates with the following backend endpoints:

- **POST /shorten/** - Create shortened URL
- **GET /{code}** - Redirect to original URL

### API Configuration

The API base URL is configured in `src/app/services/url-shortener.service.ts`. Update the `apiUrl` property to match your backend deployment:

```typescript
private readonly apiUrl = 'http://localhost:9000/shorten';
```

## Docker Deployment

Build and run the Docker container:

```bash
# Build the image
docker build -t url-shortener-frontend .

# Run the container
docker run -p 80:80 url-shortener-frontend
```

## Features in Detail

### URL Shortener (Home Component)

- Form validation with real-time feedback
- Loading states during API calls
- Success/error notifications
- Copy to clipboard functionality
- Responsive design for all screen sizes

### Dashboard Component

- Statistics overview (total URLs, clicks, averages)
- URL history table with pagination
- Action buttons (copy, open, delete)
- No-data state with call-to-action
- Mobile-optimized table view

### Error Handling

- HTTP error interceptors
- User-friendly error messages
- Network error handling
- Form validation errors

## Styling

The application uses Angular Material's pre-built themes with custom SCSS for:

- Responsive breakpoints
- Custom animations
- Color schemes
- Component-specific styling

## Future Enhancements

- User authentication
- URL analytics and click tracking
- Custom short codes
- QR code generation
- Bulk URL shortening
- URL expiration management
- Custom domains
- Advanced analytics dashboard

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the URL Shortener microservice application.
