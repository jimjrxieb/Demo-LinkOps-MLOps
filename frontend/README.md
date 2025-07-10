# LinkOps Frontend - MLOps Command Center

A modern, sci-fi themed Vue.js frontend for the LinkOps MLOps platform, featuring a holographic UI design with real-time monitoring, pipeline management, and security auditing capabilities.

## 🚀 Features

- **Sci-Fi Holographic UI**: Neon/glow effects with futuristic design
- **Real-time Dashboard**: Monitor orbs, runes, and system status
- **Whis Pipeline**: Visual MLOps data processing workflow
- **Security Audit**: Comprehensive repository analysis
- **Responsive Design**: Works on desktop and mobile devices
- **State Management**: Pinia store for global state
- **Modern Vue 3**: Composition API and latest features

## 📁 Project Structure

```
frontend/
├── App.vue                 # Main app component with navigation
├── main.js                 # Vue app entry point
├── index.html              # HTML template
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── postcss.config.js       # PostCSS configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── router/
│   └── index.js           # Vue Router configuration
├── views/
│   ├── Dashboard.vue      # Main dashboard view
│   ├── Whis.vue          # Whis pipeline view
│   ├── Audit.vue         # Security audit view
│   └── NotFound.vue      # 404 error page
├── components/
│   ├── OrbCard.vue       # Individual orb display
│   ├── RuneCard.vue      # Available runes display
│   ├── FicknurySearch.vue # Search functionality
│   ├── WhisPipeline.vue  # Pipeline visualization
│   ├── AuditInput.vue    # Repository input form
│   └── AuditResults.vue  # Audit results display
├── assets/
│   └── holo-theme.css    # Holographic theme styles
└── store/
    └── index.js          # Pinia store for state management
```

## 🛠️ Setup & Installation

### Prerequisites

- Node.js 18+
- npm 8+

### Installation

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Start development server:**

   ```bash
   npm run dev
   ```

3. **Build for production:**

   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## 🎨 Design System

### Color Palette

- **Primary**: `#00d4ff` (Cyan)
- **Secondary**: `#ff00ff` (Magenta)
- **Accent**: `#00ff88` (Green)
- **Background**: Dark gradients from `#0a0a0a` to `#16213e`
- **Text**: `#e0e0e0` (Light gray)

### Typography

- **Font Family**: Orbitron (primary), Courier New (fallback)
- **Weights**: 400 (regular), 700 (bold), 900 (black)

### Components

#### Cards

- Holographic borders with glow effects
- Hover animations with transform and shadow
- Backdrop blur for depth

#### Buttons

- Gradient backgrounds
- Hover effects with transform
- Icon + text combinations

#### Status Indicators

- Color-coded severity levels
- Animated pulse effects
- Glow shadows

## 🔧 Configuration

### Vite Configuration

The `vite.config.js` includes:

- Vue plugin
- Path aliases (`@` and `~`)
- Development server with proxy
- Build optimization
- PostCSS integration

### Tailwind CSS

Tailwind CSS v4 is configured with:

- Custom color palette
- Responsive breakpoints
- Custom utilities for holographic effects

### PostCSS

PostCSS is configured with:

- Tailwind CSS plugin
- Autoprefixer
- Custom plugins for advanced CSS features

## 📱 Responsive Design

The application is fully responsive with:

- Mobile-first approach
- Flexible grid layouts
- Adaptive navigation
- Touch-friendly interactions

### Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔄 State Management

### Pinia Store

The main store (`store/index.js`) manages:

- **System Status**: Online/offline, active jobs, errors
- **Orbs**: Active tasks and their status
- **Runes**: Available tools and their costs
- **Whis Pipeline**: Processing state and results
- **Audit Results**: Security scan findings
- **Search**: Query and filter state
- **UI State**: Sidebar, theme, notifications

### Store Actions

- `addOrb()` / `updateOrb()` / `removeOrb()`
- `activateRune()`
- `startWhisPipeline()`
- `runAudit()`
- `performSearch()`
- `addNotification()`

## 🎯 Key Components

### Dashboard View

- System status overview
- Active orbs grid
- Available runes
- Quick actions
- Search functionality

### Whis Pipeline View

- Visual pipeline steps
- Real-time processing
- Configuration options
- Results display

### Audit View

- Repository input
- Security scanning
- Results analysis
- Export functionality

## 🚀 Performance

### Optimizations

- **Code Splitting**: Route-based lazy loading
- **Tree Shaking**: Unused code elimination
- **Asset Optimization**: Image and CSS minification
- **Caching**: Browser and service worker caching

### Bundle Analysis

- Vendor chunks for Vue and utilities
- Component-level code splitting
- Optimized imports

## 🔒 Security

### Best Practices

- Input sanitization
- XSS prevention
- CSRF protection
- Secure headers

### Audit Features

- Dependency vulnerability scanning
- Code quality analysis
- Secret detection
- Security score calculation

## 🧪 Testing

### Available Scripts

```bash
npm run test          # Run unit tests
npm run test:ui       # Run tests with UI
npm run test:coverage # Run tests with coverage
```

### Testing Strategy

- Unit tests for components
- Integration tests for store
- E2E tests for critical flows
- Visual regression testing

## 📦 Deployment

### Build Process

1. **Development**: `npm run dev`
2. **Staging**: `npm run build:staging`
3. **Production**: `npm run build`

### Docker Support

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

### Code Style

- ESLint configuration
- Prettier formatting
- Vue 3 Composition API
- TypeScript support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

---

**Built with ❤️ for the LinkOps MLOps Platform**
