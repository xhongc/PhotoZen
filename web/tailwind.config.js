/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    base: false,
    themes: [
        'cupcake',
        'bumblebee',
        'emerald',
        'corporate',
        'synthwave',
        'retro',
        'cyberpunk',
        'valentine',
        'halloween',
        'garden',
        'forest',
        'aqua',
        'lofi',
        'pastel',
        'fantasy',
        'wireframe',
        'black',
        'luxury',
        'dracula',
        'cmyk',
        'autumn',
        'business',
        'acid',
        'lemonade',
        'night',
        'coffee',
        'winter',
        'dim',
        'nord',
        'sunset',
        {
          'light': {
              ...require("daisyui/src/theming/themes")["light"],
              "base-200": "#f8fafc",
          },
      },
        {
            'dark': {
                ...require("daisyui/src/theming/themes")["dark"],
                "base-100": "#22252B",
                "base-200": "#000",
            },
        },
        {
            'charles': {
                ...require("daisyui/src/theming/themes")["forest"],
                "base-100": "#22252B",
                "base-200": "#000",
                "neutral": "#31513f",
                "neutral-content": "#2FD973",
                "--rounded-btn": "1.9rem",
            },
        },
    ],
},
}
