import click

@click.group()
def cli():
    """
    Command Line Interface for the Energy Dashboard. This tooling 
    collects information from a number of data feeds, imports that data, 
    transforms it, and inserts it into a database.
    """
    pass

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
# Feeds (plural)
#------------------------------------------------------------------------------
@cli.group()
def feeds():
    """
    Manage the full set of data 'feeds' (plural).
    """
    pass

@feeds.command('list', short_help='list feeds (NYI)')
def feeds_list():
    pass

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
