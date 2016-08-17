from terminaltables import SingleTable

import sys
import click
import arrow
import untangle
import requests
import textwrap
import dateutil.parser


class APIProxy(object):
    def req(self, parse=True, **params):
        params.update(dict(apikey=self.apikey))
        response = requests.get(self.endpoint, params=params)

        if self.debug:
            click.echo('-'*80)
            click.echo(response.url)
            click.echo('-'*80)
            click.echo(response.content)
            click.echo('-'*80)

        if parse:
            return self._parse(response.text)
        return response

    def _parse(self, content):
        result = untangle.parse(content)
        try:
            error = result.error
        except:
            return result
        else:
            click.echo('Error %s: %s' % (error['code'], error['description']))
            sys.exit(0)


proxy = APIProxy()


def date(text, humanize=True):
    d = arrow.get(dateutil.parser.parse(text))
    if humanize:
        return d.to('local').humanize()
    return d.to('local').format('YYYY-MM-DD HH:mm')


@click.group()
@click.option('--endpoint', envvar='NZ_ENDPOINT', required=True,
              help='The Newznab API endpoint to use.')
@click.option('--apikey', envvar='NZ_APIKEY', required=True,
              help='API key for your Newznab endpoint.')
@click.option('--debug', default=False, is_flag=True,
              help='Enable debug')
@click.version_option()
def cli(endpoint, apikey, debug):
    '''Command line interface to Newznab API endpoints.'''

    proxy.endpoint = endpoint
    proxy.apikey = apikey
    proxy.debug = debug


@cli.command()
@click.option('--category', multiple=True)
@click.argument('query', default='')
def search(category, query):
    '''Search for content.'''

    params = dict(t='search', cat=','.join(category))
    if query:
        params['q'] = query

    results = proxy.req(**params)
    try:
        results = results.rss.channel.item
    except:
        results = []

    data = [('Title', 'Date', 'Size (GB)', 'GUID')]

    for result in results:
        attrs = dict((e['name'], e['value']) for e in result.newznab_attr)

        data.append([
            '\n'.join(textwrap.wrap(result.title.cdata, 60)),
            date(result.pubDate.cdata),
            '%0.2f' % (int(attrs['size']) / 1024.0 / 1024.0 / 1024.0),
            result.guid.cdata.rsplit('/', 1)[1]
        ])

    table = SingleTable(data, title='Search Results: %s' % query)
    click.echo(table.table)


@cli.group()
def categories():
    '''Category related commands.'''


@categories.command()
def list():
    '''List categories.'''

    cats = proxy.req(t='caps').caps.categories.category

    def _echo_category(category, level=0):
        click.echo(
            '%s%s [%s]' % (('   ' * level), category['name'], category['id'])
        )

        if level == 0:
            for subcategory in getattr(category, 'subcat', []):
                _echo_category(subcategory, level=1)

    for category in cats:
        _echo_category(category)
        click.echo()


@cli.group()
def nzb():
    '''Commands for a particular NZB.'''


@nzb.command()
@click.argument('guid')
def details(guid):
    '''Get details about a particular NZB.'''

    details = proxy.req(t='details', id=guid).rss.channel.item
    attrs = dict((e['name'], e['value']) for e in details.newznab_attr)

    data = [
        ('Title:', details.title.cdata),
        ('Date:', date(details.pubDate.cdata, humanize=False)),
        ('Category:', details.category.cdata),
        ('Size:', '%0.2f GB' % (int(attrs['size']) / 1024.0 / 1024.0 / 1024.0))
    ]

    table = SingleTable(data, title='Details: %s' % details.title.cdata)
    table.inner_heading_row_border = False
    click.echo(table.table)


@nzb.command()
@click.argument('guid')
def download(guid):
    '''Download the specified NZB.'''

    response = proxy.req(t='get', id=guid, parse=False).content

    filename = '%s.nzb' % guid
    with open(filename, 'wb') as nzb:
        nzb.write(response)

    click.echo('NZB has been downloaded to: %s' % filename)


@nzb.command()
@click.argument('guid')
def nfo(guid):
    '''Print NFO for specified NZB, if available.'''

    response = proxy.req(t='info', id=guid, parse=False)
    if 'No such function' in response.text:
        response = proxy.req(t='getnfo', guid=guid, parse=False)

    if 'error code="300"' in response.text:
        click.echo('Release does not have an NFO file associated.')
    else:
        click.echo(response.content)
