/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		"./app/templates/**/*.html",
		"./app/templates/*.html",
		"./app/static/src/**/*.js"
	],
	theme: {
		extend: {
			colors: {
				"theme-clr": "var(--theme-clr)",
				"theme-hvr-clr": "var(--theme-hvr-clr)",
				"outline-clr": "var(--outline-clr)"
			},
		},
	},
	plugins: [],
}

