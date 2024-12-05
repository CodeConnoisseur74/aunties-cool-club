/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './coolclub/templates/**/*.html',
    './chat/templates/**/*.html',
    './aunties-cool-club/static/js/**/*.js',
  ],
  safelist: [
  ],
  daisyui: {
    themes: ["synthwave"],
  },
  plugins: [
    require('daisyui'),
  ],
}
