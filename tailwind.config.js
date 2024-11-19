/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './coolclub/templates/**/*.html',
    './chat/templates/**/*.html',
    './aunties-cool-club/static/js/**/*.js',
  ],
  safelist: [
  ],
  theme: {
    extend: {},
  },
  plugins: [
    // Add any Tailwind plugins if needed
  ],
  darkMode: ['class', '[data-theme="dark"]'], // Using custom attribute selector for dark mode
}
