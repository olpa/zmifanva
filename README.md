# zmifanva - Lojban ↔ English Machine Translation Engine

# Run

## Run the web application

```
# No need to download if you have cloned the repository
wget https://raw.githubusercontent.com/olpa/zmifanva/master/docker-compose.yaml

docker-compose up

xdg-open http://localhost:6543
```

Zmivanfa works on the port 6543. Open the start page in your browser: <http://localhost:6543>.

## Run the translator in the command line

```
# For Lojban to English
docker run -it --rm olpa/moses-zf-jb-en
# For English to Lojban
docker run -it --rm olpa/moses-zf-en-jb
```

Write a sentence, press ENTER. Find a translation among output.

You should tokenize the input. Instead of writing "Hello, world!" write "hello , world !"

## Run the translator over XML-RPC

On example of Lojban to English. Start the container as an xmlrpc server:

```
ZFDIR=jb-en
docker run -it --rm -p 8080:8080 \
  olpa/moses-zf-$ZFDIR \
  /opt/moses/bin/moses --server --server-port 8080 \
    -f /zmifanva/moses_model/$ZFDIR/moses.ini
```

Create `x.xml` with a payload for an xmlrpc request:

```
<?xml version="1.0"?>
<methodCall>
  <methodName>translate</methodName>
  <params>
    <param>
      <value>
        <struct>
          <member>
            <name>text</name>
            <value>
              <string>coi ro do</string>
            </value>
          </member>
          <member>
            <name>align</name>
            <value>
              <string>false</string>
            </value>
          </member>
          <member>
            <name>report-all-factors</name>
            <value>
              <string>false</string>
            </value>
          </member>
        </struct>
      </value>
    </param>
  </params>
</methodCall>
```

Make a call:

```
curl -d @x.xml http://localhost:8080/RPC2
```

Get the result:

```
<?xml version="1.0" encoding="UTF-8"?>
<methodResponse>
<params>
<param><value><struct>
<member><name>text</name>
<value><string>Hello , everyone ! </string></value></member>
</struct></value></param>
</params>
</methodResponse>
```

# Develop

Moses models: [./moses_model/scripts/README.md](./moses_model/scripts/README.md).

Web application: [./web/README.md](./web/README.md).

# Notes

Developed by Masato Hagiwara: <https://github.com/mhagiwara/zmifanva>, forked at <https://github.com/olpa/zmifanva/>.

The project contains the directory `seq2seq` for neural translation. Not investigated.
