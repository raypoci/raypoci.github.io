/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#22A39F',
          light: '#3DB8B3',
          dark: '#1c8784',
        },
        secondary: {
          DEFAULT: '#fdd007',
          light: '#ffe047',
          dark: '#e6b800',
        },
      },
      fontFamily: {
        sans: ['Open Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
