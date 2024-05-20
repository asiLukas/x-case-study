# GymBeam case study
## Installation
### Environment
- Build the Odoo 17 image from the supplied Dockerfile
- This will create a local image with pre-made environment that the docker-compose can use
- `docker build .`
- Note: when testing, I have noticed that when I build the image, it creates a local image with name `<none>`,
and for the docker-compose to recognize it, it **needs** to be renamed:
- `docker images` -> get the `IMAGE_ID` of the last `<none>` named image
- `docker tag IMAGE_ID odoo:17.0`
- Run docker-compose to create web -> odoo:17, db-> postgres:13 and mailhog containers:
- `docker compose build`
- `docker compose up -d`
### Odoo:
- Create a database
- Install Gymbeam Employee and Gymbeam Applicant apps
