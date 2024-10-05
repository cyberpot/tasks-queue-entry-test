# How to run

Create `.env` file according to `sample.env`

```bash
cp sample.env .env
```

Build docker image
```bash
docker-compose build
```

Run containers
```bash
docker-compose up
```

The compose file includes the `tests` configuration