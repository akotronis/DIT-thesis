# Commands
## Docker
- Build the image: `../app/back$ docker build -t img-dit-back .[ --no-cache --progress=plain]`
- Run the image: `../app/back$ docker run --name ctr-dit-back -d --rm -v "$(pwd):/opt/back" -p 8000:8000 img-dit-back`