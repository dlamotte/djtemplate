#!/bin/sh

URL="https://github.com/dlamotte/djtemplate/tarball/master"

projectname="$1"

if [[ -z $projectname ]]; then
    echo "no project name, giving up..."
    exit 1
fi

echo "% django-admin.py startproject --template=\"$URL\" \"$projectname\""
django-admin.py startproject --template="$URL" "$projectname"

echo "% cd $projectname"
cd $projectname

mv *-*-*/* .
rmdir *-*-*

echo "% virtualenv env"
virtualenv env

echo "% pip -E env install -e ."
pip -E env install -e .

echo "% psql -c \"create database $projectname;\""
psql -c "create database $projectname;"

cat <<EOF > .gitignore
/env/
/$projectname/media/
/settings_local.py
/*.egg-info/
EOF

echo "% git init"
git init

chmod u+x ./manage.py ./setup.py
mv Procfile.py Procfile

echo ""
echo "You still need to do the following:"
echo source env/bin/activate
echo ./manage.py syncdb
echo ./manage.py runserver

rm -f setup.sh
