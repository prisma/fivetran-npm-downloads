poetry install
cd .venv
zip -r ../deployment-package.zip .
cd ..
zip -g deployment-package.zip lambda_function.py
