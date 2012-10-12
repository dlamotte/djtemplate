#!/bin/sh

trap 'echo "caught error: exiting..."; exit 1' ERR

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

# remove tarball top-level dir from github
mv *-*-*/* .
rmdir *-*-*

echo "% virtualenv env"
virtualenv env
source env/bin/activate

echo "% pip install -e ."
pip install -e .

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
rm -f setup.sh

echo "% ./manage.py syncdb --all"
./manage.py syncdb --all

echo "% ./manage.py migrate --fake"
./manage.py migrate --fake

echo ""
echo "Enter virtual environment with:"
echo source env/bin/activate
