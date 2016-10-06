#! /bin/bash

cp luke-client.py luke-client.ser.service /tmp/

#get and unpack the image
wget -o /tmp/initrd.img http://magic-address/images/pxeboot/initrd.img
mkdir /tmp/init
cd /tmp/init
xz -dc ../initrd.img | cpio --quiet -i --make-directories

#insert the script
mv /tmp/luke-client.py usr/bin/
chmod +x usr/bin/luke-client.py

#insert the srevice
mv /tmp/luke-client.service usr/lib/systemd/system
ln -s /usr/lib/systemd/system/luke-client.service etc/systemd/system/sysinit.target.wants/luke-client.service

#insert dependencies
cd /usr/lib/python2.7/site-packages
tar -cf - requests urllib3 backports chardet idna six.py | (cd /tmp/init/usr/lib/python2.7/site-packages ; tar -xf -)
cp /usr/lib64/python2.7/{cgi,platform,Queue,Coockie,stringprep,re}.py /tmp/init/usr/lib64/python2.7
cp -R /usr/lib64/python2.7/json /tmp/init/usr/lib64/python2.7
cp /usr/lib64/python2.7/lib-dynload/unicodedata.so /tmp/init/usr/lib64/python2.7/lib-dynload/unicodedata.so

#repack
cd /tmp/init
find . 2> /dev/null | cpio --quiet -c -o | xz -9 --format=lzma > /tmp/luke.img
