/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bayyinah: {
          navy: '#12183F',
          'navy-light': '#1D255B',
          'navy-dark': '#0B0F2A',
          purple: '#6150EA',
          'purple-hover': '#4E3ED6',
          'purple-light': '#EEECFD',
          turquoise: '#2EF2C2',
          'turquoise-dark': '#13B890',
          'turquoise-light': '#E9FCF7',
          'off-white': '#F2F4FF',
          gray: {
            50: '#F8F9FE',
            100: '#F2F4FF',
            200: '#E2E6FA',
            300: '#C7CEF2',
            400: '#949FD4',
            500: '#6470AA',
            600: '#434D7E',
            700: '#2C345C',
            800: '#1A2040',
            900: '#12183F',
          }
        }
      },
      fontFamily: {
        sans: ['"Readex Pro"', 'sans-serif'],
      },
      boxShadow: {
        'subtle': '0 4px 20px -2px rgba(18, 24, 63, 0.05)',
        'elevated': '0 10px 30px -4px rgba(18, 24, 63, 0.08)',
        'glow-turquoise': '0 0 25px rgba(46, 242, 194, 0.25)',
        'glow-purple': '0 0 25px rgba(97, 80, 234, 0.25)',
      }
    },
  },
  plugins: [],
}
