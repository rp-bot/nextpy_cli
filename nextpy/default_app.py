import argparse
import subprocess
import os
import platform

CWD = os.getcwd()
OS = platform.system()


def command_maker(argument_dict):
    # TODO: classify the essential and non essential arguments to catch errors.
    # non_esential=["language", ]
    command = []
    for value in argument_dict.values():
        if value is not None:
            command.append(value)
    return command


def clean_up(project_name: str, app_dir: str):
    # clean up files in the directory
    if app_dir == "--app":
        with open(f"{project_name}/tailwind.config.js", "w+") as tailwind_config_js, open(f"{project_name}/src/app/globals.css", "w+") as globals_css, open(f"{project_name}/src/app/page.js", "w+") as index_js:
            tailwind_config_js.writelines(
                """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}""")
            globals_css.writelines(
                """@tailwind base;
@tailwind components;
@tailwind utilities;"""
            )
            index_js.writelines(
                """export default function Home() {
	return (
		<div className="bg-black">
			<div>Home Page</div>
		</div>
	);
}"""
            )

    elif app_dir == "--no-app":
        with open(f"{project_name}/tailwind.config.js", "w+") as tailwind_config_js, open(f"{project_name}/src/styles/globals.css", "w+") as globals_css, open(f"{project_name}/src/pages/index.js", "w+") as index_js:
            tailwind_config_js.writelines(
                """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}""")

            globals_css.writelines(
                """@tailwind base;
@tailwind components;
@tailwind utilities;"""
            )

            index_js.writelines(
                """export default function Home() {
	return (
		<div className="bg-black">
			<div>Home Page</div>
		</div>
	);
}"""
            )

    # FIXME this is os specific need to make it universal
    delete_process = subprocess.Popen(
        ['cmd', '/c', 'del', f'.\\{project_name}\\public\\*.svg', ], shell=True, text=True, cwd=CWD)
    delete_process.wait()


def auto_start_app(project_name, no_auto_arg=None):
    # change to specified project dir
    os.chdir(os.path.join(project_name))

    open_IDE = subprocess.Popen(
        ['code', f'.\\{project_name}', ], shell=True, text=True, cwd=CWD)
    open_IDE.wait()

    if no_auto_arg is None:
        # Start app
        install_command = subprocess.Popen(
            ['npm', 'install'], shell=True, text=True, cwd=os.getcwd())
        install_command.wait()

        run_command = subprocess.Popen(
            ['npm', 'run', 'dev'], shell=True, text=True, cwd=os.getcwd())
        run_command.wait()

    else:
        print("App was created, but wasn't started")


def main():

    parser = argparse.ArgumentParser(
        description='Another unnecessary level of automation.')

    # ProjectName
    parser.add_argument("project_name", type=str,
                        help="Type the name of the nextjs project. This will also be the name of your folder.")
    # Type script or javascript
    parser.add_argument("--typescript", "--ts", type=str, default="--js",
                        help="Specify if you WANT typescript. Default is javascript")

    # Tailwind or no Tailwind
    parser.add_argument("--no-tailwind", type=str, default="--tailwind",
                        help="Specify if you DON'T WANT tailwind. Default is WITH tailwind")

    # ESLint or no
    parser.add_argument("--no-eslint", type=str, default="--eslint",
                        help="Specify if you DON'T WANT eslint. Default is WITH eslint")
    # src dir or no
    parser.add_argument("--no-src-dir", type=str, default="--src-dir",
                        help="Specify if you DON'T WANT the src-dir. Default is WITH src-dir")

    # experimental app or no
    parser.add_argument("--no-app", type=str, default="--app",
                        help="Specify if you WANT the experimental-app. Default is WITHOUT experimental-app")

    # import alias or nah
    parser.add_argument("--no-import-alias", type=str, default="--import-alias",
                        help="Specify if you DON'T WANT the import alias. Default is it imports alias")

    # bootstrapclient arg
    parser.add_argument("--use-pnpm", type=str, default="--use-npm",
                        help="Specify if you WANT Pnpm. Default is npm")

    parser.add_argument("--next-help", type=str, default=None,
                        help="Next JS help")

    parser.add_argument("--no-auto-start", type=str, default=None,
                        help="Automatically start development server")

    args = parser.parse_args()
    # VERSION
    main_arguments = {
        "package_execution": "npx",
        "create_command": "create-next-app@latest",
        "version": None,
        "project_name": args.project_name,
        "language": args.typescript,
        "tailwind": args.no_tailwind,
        "eslint": args.no_eslint,
        "src_dir": args.no_src_dir,
        "no_app": args.no_app,
        "import_alias": args.no_import_alias,
        # TODO: Make Alias string customizable
        "alias_string": "@/*",
        "bootstrap_client": args.use_pnpm,

    }
    other_arguments = {"no_auto": args.no_auto_start}

    #  construct command
    main_command = command_maker(main_arguments)

    # run command
    x = subprocess.Popen(main_command, shell=True, text=True)
    x.wait()

    # Run clean up function if app was created or else dont
    clean_up(main_command[2], main_command[7]) if not x.poll() else None

    # Start app
    auto_start_app(main_command[2])


if __name__ == '__main__':
    main()
