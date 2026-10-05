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
          'deep-emerald': '#063F36',
          emerald: '#087F68',
          'soft-emerald': '#35B99A',
          gold: '#C9A24A',
          'light-gold': '#E7C978',
          ivory: '#F8F7F2',
          white: '#FFFFFF',
          'dark-text': '#10201D',
          'secondary-text': '#53615D'
        }
      },
      fontFamily: {
        sans: ['"Readex Pro"', 'sans-serif'],
      },
      boxShadow: {
        'subtle': '0 4px 20px -2px rgba(6, 63, 54, 0.05)',
        'elevated': '0 10px 30px -4px rgba(6, 63, 54, 0.08)',
        'glow-emerald': '0 0 25px rgba(53, 185, 154, 0.25)',
        'glow-gold': '0 0 25px rgba(201, 162, 74, 0.25)',
      }
    },
  },
  plugins: [],
}
