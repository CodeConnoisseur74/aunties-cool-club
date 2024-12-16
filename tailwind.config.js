/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './chat/templates/**/*.html',
    './coolclub/static/js/**/*.js',
    './coolclub/templates/**/*.html',
  ],
  flyonui: {
    themes: [
      {
        synthwave: {
          "primary": "#e779c1",
          "primary-content": "#13050e",
          "secondary": "#58c7f3",
          "secondary-content": "#030e14",
          "accent": "#ffd200",
          "accent-content": "#161000",
          "neutral": "#221551",
          "neutral-content": "#cdccdb",
          "base-100": "#1a103d",
          "base-200": "#150c34",
          "base-300": "#10092b",
          "base-content": "#cbcad6",
          "info": "#53c0f3",
          "info-content": "#020e14",
          "success": "#71ead2",
          "success-content": "#041310",
          "warning": "#eace6c",
          "warning-content": "#130f04",
          "error": "#ec8c78",
          "error-content": "#130705"
        }
      }
    ]
  },
  plugins: [
    require('flyonui'),
  ],
};
