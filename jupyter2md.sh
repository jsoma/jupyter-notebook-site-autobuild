rm -rf content/generated
mkdir -p content/generated
pipenv run jupyter nbconvert --to markdown notebooks/*.ipynb --output-dir content/generated/
