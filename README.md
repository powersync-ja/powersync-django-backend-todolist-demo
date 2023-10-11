# PowerSync Django Backend: Todo List Demo

## Overview
Demo Django application which has HTTP endpoints to authorize a PowerSync enabled application to sync data between a client device and a Postgres database.
This repo compliments the [PowerSync + Django React Native Demo: Todo List](https://github.com/michaelbarnes/powersync-django-react-native-todolist-demo)

## Requirements
This app needs on a Postgres instance that's hosted. For a free version for testing/demo purposes, visit [Supabase](https://supabase.com/).

## Running the app
1. Clone the respository
2. Follow the steps outlined in [PowerSync Custom Authentication Example](https://github.com/journeyapps/powersync-jwks-example), [Generate a key-pair](https://github.com/journeyapps/powersync-jwks-example#1-generate-a-key-pair) to get the keys you need for this app.
3. Create a new `.env` file in the root project directory and add the following variables:
```
POWERSYNC_PRIVATE_KEY=
POWERSYNC_PUBLIC_KEY=
POWERSYNC_URL=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```
4. Install dependancies
```sh
pip install -r requirements.txt
```
5. Run migrations on your Postgres database
```sh
python manage.py makemigrations
python manage.py migrate
```
6. Run the following SQL statement on your Postgres database:
```sql
create publication powersync for table api_list, api_todo;
```

## Start App
1. Run the following to start the application
```sh
python manage.py runserver
```
This will start the app on `127.0.0.1:8000`
2. Test the app the app is working by opening `http://127.0.0.1:8000/api/get_keys/` in the browser
3. You should get a JSON object as the response to that request

## Connecting the app with PowerSync 
This process is only designed for demo/testing purposes, and is not intended for production use. You won't be using ngrok to host your application and database.
1. Download and install [ngrok](https://ngrok.com/)
2. Run the ngrok command to create a HTTPS tunnel to your local application
```sh
ngrok http 8000
```
This should create the tunnel and a new HTTPS url should be availible e.g.
```sh
ngrok by @inconshreveable                                                                                                                  (Ctrl+C to quit)

Session Status                online
Account                       Michael Barnes (Plan: Free)
Update                        update available (version 2.3.41, Ctrl-U to update)
Version                       2.3.40
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://your_id.ngrok-free.app -> http://localhost:8000
Forwarding                    https://your_id.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              1957    0       0.04    0.03    0.01    89.93
```
3. Open the PowerSync Dashboard and paste the `Forwarding` url starting with HTTPS into the Credentials tab of your PowerSync instance e.g.
```
JWKS URI 
https://your_id.ngrok-free.app/api/get_keys/
```
Pay special attention to the URL, it should include the `/api/get_keys/` path as this is used by the PowerSync server to validate tokens and the demo will not work without it.

4. Update the `AppConfig.ts` if you're using the [PowerSync + Django React Native Demo: Todo List](https://github.com/michaelbarnes/powersync-django-react-native-todolist-demo) and set the `djangoUrl` value.