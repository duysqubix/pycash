# Pycash

A cli utility for cryptocurrencies written in python, using [CoinAPI.io](https://www.coinapi.io)


# Quick Usage

Create a new file in the main project directory, `.env` and define `COIN_API_KEY`. You can get a free one [here](https://www.coinapi.io/market-data-api/pricing#)

```bash
docker pull qubixds/pycash && docker run --rm qubixds/pycash --help
```

# Build Instruction

Requires `python 10.0+` and [poetry](https://python-poetry.org)

```bash 
cd $PROJECT_DIR && \
poetry install && \
poetry run pycash --help
```

Wrap it in a bash script for convenience, `pycash`

```bash
#!/bin/bash 

docker run --rm qubixds/pycash "$@" # save as `pycash`
#-------------------------------------------------------#


chmod +x pycash && \
sudo cp pycash /usr/local/bin/`

pycash --help
```