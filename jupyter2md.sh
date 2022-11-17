rm -rf content/generated
mkdir -p content/generated
jupyter nbconvert --to markdown notebooks/*.ipynb --output-dir content/generated/
