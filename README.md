# Theme Lab

A local visual editor for designing the shared Nova palette used across terminal-oriented tools. `themes/nova.json` is the source of identity; destination configurations are adapters maintained in their own repositories.

## Setup

```bash
python3 -m venv .venv
```

The project has no runtime dependencies outside Python's standard library.

## Edit the palette

```bash
.venv/bin/python theme_lab.py serve
```

Open <http://localhost:8765> from Windows. Color changes preview immediately. **Save palette** updates `themes/nova.json`.

The server binds to `0.0.0.0` by default for WSL-to-Windows forwarding. Use `--host 127.0.0.1` for a loopback-only listener.

## Export the canonical palette

There is one platform-neutral output:

```bash
.venv/bin/python theme_lab.py export --output dist/nova.palette.json
```

The export contains the normalized name, background, foreground, cursor, selection, and sixteen ANSI colors. It intentionally contains no Neovim highlight groups or Windows settings structure.

## Apply to a destination

Use an agent in the destination repository, providing `themes/nova.json` or `dist/nova.palette.json` as the source.

- **Windows Terminal:** copy the palette fields into one object in the `schemes` array. The palette already uses Windows Terminal's field names; keep the scheme name `Nova`.
- **Neovim:** update only the `nova` palette table in `lua/user/theme.lua`. That file is the single theme entrypoint and owns the stable mapping from palette roles to syntax, Treesitter, Markdown, diagnostics, and plugin highlights.

Destination-specific behavior belongs at the destination. Do not add platform renderers here unless the shared palette schema itself needs to evolve.

## Test

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```
