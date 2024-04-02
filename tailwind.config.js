/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		"./app/templates/**/*.html",
		"./app/templates/*.html",
		"./app/static/src/**/*.js",
		"./node_modules/flowbite/**/*.js"
	],
	theme: {
		extend: {
			colors: {
				"theme-clr": "var(--theme-clr)",
				"theme-hvr-clr": "var(--theme-hvr-clr)",
				"outline-clr": "var(--outline-clr)",

				"alert-info": "var(--alert-info)",
				"alert-info-solid": "var(--alert-info-solid)",
				
				"alert-error": "var(--alert-error)",
				"alert-error-solid": "var(--alert-error-solid)",
				
				"alert-success": "var(--alert-success)",
				"alert-success-solid": "var(--alert-success-solid)",
				
				"alert-warning": "var(--alert-warning)",
				"alert-warning-solid": "var(--alert-warning-solid)",
				
			},
		},
	},
	plugins: [
		require("flowbite/plugin")
	]
}

