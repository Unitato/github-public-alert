# github-public-alert
Docker container to monitor a GitHub User and alert if a new repo becomes public.
## Requirements
You will need a basic GitHub api key - it doesn't need any special set of permissions
The project also uses [SendGrid](https://sendgrid.com/) for email delivery mechanism, you can register for a free tier.
## Usage
```
Copy and edit the configuration file: confg/secrets-sample.yaml -> config/secrets.yaml

# build the docker
docker build . -t github-public-alert
docker run -it -p8080:8080 --rm -v config/secrets.yaml:/app/secrets.yaml github-public-alert python /app/main.py
```
