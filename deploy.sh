mkdir package
pip install --target ./package requests munch
cd package
zip -r ../my_deployment_package.zip .
cd ..
zip my_deployment_package.zip lambda_function.py
rm -rf package
