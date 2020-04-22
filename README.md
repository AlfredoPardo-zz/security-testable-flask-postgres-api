# Security Testable Flask Postgres API

You may need to update the `config.yaml` file with the IP address or hostname of your superset database and set `initialize_db` to False if you don't need initially load table data

## Building and Running the API

> $ cd api

> $ docker build -t sfta .

>$ docker run --rm -it -p 5000:5000 --network=apache-superset_default --name=sfta sfta

**Note**: You may need to check with `docker network ls` if the network name is correct.

