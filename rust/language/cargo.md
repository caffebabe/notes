## Cargo is the Rust package manager

To accomplish this goal, Cargo does four things:

- Introduces two metadata files with various bits of package information.
- Fetches and builds your package’s dependencies.
- Invokes rustc or another build tool with the correct parameters to build your package.
- Introduces conventions to make working with Rust packages easier.

