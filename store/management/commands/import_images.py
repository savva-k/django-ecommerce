#!/usr/bin/env python
import csv
from ftplib import FTP_TLS
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from pathlib import Path
from shutil import rmtree
from store.models import Image, Item


class Command(BaseCommand):
    TMP_DIR = './tmp/'
    help = 'Import images from a CSV file and an FTP server Warning: existing images will be overridden'

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='A CSV with columns: id, item_id, is_main, filename', required=True)
        parser.add_argument('--ftp_server', help='FTP server for importing images', required=True)
        parser.add_argument('--path', help='Path to images folder on the specified FTP server', required=True)
        parser.add_argument('--user', help='FTP server user', required=True)
        parser.add_argument('--password', help='FTP server password', required=True)

    def handle(self, *args, **options):
        ftp = self.connect_to_ftp(options)
        self.prepare_for_import()

        with open(options['csv'], newline='') as file:
            images = csv.DictReader(file)
            for row in images:
                path_to_file = self.import_image(ftp, row['filename'])
                self.create_image(row['item_id'], row['is_main'], row['filename'], path_to_file)
                
        ftp.quit()
        self.cleanup()
    
    def import_image(self, ftp, filename):
        path_to_image = self.TMP_DIR + filename

        with open(path_to_image, 'wb') as img:
            ftp.retrbinary('RETR ' + filename, img.write)

        return path_to_image

    def create_image(self, item_id, is_main, filename, path_to_file):
        self.stdout.write('Creating image: item_id=%s, filename=%s' % (item_id, filename))
        if Item.objects.filter(pk=item_id).exists():
            image = Image(item_id=item_id, is_main=bool(is_main))
            image.image.save(filename, File(open(path_to_file, 'rb')))
        else:
            self.stderr.write('Item not found: %s' % item_id)

    def connect_to_ftp(self, options):
        host = options['ftp_server']
        path = options['path']
        user = options['user']
        password = options['password']

        ftp = FTP_TLS(host=host)
        ftp.login(user=user, passwd=password)
        ftp.cwd(path)

        return ftp

    def prepare_for_import(self):
        Path(self.TMP_DIR).mkdir(parents=True, exist_ok=True)
        Image.objects.all().delete()

    def cleanup(self):
        rmtree(self.TMP_DIR)
