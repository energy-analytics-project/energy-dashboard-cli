# Energy Dashboard Command Line Interface (edc)

Command Line Interface for the Energy Dashboard.

Still a WIP...

## Show Help

```bash
Usage: edc [OPTIONS] COMMAND [ARGS]...

  Command Line Interface for the Energy Dashboard. This tooling  collects
  information from a number of data feeds, imports that data,  transforms
  it, and inserts it into a database.

Options:
  --config-dir TEXT     config file directory
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  config   Configure the CLI path : path to the energy dashboard
  feed     Manage individual 'feed' (singular).
  feeds    Manage the full set of data 'feeds' (plural).
  license  Show the license (GPL v3).
```

##Usage

### Examples

```bash
edc feed invoke data-oasis-atl-lap-all -c "git st"
edc feed invoke data-oasis-atl-lap-all -c "ls"
edc feed invoke data-oasis-atl-lap-all -c "cat manifest.json"
edc feed invoke data-oasis-atl-lap-all -c "head manifest.json"
edc feeds list
edc feeds list | grep atl
edc feeds list | grep atl | edc feed invoke "head manifest.json"
edc feeds list | grep atl | edc feed invoke -c "head manifest.json" -
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} -c "head manifest.json"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} -c "jq . < manifest.json"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} -c "jq .url < manifest.json"
edc feeds list | grep mileage | xargs -L 1 -I {} edc feed invoke {} -c "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} -c "jq .url < manifest.json"
edc feeds list| xargs -L 1 -I {} edc feed invoke {} -c "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status {}
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status --header {}
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status --header {}
edc feeds list | grep mileage | xargs -L 1 -I {} edc feed status --header {}
```

## Author
Todd Greenwood-Geer (Enviro Software Solutions, LLC)
