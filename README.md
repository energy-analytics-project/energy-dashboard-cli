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
  config
  feed     Manage individual 'feed' (singular).
  feeds    Manage the full set of data 'feeds' (plural).
  license  Show the license (GPL v3).
```

### config

```bash
Usage: edc config [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  show    Show the config
  update  Update config
```

### feed

```bash
Usage: edc feed [OPTIONS] COMMAND [ARGS]...

  Manage individual 'feed' (singular).

Options:
  --help  Show this message and exit.

Commands:
  create  create new feed
  invoke  invoke a shell command in the feed directory
  status  show feeds status (NYI)
```

### feeds

```bash
Usage: edc feeds [OPTIONS] COMMAND [ARGS]...

  Manage the full set of data 'feeds' (plural).

Options:
  --help  Show this message and exit.

Commands:
  list    list feeds
  search  search feeds (NYI)
```

### license

```bash
    
    edc : Energy Dashboard Command Line Interface
    Copyright (C) 2019  Todd Greenwood-Geer (Enviro Software Solutions, LLC)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
```

##Usage

### Examples

```bash
edc feed invoke data-oasis-atl-lap-all "git st"
edc feed invoke data-oasis-atl-lap-all "ls"
edc feed invoke data-oasis-atl-lap-all "cat manifest.json"
edc feed invoke data-oasis-atl-lap-all "head manifest.json"
edc feeds list
edc feeds list | grep atl
edc feeds list | grep atl | edc feed invoke "head manifest.json"
edc feeds list | grep atl | edc feed invoke "head manifest.json" -
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "head manifest.json"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "jq . < manifest.json"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "jq .url < manifest.json"
edc feeds list | grep mileage | xargs -L 1 -I {} edc feed invoke {} "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "jq .url < manifest.json"
edc feeds list| xargs -L 1 -I {} edc feed invoke {} "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status {}
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status --header {}
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status --header {}
edc feeds list | grep mileage | xargs -L 1 -I {} edc feed status --header {}
```

## Author
Todd Greenwood-Geer (Enviro Software Solutions, LLC)
