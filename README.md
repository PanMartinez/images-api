# IMAGES-API

This is simple API for images uploading and resizing.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Installation
To run this project locally, clone the repo and run:

```bash
docker-compose up --build
```
This will start the API on port 8000. You can then access the API at http://localhost:8000/api.

All following commands can be executed if `web` container is running.

To access django shell run:
```bash
docker-compose exec web python manage.py shell
```

To run tests:
```bash
docker-compose exec web pytest
```

---

## Usage
Application uses swagger for API documentation. To access it, go to http://localhost:8000/.

To upload an image, send a POST request to `/api/images/` with the image file in the request body.
The API will resize uploaded image and return it in the response.

To get a resized image, send a GET request to `/api/images/<image_id>/`, and to get list of all images, send a GET
request to `/api/images/`.

---

## Contributing
Contributions are welcome! Please submit a pull request with your changes.

Application uses pre-commit hooks. Before committing anything, run `pre-commit install` to install them.

---

## License
This project is licensed under the MIT License.
