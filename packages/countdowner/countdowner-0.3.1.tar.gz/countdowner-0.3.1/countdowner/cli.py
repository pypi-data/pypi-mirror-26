import click

import countdowner.main as m


@click.command(short_help='Get the current prices of your watchlist products')
@click.option('-o', '--out_path', default=None,
  help='CSV output path')
@click.option('-d', '--mailgun_domain', default=None,
  help='Mailgun domain key')
@click.option('-k', '--mailgun_key', default=None,
  help='Mailgun API key')
@click.option('-h', '--as_html', is_flag=True, default=True,
  help='Send the optional email as HTML if true;'
  'otherwise send it as text; defaults to True')
@click.option('-a', '--async', is_flag=True, default=True,
  help='Collect the product prices asynchronously; defaults to True')
@click.argument('watchlist_path')
def countdownit(watchlist_path, out_path, mailgun_domain=None,
  mailgun_key=None, as_html=True, async=True):
    """
    Read a YAML watchlist located at ``--watchlist_path``,
    collect all the product information from Countdown, and
    write the result to a CSV located in the directory ``--out_dir``,
    creating the directory if it does not exist.
    If ``--domain`` (Mailgun domain) and ``--key`` (Mailgun API key)
    are given, then email the products on sale (if there are any)
    to the email address listed in the watchlist.
    """
    m.run_pipeline(watchlist_path, out_path, mailgun_domain, mailgun_key,
      as_html=as_html, async=async)
