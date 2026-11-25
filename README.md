# Process Monitor

List the top processes by CPU or memory usage, using the `ps` command.

## Requirements

- Python 3.8+
- Standard library only — no third-party packages
- The `ps` command (present on Linux and macOS)

## Usage

```bash
python3 main.py
python3 main.py --sort mem --limit 5
python3 main.py --sort cpu --user root
```

## Example

```bash
$ python3 main.py --sort cpu --limit 3
    PID USER         %CPU  %MEM  COMMAND
------------------------------------------------------------
   1234 alice        12.3   1.2  /usr/bin/python3 main.py
    567 bob           4.1   0.8  /usr/lib/firefox/firefox
    890 alice         2.0   0.5  /usr/bin/gnome-shell

Showing 3 process(es) sorted by CPU usage.
```

## License

MIT — see [LICENSE](LICENSE).
