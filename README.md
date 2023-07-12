# Fivetran Custom Connector: npm Downloads

This is a [Fivetran custom connector](https://fivetran.com/docs/functions) for retrieving package download numbers from [npm](https://www.npmjs.com/). Given a list of package names, the connector incrementally fetches the data according to the schedule specified in Fivetran.

The connector was built for AWS but will probably also work on Google Cloud Functions / Azure Functions with minor adjustments. Although issues are welcomed, it is provided as-is with no support or maintenance guarantees. 

## Setup
1. Add a new connector in Fivetran by clicking _Add Connector_ and searching for _AWS Lambda_.
1. Follow steps 1, 2 and 3 in the [setup guide](https://fivetran.com/docs/functions/aws-lambda/setup-guide).
1. Open a new terminal and run `sh deploy.sh` to generate `deployment-package.zip`.
1. Follow step 4 of the setup guide, except:
    - Choose _Author from scratch_ when creating a new Lambda.
    - Upload the zip file when prompted to add your code.
    - Go to _Configuration_ > _Environment variables_ and add a new one called `NPM_PACKAGES`. The value should be a comma-separated string of package names, e.g. `package1,package2,@org/package3`.
1. Finish setting up the function.

You should now be able to trigger the first sync in Fivetran.

## Usage Notes
By default, daily download numbers will be fetched starting from 1st Jan 2018. This can be changed by updating the `DEFAULT_DATE` variable in `lambda_function.py`. New packages can be added at any time by editing the environment variable.

Sometimes npm's API returns 0 downloads for all packages on a given day. This can be fixed by waiting for the API to be fixed and fully resyncing the connector, or manually adding new rows to your destination table.
