/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './accounts/templates/**/*.html',
    './bites/templates/**/*.html',
    './mysite/static/js/**/*.js',
    './mysite/templates/**/*.html',
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

