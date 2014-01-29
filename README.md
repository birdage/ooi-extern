ooi-extern
==========

## macosx

install postgres to a virtual env named "postgres"
pull down this repo and run bootstrap.py and bin/buildout to develope the eggs needed.

git submodule update --init

multicorn

virtenv

### 


### postgres data store

../geonode/geoserver/data/workspaces/geonode

kinda looks like this

```
<dataStore>
  <id>DataStoreInfoImpl-1557c66f:143d5325248:-7ffe</id>
  <name>asd</name>
  <description>asd</description>
  <type>PostGIS</type>
  <enabled>true</enabled>
  <workspace>
    <id>WorkspaceInfoImpl-78ff667e:12476299803:-7ffd</id>
  </workspace>
  <connectionParameters>
    <entry key="port">5432</entry>
    <entry key="Connection timeout">20</entry>
    <entry key="dbtype">postgis</entry>
    <entry key="host">localhost</entry>
    <entry key="validate connections">true</entry>
    <entry key="encode functions">false</entry>
    <entry key="max connections">10</entry>
    <entry key="database">postgres</entry>
    <entry key="namespace">http://www.geonode.org/</entry>
    <entry key="schema">public</entry>
    <entry key="Loose bbox">true</entry>
    <entry key="Expose primary keys">false</entry>
    <entry key="Session startup SQL">select runCovTest();</entry>
    <entry key="fetch size">1000</entry>
    <entry key="Max open prepared statements">50</entry>
    <entry key="preparedStatements">false</entry>
    <entry key="Estimated extends">true</entry>
    <entry key="user">rpsdev</entry>
    <entry key="min connections">1</entry>
  </connectionParameters>
  <__default>false</__default>
</dataStore>
```

## centos 6.3 install (tested as a VM)

```
sudo yum -y update
```

```
vi /etc/sysconfig/selinux
```
Set 
```
SELINUX=disabled
```

sudo reboot

```
sudo vi /etc/sysconfig/iptables
```
Add the following lines:
```
-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 5432 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8000 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8080 -j ACCEPT
```

```
sudo service iptables restart
```

Install Python 2.7.3
```
yum -y groupinstall "Development tools"
yum -y install zlib-devel
yum -y install bzip2-devel
yum -y install openssl-devel
yum -y install ncurses-devel
```





