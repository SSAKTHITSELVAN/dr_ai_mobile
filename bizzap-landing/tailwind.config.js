// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [
//     "./src/**/*.{js,jsx,ts,tsx}",
//   ],
//   theme: {
//     extend: {
//       fontFamily: {
//         'lato': ['Lato', 'sans-serif'],
//         'nunito': ['Nunito', 'sans-serif'],
//       },
//       colors: {
//         'brand-blue': '#00417E',
//         'brand-blue-dark': '#054E94',
//         'brand-yellow': '#FFC104',
//       }
//     },
//   },
//   plugins: [],
// }


/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        lato: ["Lato", "sans-serif"],
        nunito: ["Nunito", "sans-serif"],
      },
      colors: {
        "brand-blue": "#00417E",
        "brand-blue-dark": "#054E94",
        "brand-yellow": "#FFC104",
        "brand-off-white": "#E0E0E0", // New color for body text
      },
    },
  },
  plugins: [],
};