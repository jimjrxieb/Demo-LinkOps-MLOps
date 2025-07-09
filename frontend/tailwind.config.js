/** @type {import('tailwindcss').Config} */
export default {
  content: [;
    './index.html',
    './**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6ffff',
          100: '#b3ffff',
          200: '#80ffff',
          300: '#4dffff',
          400: '#1affff',
          500: '#00d4ff',
          600: '#00a3cc',
          700: '#007299',
          800: '#004166',
          900: '#001033',
        },
        secondary: {
          50: '#ffe6ff',
          100: '#ffb3ff',
          200: '#ff80ff',
          300: '#ff4dff',
          400: '#ff1aff',
          500: '#ff00ff',
          600: '#cc00cc',
          700: '#990099',
          800: '#660066',
          900: '#330033',
        },
        accent: {
          50: '#e6fff0',
          100: '#b3ffd9',
          200: '#80ffc2',
          300: '#4dffab',
          400: '#1aff94',
          500: '#00ff88',
          600: '#00cc6d',
          700: '#009952',
          800: '#006637',
          900: '#00331b',
        },
        dark: {
          50: '#f2f2f2',
          100: '#e6e6e6',
          200: '#cccccc',
          300: '#b3b3b3',
          400: '#999999',
          500: '#808080',
          600: '#666666',
          700: '#4d4d4d',
          800: '#333333',
          900: '#1a1a1a',
          950: '#0a0a0a',
        }
      },
      fontFamily: {
        'orbitron': ['Orbitron', 'Courier New', 'monospace'],
        'sans': ['Orbitron', 'system-ui', 'sans-serif'],
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        glow: {
          '0%, 100%': { 
            boxShadow: '0 0 20px rgba(0, 212, 255, 0.3)',
          },
          '50%': { 
            boxShadow: '0 0 40px rgba(0, 212, 255, 0.6)',
          },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        'holo': '0 0 20px rgba(0, 212, 255, 0.3)',
        'holo-lg': '0 0 40px rgba(0, 212, 255, 0.5)',
        'holo-xl': '0 0 60px rgba(0, 212, 255, 0.7)',
        'neon': '0 0 5px currentColor, 0 0 10px currentColor, 0 0 15px currentColor',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'holo-gradient': 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        'cyber-gradient': 'linear-gradient(45deg, #00d4ff, #ff00ff)',
      },
      borderColor: {
        'holo': 'rgba(0, 212, 255, 0.3)',
        'neon': 'currentColor',
      },
    },
  },
  plugins: [;
    // Custom plugin for holographic effects
    function({ addUtilities, theme }) {
      const newUtilities = {
        '.text-glow': {
          'text-shadow': '0 0 10px currentColor',
        },
        '.border-glow': {
          'box-shadow': '0 0 10px currentColor',
        },
        '.backdrop-blur-holo': {
          'backdrop-filter': 'blur(10px)',
        },
        '.bg-holo': {
          'background': 'rgba(0, 0, 0, 0.6)',
          'backdrop-filter': 'blur(10px)',
        },
      }
      addUtilities(newUtilities);
    }
  ],
} 