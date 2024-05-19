# GymBeam case study

### Installation
- Build the Odoo 17 image from the supplied Dockerfile.
- This will create a local image with pre-made environment that the docker-compose can use.
- `docker build .`
- Note: when testing, I have noticed that when i build the image, it create a local image with name <none>,
and for the docker-compose to recognize it, I need to rename it with:
- `docker tag IMAGE_ID odoo:17.0`

Run docker-compose to create web, db and mailhog containers:
`docker-compose build`
`docker-compose up -d`
