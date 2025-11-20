/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html', // Incluye todos los HTML en tu proyecto
        './**/*.html',           // Incluye archivos HTML en subdirectorios
        './static/**/*.js',  
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  }
  