## Albums

Can look like

```
04 Blueprints.mp3
08. End of the World.mp3
```

## Metadata

Should take priority.

```python
In [33]: MP3("01 Hollow.mp3").keys()
Out[33]: dict_keys(['TALB', 'TPE1', 'TPE2', 'COMM::eng', 'TPOS', 'TCON', 'TIT2', 'TRCK', 'APIC:', 'COMM:ID3v1 Comment:eng', 'TDRC'])

In [34]: MP3("01 Hollow.mp3").get("TIT2")
Out[34]: TIT2(encoding=<Encoding.UTF16: 1>, text=['Hollow'])

In [35]: MP3("01 Hollow.mp3").get("TRCK")
Out[35]: TRCK(encoding=<Encoding.LATIN1: 0>, text=['1/11'])

In [36]: MP3("01 Hollow.mp3").get("TALB")
Out[36]: TALB(encoding=<Encoding.UTF16: 1>, text=['Blueprints'])

In [37]: MP3("01 Hollow.mp3").get("TPE1")
Out[37]: TPE1(encoding=<Encoding.UTF16: 1>, text=['Wage War'])

In [38]: MP3("01 Hollow.mp3").get("TPE2")
Out[38]: TPE2(encoding=<Encoding.UTF16: 1>, text=['Wage War'])

In [39]: MP3("01 Hollow.mp3").get("TPOS")
Out[39]: TPOS(encoding=<Encoding.LATIN1: 0>, text=['1/1'])

In [40]: MP3("01 Hollow.mp3").get("TCON")
Out[40]: TCON(encoding=<Encoding.UTF16: 1>, text=['Metalcore'])
```

- Based on metadata, Sort by Genre, if no genre do Misc/Other

But it seems like there are differences

```python
In [51]: mutagen.File("01\ Trapt\ -\ Headstrong.flac".replace('\\', ''))
Out[51]: {'albumartist': ['Trapt'], 'disctotal': ['1'], 'releasetype': ['album'], 'title': ['Headstrong'], 'musicbrainz_trackid': ['240ce563-437b-41aa-901e-3067735c770c'], 'musicbrainz_releasegroupid': ['bb59668a-49f4-31ea-8260-d101ddcc445f'], 'releasestatus': ['official'], 'label': ['Warner Bros. Records'], 'totaltracks': ['11'], 'discnumber': ['1'], 'musicbrainz_albumid': ['a3482d25-5f1f-4154-b766-a05d6ffd2d10'], 'date': ['2002-11-05'], 'totaldiscs': ['1'], 'media': ['CD'], 'musicbrainz_artistid': ['8876c0be-ccff-4d46-aa91-7f935a3b3b6b'], 'originaldate': ['2002-11-05'], 'releasecountry': ['US'], 'musicbrainz_albumtype': ['album'], 'genre': ['Alternative Metal', 'Grunge', 'Hard Rock', 'Heavy Metal', 'Metal', 'Pop Rock', 'Post-Grunge', 'Post-Rock', 'Rock'], 'musicbrainz_releasetrackid': ['cd11ab30-cce5-3fab-a1d9-7124111356e3'], 'musicbrainz_albumartistid': ['8876c0be-ccff-4d46-aa91-7f935a3b3b6b'], 'originalyear': ['2002'], 'artist': ['Trapt'], 'musicbrainz_albumstatus': ['official'], 'album': ['Trapt'], 'tracktotal': ['11'], 'tracknumber': ['1']}
```

For an m4a file

```python
In [56]: mutagen.File("Rabbit\ Junk\ -\ 01\ -\ Born\ and\ Bled.m4a".replace('\\', '')).keys()
Out[56]: dict_keys(['©nam', '©ART', 'aART', '©alb', '©gen', 'trkn', 'disk', '©day', '----:com.apple.iTunes:ORGANIZATION', '----:com.apple.iTunes:ALBUM ARTIST', 'covr', '©too'])
```

Another flac example

```python
In [61]: mutagen.File("20 Shinedown - I Dare You (Clear Channel Stripped).flac".replace('\\', '')).keys()
Out[61]:
['albumartist',
 'disctotal',
 'releasetype',
 'title',
 'musicbrainz_trackid',
 'musicbrainz_releasegroupid',
 'releasestatus',
 'totaltracks',
 'discnumber',
 'musicbrainz_albumid',
 'date',
 'totaldiscs',
 'media',
 'musicbrainz_artistid',
 'originaldate',
 'musicbrainz_albumtype',
 'genre',
 'musicbrainz_releasetrackid',
 'musicbrainz_albumartistid',
 'originalyear',
 'artist',
 'musicbrainz_albumstatus',
 'album',
 'tracktotal',
 'tracknumber']
```
