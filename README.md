# Price tracker for digitec.ch and galaxus.ch

[![Travis CI Status](https://secure.travis-ci.org/fredj/dg-price-tracker.svg)](http://travis-ci.org/#!/fredj/dg-price-tracker)

Build:

```bash
docker build -t dg_updater updater/
```

Run:

```bash
docker run -e GITHUB_TOKEN=xxx dg_updater
```
