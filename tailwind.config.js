/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './coolclub/templates/**/*.html',
    './chat/templates/**/*.html',
    './static/js/**/*.js',
  ],
  safelist: [
    // Add any classes you want to safelist here
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
  darkMode: ['class', '[data-theme="dark"]'],
};
