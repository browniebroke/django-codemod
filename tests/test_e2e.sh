#!/usr/bin/env bash

set -xu

mkdir -p e2e
cd e2e
django-admin startproject djcme2e
cd djcme2e
django-admin startapp app1

echo "from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


class AppModel(models.Model):
    name = models.CharField(_('Name'))
    slug = models.SlugField(_('Name'))

    def __str__(self):
        return force_text(self.name)
" > app1/models.py

cp -r ../djcme2e ../djcme2e_orig

djcodemod run --deprecated-in 3.0 .

cd ..

OUT=$(diff -qr djcme2e_orig/ djcme2e/ | grep -v 'models.py differ')

if [ "${OUT}" != "" ]
then
    echo "ERROR: unexpected differences found:"
    diff -r djcme2e_orig/ djcme2e/
    exit 1
else
    exit 0
fi
