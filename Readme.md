Google Sheets support is deprecated ( data/sheets ). Will continue from  Dynamo DB ( data/dynamodb )

To Build lambda layer

docker build -o .\lambda_layer\ .

Register Commands:
scripts/register_commands.py

Create lambda zip bundle:
scripts/bundle.py
