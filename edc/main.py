import click
import json
import os
import json

@click.group()
@click.option('--config-dir', default="~/.config/energy-dashboard", help="config file directory")
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, config_dir, debug):
    """
    Command Line Interface for the Energy Dashboard. This tooling 
    collects information from a number of data feeds, imports that data, 
    transforms it, and inserts it into a database.
    """
    ctx.obj = {
            'config-dir': config_dir,
            'debug': debug
            }

#------------------------------------------------------------------------------
# License
#------------------------------------------------------------------------------
@cli.command()
def license():
    """
    Show the license (GPL v3).
    """
    print("""    
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
    """)

#------------------------------------------------------------------------------
# Configure
#------------------------------------------------------------------------------
@cli.command()
@click.argument('path')
@click.pass_context
def config(ctx, path):
    """
    Configure the CLI

    path : path to the energy dashboard
    """
    debug = ctx.obj['debug']
    config_dir = os.path.expanduser(ctx.obj['config-dir'])
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        if debug: click.echo("created config dir: %s" % config_dir)
    cfg_file_path = os.path.join(config_dir, 'energy-dashboard-client.config')
    if os.path.exists(cfg_file_path):
        config = load_config(cfg_file_path)
        if debug: click.echo("loaded config file: %s" % cfg_file_path)
    else:
        config = empty_config()
        if debug: click.echo("loaded empty config")
    # override prev values
    config2 = Config(config, {'ed_path': path, 'cfg_file': cfg_file_path})
    config2.save()
    if debug: click.echo("saved config to: %s" % config2.cfg_file())



#------------------------------------------------------------------------------
# Feeds (plural)
#------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def feeds(ctx):
    """
    Manage the full set of data 'feeds' (plural).
    """
    pass

@feeds.command('list', short_help='list feeds (NYI)')
@click.pass_context
def feeds_list(ctx):
    cfg = load_config(ctx.obj['config-dir'])
    items = os.listdir(cfg.ed_path)
    return items

@feeds.command('search', short_help='search feeds (NYI)')
def feeds_search():
    pass

@feeds.command('status', short_help='show feeds status (NYI)')
def feeds_status():
    pass

#------------------------------------------------------------------------------
# Feed (singular)
#------------------------------------------------------------------------------
@cli.group()
def feed():
    """
    Manage individual 'feed' (singular).
    """
    pass

@feed.command('add', short_help='add new feed (NYI)')
def feed_add():
    pass


#------------------------------------------------------------------------------
# Config Stuff
#------------------------------------------------------------------------------
class Config():
    def __init__(self, config, m):
        """
        config  : Config instance
        m       : map of overrides
        """
        self._ed_path    = os.path.expanduser(m['ed_path']  or config.ed_path())
        self._cfg_file   = os.path.expanduser(m['cfg_file'] or config.cfg_file())

    def save(self) -> None:
        m               = {}
        m['ed_path']    = os.path.expanduser(self._ed_path)
        m['cfg_file']   = os.path.expanduser(self._cfg_file)
        with open(self._cfg_file, 'w') as outfile:
            json.dump(m, outfile, indent=4, sort_keys=True)

    def ed_path(self):
        return self._ed_path

    def cfg_file(self):
        return self._cfg_file

def empty_config() -> Config:
    return Config(None, {'ed_path':"", 'cfg_file':""})

def load_config(f:str) -> Config:
    with open(f, 'r') as json_cfg_file:
        m = json.load(json_cfg_file)
        return Config(None, m)
