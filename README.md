microdata
=========

[![Build Status](https://github.com/edsu/microdata/actions/workflows/ci.yml/badge.svg)](https://github.com/edsu/microdata/actions/workflows/ci.yml)
 
microdata.py is a small utility library for extracting [HTML5
Microdata](http://dev.w3.org/html5/md/) from HTML. It depends on
[html5lib](http://code.google.com/p/html5lib/) to do the heavy lifting of
building the DOM. For more about HTML5 Microdata check out Mark Pilgrim's
[chapter](http://diveintohtml5.org/extensibility.html) on on it in [Dive Into
HTML5](http://diveintohtml5.org/).

Command Line
------------

When you install microdata via pip it will also install a command line utility: 

```
$ microdata https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=dQw4w9WgXcQ
{
  "items": [
    {
      "type": [
        "http://schema.org/VideoObject"
      ],
      "properties": {
        "url": [
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        ],
        "name": [
          "Rick Astley - Never Gonna Give You Up (Official Music Video)"
        ],
        "description": [
          "The official video for \u00e2\u20ac\u0153Never Gonna Give You Up\u00e2\u20ac\ufffd by Rick Astley \u00e2\u20ac\u0153Never Gonna Give You Up\u00e2\u20ac\ufffd was a global smash on its release in July 1987, topping the charts ..."
        ],
        "paid": [
          "False"
        ],
        "channelId": [
          "UCuAXFkgsw1L7xaCfnd5JJOw"
        ],
        "videoId": [
          "dQw4w9WgXcQ"
        ],
        "duration": [
          "PT3M33S"
        ],
        "unlisted": [
          "False"
        ],
        "author": [
          {
            "type": [
              "http://schema.org/Person"
            ],
            "properties": {
              "url": [
                "http://www.youtube.com/channel/UCuAXFkgsw1L7xaCfnd5JJOw"
              ],
              "name": [
                ""
              ]
            }
          }
        ],
        "thumbnailUrl": [
          "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
        ],
        "thumbnail": [
          {
            "type": [
              "http://schema.org/ImageObject"
            ],
            "properties": {
              "url": [
                "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
              ],
              "width": [
                "1280"
              ],
              "height": [
                "720"
              ]
            }
          }
        ],
        "embedUrl": [
          "https://www.youtube.com/embed/dQw4w9WgXcQ"
        ],
        "playerType": [
          "HTML5 Flash"
        ],
        "width": [
          "1280"
        ],
        "height": [
          "720"
        ],
        "isFamilyFriendly": [
          "true"
        ],
        "regionsAllowed": [
          "AD,AE,AF,AG,AI,AL,AM,AO,AQ,AR,AS,AT,AU,AW,AX,AZ,BA,BB,BD,BE,BF,BG,BH,BI,BJ,BL,BM,BN,BO,BQ,BR,BS,BT,BV,BW,BY,BZ,CA,CC,CD,CF,CG,CH,CI,CK,CL,CM,CN,CO,CR,CU,CV,CW,CX,CY,CZ,DE,DJ,DK,DM,DO,DZ,EC,EE,EG,EH,ER,ES,ET,FI,FJ,FK,FM,FO,FR,GA,GB,GD,GE,GF,GG,GH,GI,GL,GM,GN,GP,GQ,GR,GS,GT,GU,GW,GY,HK,HM,HN,HR,HT,HU,ID,IE,IL,IM,IN,IO,IQ,IR,IS,IT,JE,JM,JO,JP,KE,KG,KH,KI,KM,KN,KP,KR,KW,KY,KZ,LA,LB,LC,LI,LK,LR,LS,LT,LU,LV,LY,MA,MC,MD,ME,MF,MG,MH,MK,ML,MM,MN,MO,MP,MQ,MR,MS,MT,MU,MV,MW,MX,MY,MZ,NA,NC,NE,NF,NG,NI,NL,NO,NP,NR,NU,NZ,OM,PA,PE,PF,PG,PH,PK,PL,PM,PN,PR,PS,PT,PW,PY,QA,RE,RO,RS,RU,RW,SA,SB,SC,SD,SE,SG,SH,SI,SJ,SK,SL,SM,SN,SO,SR,SS,ST,SV,SX,SY,SZ,TC,TD,TF,TG,TH,TJ,TK,TL,TM,TN,TO,TR,TT,TV,TW,TZ,UA,UG,UM,US,UY,UZ,VA,VC,VE,VG,VI,VN,VU,WF,WS,YE,YT,ZA,ZM,ZW"
        ],
        "interactionCount": [
          "1141688870"
        ],
        "datePublished": [
          "2009-10-24"
        ],
        "uploadDate": [
          "2009-10-24"
        ],
        "genre": [
          "Music"
        ]
      }
    }
  ]
}
```


Library
-------

Here's the basic usage from Python using https://raw.github.com/edsu/microdata/master/test-data/example.html as an example:

```python
>>> import microdata
>>> import urllib
>>> url = "https://raw.github.com/edsu/microdata/master/test-data/example.html"
>>> items = microdata.get_items(urllib.urlopen(url))
>>> item = items[0]
>>> item.itemtype
[http://schema.org/Person]
>>> item.name
u"Jane Doe"
>>> item.colleagues
u"http://www.xyz.edu/students/alicejones.html"
>>> item.get_all('colleagues')
[u"http://www.xyz.edu/students/alicejones.html", u"http://www.xyz.edu/students/bobsmith.html"]
>>> print item.json()
{
  "type": [
    "http://schema.org/Person"
  ],
  "id": "http://www.xyz.edu/~jane",
  "properties": {
    "colleagues": [
      "http://www.xyz.edu/students/alicejones.html",
      "http://www.xyz.edu/students/bobsmith.html"
    ],
    "name": [
      "Jane Doe"
    ],
    "url": [
      "http://www.janedoe.com"
    ],
    "jobTitle": [
      "Professor"
    ],
    "image": [
      "janedoe.jpg"
    ],
    "telephone": [
      "(425) 123-4567"
    ],
    "address": [
      {
        "type": [
          "http://schema.org/PostalAddress"
        ],
        "properties": {
          "addressLocality": [
            "Seattle"
          ],
          "addressRegion": [
            "WA"
          ],
          "streetAddress": [
            "\n          20341 Whitworth Institute\n          405 N. Whitworth\n        "
          ],
          "postalCode": [
            "98052"
          ]
        }
      }
    ],
    "email": [
      "mailto:jane-doe@xyz.edu"
    ]
  }
}
```

License
-------

* CC0
