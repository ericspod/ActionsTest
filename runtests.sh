#! /bin/bash 

PY_EXE=${TEST_PY_EXE:-$(which python)}

homedir="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Run tests under $homedir"
cd "$homedir"

echo "Using Python '$PY_EXE'"

function is_pip_installed() {
	return $("${PY_EXE}" -c "import sys, importlib.util; sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)" $1)
}

if ! is_pip_installed black
then
    pip install black
fi

"${PY_EXE}" -m black -l 120 --skip-magic-trailing-comma "$homedir"
