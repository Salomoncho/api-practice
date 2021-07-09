# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.9 [installed locally](https://docs.python-guide.org/starting/installation/). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/heroku/python-getting-started.git
$ cd python-getting-started

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku main

develop:
$  git push heroku-dev develop:main

Production:
$  git push heroku-prod master


$ heroku run python manage.py migrate
$ heroku open
```

or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

## React Installation:

1- Create the following files:

```
django-admin startapp frontend

cd frontend

create dirs:
-root
----frontend
  --src
      --components

  --static
      --css
      --frontend
      --images

  --template

```

# setting up react environment

```
npm init -y

npm i webpack webpack-cli --save-dev

npm i @babel/core babel-loader @babel/preset-env --save-dev

npm i react react-dom --save-dev

npm install @material-ui/core

npm install @babel/plugin-proposal-class-properties

npm install react-router-dom

npm install @material-ui/icons

```

# Configure config files:

babel.config.json

```
{
  "presets": [
    [
      "@babel/preset-env",
      {
        "targets": {
          "node": "10"
        }
      }
    ],
    "@babel/preset-react"
  ],
  "plugins": ["@babel/plugin-proposal-class-properties"]
}
```

webpack.config.js

```
const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify("production"),
      },
    }),
  ],
};

```

# add scripts to package.json

```
  "dev": "webpack --mode development --watch",
  "build": "webpack --mode production"
```

# Create src/index.js

```

```
