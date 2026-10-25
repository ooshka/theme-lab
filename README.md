# Terminal Theme Lab

A local visual editor for designing a 16-color Windows Terminal scheme. It provides exact color inputs, realistic ANSI output, contrast checks, and JSON export while keeping the palette separate from machine-specific Terminal settings.

## Setup

```bash
python3 -m venv .venv
```

The project has no runtime dependencies outside Python's standard library.

## Edit a palette

```bash
.venv/bin/python theme_lab.py serve
```

Open <http://localhost:8765> from Windows. Color changes preview immediately. Click a color square to use the browser's visual picker, or enter a precise hex value. **Save palette** writes changes to `themes/nova.json`; **Download JSON** downloads a Windows Terminal scheme object.

The server binds to `0.0.0.0` by default so Windows can reach the WSL-hosted
site at <http://localhost:8765>, matching the setup used by the other local
project webservers. This may also expose the unauthenticated editor to other
interfaces when allowed by the Windows firewall. For a loopback-only listener,
run:

```bash
.venv/bin/python theme_lab.py serve --host 127.0.0.1
```

## Export

```bash
.venv/bin/python theme_lab.py export --output dist/nova.windows-terminal.json
```

The exported object is ready to add to the `schemes` array in Windows Terminal's `settings.json`. The stable scheme name is `Nova`, so profiles do not need to change as the palette evolves.

## Test

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```
