# PowerSync Django Backend: Todo List Demo

## Overview

Demo Django application which has HTTP endpoints to authorize a [PowerSync](https://www.powersync.com/) enabled application to sync data between a client device and a Postgres database.
This repo complements these demo apps:
* [PowerSync + Django React Native Demo: Todo List](https://github.com/powersync-ja/powersync-js/tree/main/demos/django-react-native-todolist)
* [PowerSync + Django Flutter Demo: Todo List](https://github.com/powersync-ja/powersync-js/tree/main/demos/django-todolist)

For usage with PowerSync Open Edition, you can use [self-host-demo](https://github.com/powersync-ja/self-host-demo).
The remainder of these instructions assume you wish to use PowerSync cloud, which is more complicated.

## Requirements

* [ngrok](https://ngrok.com/) is used here for demo/testing purposes, to expose the JWKS endpoint to PowerSync Cloud. You won't be using ngrok to host your application and database in production.
* a paid ngrok plan. Ngrok has been progressively making their free version harder to use. Specifically, they now inject an interstitial warning page that requires a paid plan to remove.
* a hosted Postgres instance. For a free version for testing/demo purposes, visit [Supabase](https://supabase.com/).

## Running the app

1. Clone the repository
2. Follow the steps outlined in [PowerSync Custom Authentication Example](https://github.com/journeyapps/powersync-jwks-example) → [Generate a key-pair](https://github.com/journeyapps/powersync-jwks-example#1-generate-a-key-pair) to get the keys you need for this app.
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

4. Install dependencies

```sh
pip install -r requirements.txt
```

5. Run migrations on your Postgres database

```sh
python manage.py makemigrations
python manage.py migrate
```

Note that one of the migrations creates a test user in the `auth_user` table - you can use it to log into your frontend app. Take note of the user's id and update the hard coded id in the `upload_data` endpoint of `api/views.py` to match this user's id. In production you'd typically want to authenticate the user on this endpoint (using whatever auth mechanism you already have in place) before signing a JWT for use with PowerSync. See an example [here](https://github.com/powersync-ja/powersync-jwks-example/blob/151adf17611bef8a60d9e6cc490827adc4612da9/supabase/functions/powersync-auth/index.ts#L22)


## Start App

1. Run the following to start the application

```sh
python manage.py runserver
```

This will start the app on `127.0.0.1:8000`

2. Test the app the app is working by opening `http://127.0.0.1:8000/api/get_keys/` in the browser

3. You should get a JSON object as the response to that request

## Connecting the app with PowerSync

1. Run the ngrok command to create a HTTPS tunnel to your local application

```sh
ngrok http 8000
```

This should create the tunnel and a new HTTPS URL should be availible e.g.

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

2. Update ALLOWED_HOSTS in `todo_list_custom_backend/settings.py` to include your ngrok forwarding address e.g. `http://your_id.ngrok-free.app`, then restart your Django app.

3. Open the [PowerSync Dashboard](https://powersync.journeyapps.com/) and paste the `Forwarding` URL starting with HTTPS into the Credentials tab of your PowerSync instance e.g.

```
JWKS URI
https://your_id.ngrok-free.app/api/get_keys/
```

Pay special attention to the URL, it should include the `/api/get_keys/` path as this is used by the PowerSync server to validate tokens and the demo will not work without it.

4. Update your frontend app config
- React Native: `AppConfig.ts` if you're using the [PowerSync + Django React Native Demo: Todo List](https://github.com/powersync-ja/powersync-js/tree/main/demos/django-react-native-todolist) example client app and set the `djangoUrl` value.
- Flutter: set `djangoUrl` in `lib/app_config.dart`
