# Right-sizing STAC

[Cloud-Native Geospatial](https://guide.cloudnativegeo.org/) is a collection of specifications, tools, and ideas around how **geospatial data** can be queried, visualized, and analyzed _at rest_, without heavy infrastructure.
We're bringing the same philosophy to **geospatial metadata** via [stac-geoparquet](https://github.com/stac-utils/stac-geoparquet/blob/main/spec/stac-geoparquet-spec.md).
We hope these new technologies and tools will provide more flexibility and efficiency in how metadata are stored and queried.

## What the STAC?

The [SpatioTemporal Asset Catalog (STAC)](https://stacspec.org) specification is a **common language to describe geospatial information**.
Built on battle-tested geospatial standards and specifications such as [GeoJSON](https://geojson.org/) and [OGC API - Features](https://ogcapi.ogc.org/features/), STAC has a huge (and growing) number of [implementations](https://stacindex.org/catalogs) with single instances containing over [hundreds of million items](https://developers.planet.com/blog/2022/Aug/31/state-of-stac/).
But STAC isn't just for large organizations and companies; it can be used in any system where geospatial assets need to be stored and indexed for later use by humans, machines, or interfaces.

Most existing [STAC API](https://github.com/radiantearth/stac-api-spec) backends use customized instances of existing data store systems, such as [pgstac (for postgres)](https://github.com/stac-utils/pgstac) or [elaticsearch/opensearch](https://github.com/stac-utils/stac-fastapi-elasticsearch-opensearch).
Each of those backends support huge (>100 million items) instances, such as [Microsoft's Planetary Computer](https://planetarycomputer.microsoft.com/) or [AWS's Earth Search](https://earth-search.aws.element84.com/v1).
However, because these backends are meant to scale, they can be awkward to use for smaller data holdings, and they can be expensive when deployed via a cloud provider's [off-the-shelf services](https://aws.amazon.com/rds/).

## Cloud-Native Geospatial Metadata

Enter [geoparquet](https://geoparquet.org/), a geospatial-specific flavor of the powerful column-oriented data format [parquet](https://parquet.apache.org/).
**geoparquet** is natively _queryable_, meaning that clients, such as [DuckDB](https://duckdb.org/), can search directly from a **geoparquet** file.
In fact, DuckDB has an officially-supported [spatial extension](https://duckdb.org/docs/stable/extensions/spatial/overview.html) for doing exactly this.

```sql
D install spatial;
D load spatial;
D select * from read_parquet('s3://stac-fastapi-geoparquet-labs-375/naip.parquet')
  where st_intersects(geometry, st_geomfromgeojson('{"type":"Point","coordinates":[-105.1019,40.1672]}'));
┌─────────┬──────────────┬──────────────────────┬──────────────────────┬───────────────┬───┬───────────┬──────────────────────┬───────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│  type   │ stac_version │   stac_extensions    │          id          │  proj:shape   │ … │ naip:year │      proj:bbox       │ proj:epsg │      providers       │         bbox         │       geometry       │
│ varchar │   varchar    │      varchar[]       │       varchar        │    int64[]    │   │  varchar  │       double[]       │   int64   │ struct(url varchar…  │ struct(xmin double…  │       geometry       │
├─────────┼──────────────┼──────────────────────┼──────────────────────┼───────────────┼───┼───────────┼──────────────────────┼───────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ Feature │ 1.1.0        │ [https://stac-exte…  │ co_m_4010556_sw_13…  │ [12240, 9550] │ … │ 2021      │ [489150.0, 4441434…  │   26913   │ [{'url': https://w…  │ {'xmin': -105.1274…  │ POLYGON ((-105.060…  │
├─────────┴──────────────┴──────────────────────┴──────────────────────┴───────────────┴───┴───────────┴──────────────────────┴───────────┴──────────────────────┴──────────────────────┴──────────────────────┤
│ 1 rows                                                                                                                                                                                 19 columns (11 shown) │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The only missing piece was to bridge the gap between STAC and **geoparquet**.
[Tom Augsburger](https://github.com/TomAugspurger) began work in [May 2022](https://github.com/stac-utils/stac-geoparquet/commit/8b39b72a5694ea08ec9aaeea37d53bf589969787) with an implementation that used a [GeoDataFrame](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.html) as an intermediate representation.
Since then, the original [stac-geoparquet](https://github.com/stac-utils/stac-geoparquet) code has matured to be more performant and support alternative storage mechanisms, including [Delta Lake](https://delta.io/).
In parallel we've added an intuitive **stac-geoparquet** interface to [rustac](https://github.com/stac-utils/rustac-py), which binds more directly to the underlying Rust libraries such as [geoarrow-rs](https://github.com/geoarrow/geoarrow-rs/).

## But does it work?

Microsoft's Planetary Computer showed that [stac-geoparquet can be useful for bulk STAC item queries](https://planetarycomputer.microsoft.com/docs/quickstarts/stac-geoparquet/).
But we wondered if we could adapt **stac-geoparquet** to work with existing STAC tooling, such as [pystac-client](https://pystac-client.readthedocs.io/) or [stac-browser](https://radiantearth.github.io/stac-browser).
To do so, we built a prototype [stac-fastapi-geoparquet](https://github.com/stac-utils/stac-fastapi-geoparquet/) to put a "serverless" API layer in front of **stac-geoparquet**.

![stac-fastapi-geoparquet architecture](./img/stac-fastapi-geoparquet-architecture.excalidraw.png)

This architecture should be extremely affordable, since we're only utilizing light "serverless" services and blob storage.
To see if it worked, we ran a series of experiments where we compared **stac-fastapi-geoparquet** with a **stac-fastapi-pgstac** instance with the same data.
These results are preliminary, but encouraging.

### The good

For small- to medium-sized datasets (e.g. less than 100k items) **stac-fastapi-geoparquet** serves large pages of items faster than **stac-fastapi-pgstac**.

![paging speed](./img/search-page-speed.png)

### The bad

A database, such as **pgstac**, will usually be faster than a DuckDB query against **stac-geoparquet** when searching for one or a few items ("needle in a haystack").

![search by attributes](./img/searc-by-attributes.png)

### The ugly

At large scales (e.g. over two million items) **stac-fastapi-geoparquet** falls over — our lambda times out during a single item search.

## What next?

We'd like to bring these experiments into the real world to prove them out more.
If you've got small-to-medium-sized geospatial data holdings (think thousands to hundreds of thousands of assets), we'd love explore what we can do with (free, open-source) **stac-fastapi-geoparquet** to help you!

To see how we ran experiments and their results, check out our [labs repository](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/).
