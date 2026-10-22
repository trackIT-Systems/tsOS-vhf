# tsOS-vhf Developer Documentation

Technical documentation for developers working on tsOS-vhf. Everything tsOS-vhf inherits (partitions, overlayroot, updates, security model, telemetry, logging) is documented in [tsOS-base](https://github.com/trackIT-Systems/tsOS-base/tree/main/docs).

## Documentation

- **[Architecture](architecture.md)** - What tsOS-vhf adds to tsOS-base
- **[Build System](build.md)** - Two-stage build, Pifile structure and releases
- **[Project Structure](structure.md)** - Repository organization
- **[Radiotracking](radiotracking.md)** - `radiotracking.service`: configuration, outputs, recovery and troubleshooting

## Quick Reference

**Build**: `docker-compose run --rm pimod pimod.sh tsOS-vhf.Pifile`

**Base**: [tsOS-base](https://github.com/trackIT-Systems/tsOS-base) 2027.0.6  
**Tool**: [pimod](https://github.com/Nature40/pimod) v0.9.3  
**Architecture**: arm64
