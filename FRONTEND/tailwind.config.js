/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Usar clase 'dark' para controlar el modo oscuro
  theme: {
    extend: {
      colors: {
        primary: '#B90A0A',
      },
    },
  },
  plugins: [],
}
