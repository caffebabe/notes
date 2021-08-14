## Config

Config organizes hierarchical or layered configurations for Rust applications.

Config lets you set a set of default parameters and then extend them via merging in configuration from a variety of sources:

- Environment variables
- Another Config instance
- Remote configuration: etcd, Consul
- Files: JSON, YAML, TOML, HJSON
- Manual, programmatic override (via a .set method on the Config instance)

Additionally, Config supports:

- Live watching and re-reading of configuration files
- Deep access into the merged configuration via a path syntax
- Deserialization via **serde** of the configuration or any subset defined via a path
