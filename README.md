# animated-broccoli
mage.ai pipelines (mainly for project "filthy job stalker")

```
git clone https://github.com/kirilscherbach/animated-broccoli.git \
&& docker compose up --detach
```

[Open the UI on localhost](http://localhost:6789/)

The main pipeline is `job_digest_generator`

If you want to fully run it locally, you would have to point the `mage-mrge/io_config.yaml` to your local postgres instance and update `docker-compose.yml` so that it reads the secrets from your variables.
