### Features

- Upload a large CSV file through the web that contains product details.
- This file is processed asynchronously by a celery worker and the progress is shown on the UI(user interface).
- Filter through the list of available products.
- Create/Read/Update/Delete individual products through the web interface.
- Add webhooks to be notified about an event(creation/updation/deletion of a product through the UI).
- Delete all products and start a fresh import if required.


### Usage guidelines

- As of now, the project is deployed on http://143.244.132.242/products.

#### View and filter

- The list of products can viewed at: http://143.244.132.242/products.

- Their is also a form at the top that may be used to filter the products based on various fields.

### Create, Update and Delete

- There is a button on the button that allows you to create products from the web interface.
- For updation and deletion purpose, you may click on an individual product.

#### Webhooks

- You may visit the URL http://143.244.132.242/products/create-webhook/ to create a web hook.

- For testing purpose, you may use the website: https://ptsv2.com/ to test the actual output of the webserver.


#### Import Products

- You may visit the URL http://143.244.132.242/products/import/ to import products from a CSV file.
- Once the upload is complete, you will be redirected to the list view that displays the number of products processed by the database.


### Development

- Copy the sample `environment configuration` inside `.env.sample` to `.env` file.
- `docker` and `docker-compose` is required for set up.
- If you have the `make` command on your end, you may use the command `make build` and `make up` to build and run the image. There are some other helpful commands that may be viewed inside the `Makefile`.
- If `make` is not available, you may run the command `docker-compose build .` followed by `docker-compose up` to launch the development server.
- It is recommended to install `pre-commit` hooks preferable in a separate virtual environment. This helps in style conformation throughout the project.
    #### Set up instructions
    ```sh
    python -m venv venv
    pip install pre-commit
    pre-commit run
    ```

### Deployment

- Run `docker-compose -f docker-compose.yaml -f docker-compose.production.yaml build` to build the image.
- Run `docker-compose -f docker-compose.yaml -f docker-compose.production.yaml up -d` to run the image.

