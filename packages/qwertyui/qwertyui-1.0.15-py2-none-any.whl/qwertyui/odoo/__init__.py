import datetime
import os
import requests
import tempfile

from qwertyui import urlparse


def get_odoo_version(host, **kwargs):
    r = requests.post(
        '{}/jsonrpc'.format(host),
        headers={'Content-Type': 'application/json'},
        json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'call',
            'params': {
                'method': 'server_version',
                'service': 'db',
                'args': {}
            }
        },
        **kwargs
    )
    return r.json()['result']


def get_server_version(host, **kwargs):
    r = requests.post(
        '{}/jsonrpc'.format(host),
        headers={'Content-Type': 'application/json'},
        json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'call',
            'params': {
                'method': 'server_version',
                'service': 'db',
                'args': {}
            }
        },
        **kwargs
    )

    return r.json()['result']


def list_dbs(host, **kwargs):
    r = requests.post(
        '{}/jsonrpc'.format(host),
        headers={'Content-Type': 'application/json'},
        json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'call',
            'params': {
                'method': 'list',
                'service': 'db',
                'args': {}
            }
        },
        **kwargs
    )

    return r.json()['result']


def download_backup(host, db, master_pwd, backup_dir=None, backup_format='zip', chunk_size=16384):
    """
    Downloads a full backup of an ODOO database and all data files.
    """

    if not backup_dir:
        backup_dir = tempfile.mkdtemp()

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    session = requests.Session()

    session.get(
        '{}/web'.format(host),
        params={'db': db},
        verify=True
    )
    resp = session.post(
        '{}/web/database/backup'.format(host),
        {'master_pwd': master_pwd, 'name': db, 'backup_format': backup_format},
        stream=True,
        verify=True
    )
    if 'application/octet-stream' not in resp.headers['Content-Type']:
        raise Exception('Content-type is not application/octet-stream, no zipfile received!')

    now = datetime.datetime.now()
    parsed = urlparse(host)
    file_name = 'backup-{hostname}-{db}-{now}.{ext}'.format(
        hostname=parsed.hostname,
        db=db,
        now=now.strftime('%Y%m%d-%H%M%S'),
        ext=backup_format
    )
    file_path = os.path.join(backup_dir, file_name)

    with open(file_path, 'wb') as f:
        size = 0
        for chunk in resp.iter_content(chunk_size):
            f.write(chunk)
            size += len(chunk)

    return file_path, size


def download_all_backups(host, master_pwd, backup_dir=None, **kwargs):
    """
    Similar to download_backup above but downloads backups of all dbs for the specified ODOO host.
    """

    if not backup_dir:
        backup_dir = tempfile.mkdtemp()

    backups = {}

    for db in list_dbs(host):
        backups[db] = download_backup(
            host,
            db,
            master_pwd,
            backup_dir=backup_dir,
            **kwargs
        )

    return backups


def upload_backup(host, db, master_pwd, file_content, copy=True, content_type='application/zip'):
    """
    Uploads backup to host under new db name 'db'.
    """

    session = requests.Session()

    resp = session.post(
        '{}/web/database/restore'.format(host),
        {
            'copy': 'true' if copy else 'false',
            'master_pwd': master_pwd,
            'name': db,
        },
        files={
            'backup_file': ('backup-file', file_content, content_type),
        },
        verify=True
    )

    return resp
