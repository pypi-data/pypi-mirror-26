import os
import time
import json
import click
from tabulate import tabulate

from swag_client.backend import SWAGManager, validate
from swag_client.migrations import run_migration
from swag_client.util import parse_swag_config_options


def create_swag_from_ctx(ctx):
    """Creates SWAG client from the current context."""
    swag_opts = {}
    if ctx.obj['TYPE'] == 'file':
        swag_opts = {
            'swag.type': 'file',
            'swag.data_dir': ctx.obj['DATA_DIR'],
            'swag.data_file': ctx.obj['DATA_FILE']
        }
    elif ctx.obj['TYPE'] == 's3':
        swag_opts = {
            'swag.type': 's3',
            'swag.bucket_name': ctx.obj['BUCKET_NAME'],
            'swag.data_file': ctx.obj['DATA_FILE'],
            'swag.region': ctx.obj['REGION']
        }
    elif ctx.obj['TYPE'] == 'dynamodb':
        swag_opts = {
            'swag.type': 'dynamodb',
            'swag.region': ctx.obj['REGION']
        }
    return SWAGManager(**parse_swag_config_options(swag_opts))


@click.group()
@click.option('--namespace', default='accounts')
@click.pass_context
def cli(ctx, namespace):
    ctx.obj = {'NAMESPACE': namespace}


@cli.group()
@click.option('--region', default='us-east-1', help='Region the table is located in.')
@click.pass_context
def dynamodb(ctx, region):
    ctx.obj['REGION'] = region
    ctx.obj['TYPE'] = 'dynamodb'


@cli.group()
@click.option('--data-dir', help='Directory to store data.', default=os.getcwd())
@click.option('--data-file')
@click.pass_context
def file(ctx, data_dir, data_file):
    """Use the File SWAG Backend"""
    ctx.obj['DATA_DIR'] = data_dir
    ctx.obj['DATA_FILE'] = data_file
    ctx.obj['TYPE'] = 'file'


@cli.group()
@click.option('--bucket-name', help='Name of the bucket you wish to operate on.')
@click.option('--data-file', help='Key name of the file to operate on.')
@click.option('--region', default='us-east-1', help='Region the bucket is located in.')
@click.pass_context
def s3(ctx, bucket_name, data_file, region):
    """Use the S3 SWAG backend."""
    ctx.obj['BUCKET_NAME'] = bucket_name
    ctx.obj['DATA_FILE'] = data_file
    ctx.obj['TYPE'] = 's3'
    ctx.obj['REGION'] = region


@cli.command()
@click.pass_context
def list(ctx):
    """List SWAG account info."""
    if ctx.obj.get('NAMESPACE') != 'accounts':
        click.echo(
            click.style('Only account data is available for listing.', fg='red')
        )
        return

    swag = create_swag_from_ctx(ctx)
    accounts = swag.get_all()
    _table = [[result['name'], result.get('id')] for result in accounts]
    click.echo(
        tabulate(_table, headers=["Account Name", "Account Number"])
    )


@cli.command()
@click.option('--start-version', default=1, help='Starting version.')
@click.option('--end-version', default=2, help='Ending version.')
@click.pass_context
def migrate(ctx, start_version, end_version):
    """Transition from one SWAG schema to another."""
    if ctx.obj['TYPE'] == 'file':
        if ctx.obj['DATA_FILE']:
            file_path = ctx.obj['DATA_FILE']
        else:
            file_path = os.path.join(ctx.obj['DATA_DIR'], ctx.obj['NAMESPACE'] + '.json')

        # todo make this more like alemebic and determine/load versions automatically
        with open(file_path, 'r') as f:
            data = json.loads(f.read())

        data = run_migration(data, start_version, end_version)
        with open(file_path, 'w') as f:
            f.write(json.dumps(data))


@cli.command()
@click.pass_context
def propagate(ctx):
    """Transfers SWAG data from one backend to another"""
    data = []
    if ctx.obj['TYPE'] == 'file':
        if ctx.obj['DATA_FILE']:
            file_path = ctx.obj['DATA_FILE']
        else:
            file_path = os.path.join(ctx.obj['DATA_DIR'], ctx.obj['NAMESPACE'] + '.json')

        with open(file_path, 'r') as f:
            data = json.loads(f.read())

    swag_opts = {
        'swag.type': 'dynamodb'
    }

    swag = SWAGManager(**parse_swag_config_options(swag_opts))

    for item in data:
        time.sleep(2)
        swag.create(item)


@cli.command()
@click.pass_context
def create(ctx):
    """Create a new SWAG item."""
    pass


@cli.command()
@click.pass_context
@click.argument('data', type=click.File())
def update(ctx, data):
    """Updates a given record."""
    swag = create_swag_from_ctx(ctx)
    data = json.loads(data.read())

    for account in data:
        swag.update(account)


@cli.command()
@click.argument('data', type=click.File())
@click.pass_context
def seed_aws_data(ctx, data):
    """Seeds SWAG from a list of known AWS accounts."""
    swag = create_swag_from_ctx(ctx)
    for k, v in json.loads(data.read()).items():
        for account in v['accounts']:
            data = {
                    'description': 'This is an AWS owned account used for {}'.format(k),
                    'id': account['account_id'],
                    'contacts': [],
                    'owner': 'aws',
                    'provider': 'aws',
                    'sensitive': False,
                    'email': 'support@amazon.com',
                    'name': k + '-' + account['region']
                }

            click.echo(click.style(
                'Seeded Account. AccountName: {}'.format(data['name']), fg='green')
            )

            swag.create(data)


file.add_command(list)
file.add_command(validate)
file.add_command(migrate)
file.add_command(propagate)
file.add_command(create)
file.add_command(seed_aws_data)
file.add_command(update)
dynamodb.add_command(list)
dynamodb.add_command(create)
dynamodb.add_command(update)
dynamodb.add_command(seed_aws_data)
s3.add_command(list)
s3.add_command(create)
s3.add_command(update)
s3.add_command(seed_aws_data)


