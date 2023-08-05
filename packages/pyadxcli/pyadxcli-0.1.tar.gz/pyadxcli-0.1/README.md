[![Build Status](https://travis-ci.org/audionamix/pyadxcli.svg?branch=master)](https://travis-ci.org/audionamix/pyadxcli)

# A Python client to Audionamix API

This a very simple client written in python to illustrate the documentation
found at http://developer.audionamix.com

## Install

```bash
python setup.py install
```

## Example

```python
from pyadxcli.client import Client

client = Client("myclientid", "myclientsecret")
source_url = client.upload_source_file("/path/to/source/file.wav")
pitch = client.track_pitch(source_url)
consonants = client.track_consonants(source_url)
vex = client.extract_vocals(source_url, consonants, pitch)
result = client.download(vex)
print(result)
```
