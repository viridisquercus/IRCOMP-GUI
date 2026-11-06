# Local exchange format

The standalone GUI uses UTF-8 JSON format `1.0`. This is its local exchange
boundary; it is not the IRCOMP compiler specification.

- [exchange.schema.json](exchange.schema.json): request, evidence and review
  envelopes with shared definitions; all references are local.
- [catalogue.json](catalogue.json): supported reference metadata and profiles.
- [examples](examples/): one request and compatible, empty or mismatching evidence.
  These are synthetic demonstration data.
- [NCBI report](references/grch38-p14-assembly-report.txt): source identifiers and
  lengths for the catalogue's explicit 24 nuclear chromosome subset.

A request contains a study/request ID, one complete revision and its target labels.
Evidence must match the request ID and whole selected revision, including interval
identities and reference context. Scores remain original observations; zero and
absence are distinct. Review dispositions and rationale belong to collection
membership, not to source evidence. Review exports include the complete original
source files with SHA-256 and label unresolved work as a draft.

The runtime applies schema and domain validation before accepting data. The
mismatching evidence file is intentionally refused for the selected sample request.
An empty candidate list is valid and does not imply any scientific computation.

Reference metadata does not prove sequence availability or biological suitability.
The catalogue excludes mitochondria, patches and alternative loci; it records its
source URL/hash. Current service types and limits are in `/docs` and
[architecture](../docs/architecture.md).

Future compiler ownership, missing specification fields and adapter gates are
recorded in [Confluence](https://viridisquercusnova.atlassian.net/wiki/spaces/IRCOMP/pages/29392897).
The executable local schema stays with this repository.
