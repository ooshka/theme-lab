# Theme Lab agent guidance

## Source of truth

- Treat `themes/nova.json` as the canonical Nova identity.
- Keep the schema platform-neutral: name, UI colors, and the sixteen ANSI colors.
- Use `theme_lab.py export` only to validate, normalize, and copy that palette.

## Applying Nova elsewhere

- Make destination changes in the destination repository, not in theme-lab.
- For Windows Terminal, map the palette directly into a `schemes` entry named `Nova`.
- For Neovim, change only the palette table in `lua/user/theme.lua`; keep that file as the single theme entrypoint.
- Preserve destination-specific highlight semantics and plugin integration unless the user explicitly asks to redesign them.
- Never invent extra colors while applying Nova. Use only canonical palette values, plus transparency where supported.

## Verification

- Run `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v` after theme-lab changes.
- Validate the destination with its native tooling after applying a palette update.
