# READ ME

This repository contains implementation and utility code for Internet of Things Directory project.

## How to bootstrap the project

1. `git clone git@github.com:Riolu/IoT.git`
2. To run an application node (level1 node), execute `python -m IoT.level1.run`
3. To run the access-control server, execute `python -m IoT.access.run`

Sidenotes:

To initialize database at an application server, use `python -m IoT.level1.init_db`

To initialize database at access-control server, use `python -m IoT.access.init_db`

### Utils

We also provide util programs for using the system.

You can use `bash ./IoT/evaluation/init_master` and `bash ./IoT/evaluation/init_secondary` to initiate the application nodes on `nuc6` and `nuc7` respectively

#### Access-Control Util

In `IoT/access/util` folder, we provide util programs to generate RSA pairs, access tokens and RSA signatures.

Be sure to explore them if you would love to enable access control.

## A simple walk-through

```
    0(1) 
    |
    1(2)
    | 
    0(3)
  /   \
1(4)   1(4b)
|      |
0(5)   0(5b)
```

0: auc6
1: auc7

### Init

> Alita register publicKey

`curl -d '{"id": "alita", "password": "ppp", "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnnlzTo6qzhD4UHTAH+KY\nK6ZI/7uqIqMDlQE+ioLMWXUoy4XHe7NTruU8yTXgOHo1h/ObJ/quM6xIPBJlYevm\nnhkwsSuy2gifcYki9FmoyVcIJOR9IPEhivfwCCmTte4PRR4JGNvdqE5UJWSraqT3\n7AtdDDlBTeePtF6gIQppdW02Ju4cV5N2+OjFryLyUtOHOA0Q2vW7lrbPzhUxaNUc\nzqcDE+8BxtN5/kst8HcyKLRoMlrA+4L3s6SEEPQ4ku6qs9maKnC5dUhvuJIXTKEj\nqNPzfCOpK6D5mWZ5K2b70DzGP+3UWW3UWe4n8iWV99baUNnVKU4e8WXiF4YcUPDg\nEQIDAQAB\n-----END PUBLIC KEY-----"}' -H "Content-Type: application/json" -X POST http://localhost:4999/registerUserPublicKey`

> Brian register publicKey

`curl -d '{"id": "brian", "password": "bbb", "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwxyl4H99t6S0h8xPqunq\nX9RgKKsXTHzjeZ6T4Tf+xebbAXUveM3Ed3YFF2yHUF/H52m4ucG/CWbS4JieT750\noyIwGfEcWzklokXscdR2asPdEpLKQ/LHlt4sGAFS5ev8RBELT7M/rcVVU/YA9lgP\nhbsyTPVJ7TuedioLz78TTSEV2sEyh3Qae8iDUyevUdnGZBzR8/vFMosnkxYGGLLf\nOT9nFED3gcaal9gms2qSv92L4uDCQYHAxWxOs3UPDI9fLZPWErFhGKek1GQ4DGLv\nKp491OR63QdhpgFibdAn5WppglB8zMwZTyHuxXN4dBgfsukUP/PlefMw61RjbJbA\nywIDAQAB\n-----END PUBLIC KEY-----"}' -H "Content-Type: application/json" -X POST http://localhost:4999/registerUserPublicKey`

> Alita registers a public TV at level5, sets its publicity to be 1

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoicmVnaXN0ZXIiLCJwYXJhbXMiOnt9fX0.IwRe3PNlguXG9WraPJoW9pzOrxeuAhrcJUF7RgSBX3Q", "id": "alita", "signature": "luH1x+qIEPNOSoWAi+y70mnCF31qGvBZABn4Dww7xmuAkxqEaBdDdxo729zsQqmnXcIBvFCszjRgdfeOd1Wv5eelrFyafo0RqyJLLwtZNYpwjZjY4t1iKMUeojcXTlUiNeHKrBmlHKpVH9oPoBSM+cNHYGgwNI32I05no/ghtnossFnVdDmWetbB/viXW/x4sy+iAkM5O17SDENANxIfMFGZYFRD6GEnBQxEJI0PICcEKE3/Y/bnGbuhkrha6rPmF2Zyup3V5OUW2T7qeLfffvdnWuC5Dpu7WTKIanRXGWa8XVFNuFVz6N/tAKOFmYv8tZVjzwbOeXTUtn/JmEBU8A==", "operation": {"resource": "register", "method": "POST","params": {}, "data": {"td": {"_type": "tv", "id": "urn:dev:ops:23112-tv-1", "publicity": 1}, "targetLoc": "level5"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> Alita registers a private PC at level5

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoicmVnaXN0ZXIiLCJwYXJhbXMiOnt9fX0.IwRe3PNlguXG9WraPJoW9pzOrxeuAhrcJUF7RgSBX3Q", "id": "alita", "signature": "Xh+nwE/0g2w+aO6vFk0NvnKHaTlujAiFJSR5JfPDV7B43eExCPv9AS59W+7D/4I8utyAYCIds4LmHUJi2QrrQhK0XmmtLqVGFv4M7JYMEpuNi4VzoaBf5VXItTfQZT1OklHE/rUUki4sjjwYiiOOAsKq4nK+se5tzlYb8CDSCSRZ/eRz1ovHZHnEDG4ubxK1Nfwwc8ZFbxaWELAg7Q3OE8vRp/mJ+pIMJEdjFovRgtplDg651U9qXIMEgssF5yjIhxeoCGNWqn0/wfQOsMohbH0qbbfSOm9Ph3jhX1BGS6CXtwtrWwvadlUC4zejZRLcI8T8rehKm4lMtjdNcma91A==", "operation": {"resource": "register", "method": "POST","params": {}, "data": {"td": {"_type": "pc", "id": "urn:dev:ops:23221-pc-10"}, "targetLoc": "level5"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> Alita searches this PC with its location and type

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoic2VhcmNoQnlMb2NUeXBlIiwicGFyYW1zIjp7ImxvYyI6IioiLCJ0eXBlIjoiKiJ9fX0.osbVry6je6fVbwivRGxoEbjvmBPXNe0mAVIY_a-SuNM", "id": "alita", "signature": "TEH9apqDGqLpAKP9MQJI8jjvZI0nAxWJe2KwXSt607kpcWYvuobgNsN1NhEbsGdHzx8TGpO+SIOIcKrRdbxRR+KFfceMBaoRiBeSzpEtpSQNtQFM5hQ7PtrAHsl/JrNcu8G2EMLuQEaHNcqpNJCqktX614ScIMIwGGV7sCtm5x9GQk2FL/gCz67OiXsfKqCzRjNOohvMnRIOkQe6JwL3s3YxId1wPxdyPWpPHcIRFqDffsPmts9vWA99cPC0+esTWf9IFxCzQ0DD4hUdsPWnsfiUVl5bF/3/ohb9ht4zrlL+CCr8nP50IiVAOh7VEUiwzr3a9ywuZpQESUgSMrGk8w==", "operation": {"resource": "searchByLocType", "method": "GET", "params": {"loc": "level5", "type": "tv"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> Alita searches the the public TV at level 4

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoic2VhcmNoUHVibGljIiwicGFyYW1zIjp7ImxvYyI6IioifX19.jbBcvuPqXT2knY9iSrOpH9dl0XMGwXM7pKpSOtPnbU4", "id": "alita", "signature": "eqQ2VAm8Ybv5K44N8bNWoHlu2YPIMA9vFaYriYX0dYDnac6hYfAPicO8KDKMffChFT7dKTJ5GgVIjpjeQaCfyc4SJEHRa48AN4SIJstMK+w0gY2XhUvLCZrsgIhEJmza4uRvPZmMDFKApaq3qPd/PldG7TB2A2CGQQCFLeOzCR6MBt8S/hzRzVp0s52wW8H78e+LA9m786RVZLig17GXuLTukimCZkmK4EADGjhjM0KgwDnOeYJxxm63+thmRiNXfxieUKzgaSQy/tIE6shzJPeBAlVyx0ahXvZIoJRXFURbOAcSbvcblgkY3gJQLEdUdsCqLHRqzZ5Bv09JjIyfpg==", "operation": {"resource": "searchPublic", "method": "GET", "params": {"loc": "level4"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> Alita searches the TV by its loccation and ID

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoic2VhcmNoQnlMb2NJZCIsInBhcmFtcyI6eyJsb2MiOiIqIiwiaWQiOiIqIn19fQ.XM-8f5RBBrlbi3-ILtrlhseTXCMrJNaI3rT_m6HO068", "id": "alita", "signature": "YNqFxmaVNnf4QQCG+Y54uEsPT1BNWs+Spui8iMUilgAEkYrV0YL+tkX0XbTKbJ5tfM/Tw5oEfOmDX6eE1kXYdjtV38V1imEC7YQsyYlcLOo+fJ0fRlrrEA7UCdg0saFv7y4IN/8sK8LqA4Cj+B13ODuJsq3WnCb126yau0Po+TUGZzjSY5RoClnhOjtQPI4W1MZmJMRjkUdsGkkbFhvZisTejD81G87Kah72r0/K6ShPazhSpi7v/ZTECHNENmJ1brCH68imICkUbTJMHncM0fSFFs1I8IMAtX43klr5Mmv30oGnp7GwRiK6z5ajA4AegtmmcJQwAOnuXVji0IM6EQ==", "operation": {"resource": "searchByLocId", "method": "GET", "params": {"loc": "level5", "id": "urn:dev:ops:23112-tv-1"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> Alita relocates the TV from level5 to level5b

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoicmVsb2NhdGUiLCJwYXJhbXMiOnsiZnJvbUxvYyI6IioiLCJ0b0xvYyI6IioiLCJpZCI6IioifX19.RB0poW_Ok91X6G9bdJN9Pv23YcUEvBahrPFsOhGxoNQ", "id": "alita", "signature": "dvmllwIg6wu9oIoRf/woNU5uVLcnEy/Uhgnn4LI+NmXqHGZ5VHBWe1pxwc3UY5VY1/Ve556xNNau4h2BDmG0k0KIdgiarujoWUE+2T5i852LpO1w3aCxS2wPBx7rw14AWjnokFMUfDbJ+Nag9ja7Uy2as9ulX6dZ4n2MkYv5xcLAsGSEYpu/IYxQFmlHA0tpUy+GMAsc9sqCMEYKWouD+Hl351v0hXs5RVNWTJfHaWgTrzo3VbKlZS3LU/j1zZQBh4bCx14TagmFgJZFrVjLIETUsT/QljTVWfIKzFFc8AaEVjjwGJisF8BB3isL4eQVGInTJrCYPXle0Z7GReJTiQ==", "operation": {"resource": "relocate", "method": "PUT", "params": {"fromLoc": "level5", "toLoc": "level5b", "id": "urn:dev:ops:23112-tv-1"}, "data":{}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> Alita searchPublic at level4, no tv anymore

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoic2VhcmNoUHVibGljIiwicGFyYW1zIjp7ImxvYyI6IioifX19.jbBcvuPqXT2knY9iSrOpH9dl0XMGwXM7pKpSOtPnbU4", "id": "alita", "signature": "eqQ2VAm8Ybv5K44N8bNWoHlu2YPIMA9vFaYriYX0dYDnac6hYfAPicO8KDKMffChFT7dKTJ5GgVIjpjeQaCfyc4SJEHRa48AN4SIJstMK+w0gY2XhUvLCZrsgIhEJmza4uRvPZmMDFKApaq3qPd/PldG7TB2A2CGQQCFLeOzCR6MBt8S/hzRzVp0s52wW8H78e+LA9m786RVZLig17GXuLTukimCZkmK4EADGjhjM0KgwDnOeYJxxm63+thmRiNXfxieUKzgaSQy/tIE6shzJPeBAlVyx0ahXvZIoJRXFURbOAcSbvcblgkY3gJQLEdUdsCqLHRqzZ5Bv09JjIyfpg==", "operation": {"resource": "searchPublic", "method": "GET", "params": {"loc": "level4"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> alita searchPublic at level4b, find the tv

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoic2VhcmNoUHVibGljIiwicGFyYW1zIjp7ImxvYyI6IioifX19.jbBcvuPqXT2knY9iSrOpH9dl0XMGwXM7pKpSOtPnbU4", "id": "alita", "signature": "IYZLfULgXKeUDqBfh/9spJG6FO+seJl/E92Flh+nOy9q9hPmOukgA9z2tnnAgD3QpYs/HBe+83lhmgTLDLaERm5Ni0Gic2T8G7XG5sXOGfIKXzovLEups+pdai1C8jeah3x/nC2mTnlms6M4HzyT+YgAN5NtnwovH5O2FfRfdOGu3gogkxfglo5SzuzM4xcRD3mzLHmWQ82ZLnGvyFKPxdaxiP+4Hgoh0iGdWZZHoOhvrDI/Zr8aTGbjv786yavnFbPRxi5CvATrdQmRkPAHgCUy/xLZ7gRNacHrj0A7o1RfJ6a4KhnTFPIkexbyfjvXOGbj9TZfMRM1lHIUf8EK5w==", "operation": {"resource": "searchPublic", "method": "GET", "params": {"loc": "level4b"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> alita delete tv from level5b

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoiZGVsZXRlIiwicGFyYW1zIjp7InRhcmdldExvYyI6IioiLCJpZCI6IioifX19._mdKwKECUwcojjbAVRhW4RbO9nB1F1H_mCIPNjLucKs", "id": "alita", "signature": "XteeBd7VZHPEKtnG+Q8Ng69ppNcb0/dYNXsbXkgk3IQ5NI8Y+oBd6rl8cbv1mcNF19i3GKeW9bylkuzv7u2S/gf4atmcFbJXWQ9X3ojnoUXzunXMYa4HscDjfDZ+bEBUXCBj7mfLV+1bshOiqeu9XilcGuuVhxx0fxEQ9B6EMBGlUXHQ5sZCAEdkzfQ5lPQqWt2pwwS151aeIIMDhwnNX27M2EyCsKDX2kkffJzstjY1Qjy+r/wzYD9QAGMA3kwLrtJpLMlt7rHp35TwsSPMYOrotjQ0nvK27+o2VzwSISnXsFRdPlZp5uvf/TpVEp/FyrZQNrYZ+XC2HE55hCPT+g==", "operation": {"resource": "delete", "method": "DELETE", "params": {"targetLoc": "level5b", "id": "urn:dev:ops:23112-tv-1"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> alita searchPublic at level4b, should find nothing

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoic2VhcmNoUHVibGljIiwicGFyYW1zIjp7ImxvYyI6IioifX19.jbBcvuPqXT2knY9iSrOpH9dl0XMGwXM7pKpSOtPnbU4", "id": "alita", "signature": "IYZLfULgXKeUDqBfh/9spJG6FO+seJl/E92Flh+nOy9q9hPmOukgA9z2tnnAgD3QpYs/HBe+83lhmgTLDLaERm5Ni0Gic2T8G7XG5sXOGfIKXzovLEups+pdai1C8jeah3x/nC2mTnlms6M4HzyT+YgAN5NtnwovH5O2FfRfdOGu3gogkxfglo5SzuzM4xcRD3mzLHmWQ82ZLnGvyFKPxdaxiP+4Hgoh0iGdWZZHoOhvrDI/Zr8aTGbjv786yavnFbPRxi5CvATrdQmRkPAHgCUy/xLZ7gRNacHrj0A7o1RfJ6a4KhnTFPIkexbyfjvXOGbj9TZfMRM1lHIUf8EK5w==", "operation": {"resource": "searchPublic", "method": "GET", "params": {"loc": "level4b"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`



> alita delegates her token for searchByLocType to brian

`curl -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSJdLCJwZXJtaXNzaW9uIjp7InJlc291cmNlIjoic2VhcmNoQnlMb2NUeXBlIiwicGFyYW1zIjp7ImxvYyI6IioiLCJ0eXBlIjoiKiJ9fX0.osbVry6je6fVbwivRGxoEbjvmBPXNe0mAVIY_a-SuNM", "childID": "brian", "id": "alita", "signature": "VakJMUxoRpi+H3o+0X4Gg7Z3LwvoYZDZgKbiSWUqfl0bdnA5J9XAs7Rw0p4YmW81GutD6uBiFpTOMq3H18DDMcqooLAnFUrjsqOUkx9ZTsvl4YyKQ1uuBSEP9TAjJeHdY151bffBG8Aa6JHWtvNswwW+MOUwX6s+ytO9eoJORnOj6RmIrz1D6JObabVM29axivM4RsZuxbhKxe/wb9ZQKWGECXG6ewGzAMlb4Dtm6enRvUzKi0MJrjmRwxQtJrR46e3fLvi9aiH50jlbM+5UoneF0IyALbQQwRulj8rs0NPq11LIBzKBd6DQF5A+TjWN1x6pw/lV0Nq7Q2bu7kDj/w=="}' -H "Content-Type: application/json" -X POST http://localhost:4999/delegate`

> brian uses the token delegated by alita to searchByLocType

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSIsImJyaWFuIl0sInBlcm1pc3Npb24iOnsicmVzb3VyY2UiOiJzZWFyY2hCeUxvY1R5cGUiLCJwYXJhbXMiOnsibG9jIjoiKiIsInR5cGUiOiIqIn19fQ.lJqQJgK_dwrWgbI660OvyAuQ0LaV6IG2QS3mp4P1L5s", "id": "brian", "signature": "CAxcO0y615/dy2LDcmz4u17V/3LRi6XFSpVQnmWwWCIHsadsKM6+Txrfqpap400qgtA2G/lOHjnv8eEGlGe5vrx8ystBWGX1IE/oE6ECqw0j9P9L51R4dfTHYSr1acExuPfrkff7k+2UPkLLfpkS3ITDwz2oOii9udCTO2blQa6H5HHiNburz8InqAQ2qPlAwajEuCFcW+7yuEjoyMh0CYbmV3GGOcBFPL+SlTsuMTZDMeJTqnQXq9U0FPfp1BjaI2C/qSLioqUzeu2v6wu5qdnZooRW/1DtO8SRQ2V/h5u2rFI2gf03M1d9hdJBG9p8+I+Aib0n+IM4iIi5tQn2EA==", "operation": {"resource": "searchByLocType", "method": "GET", "params": {"loc": "level5", "type": "pc"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`

> alita revokes brian's token

`curl -d '{"id": "alita", "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyJhbGl0YSIsImJyaWFuIl0sInBlcm1pc3Npb24iOnsicmVzb3VyY2UiOiJzZWFyY2hCeUxvY1R5cGUiLCJwYXJhbXMiOnsibG9jIjoiKiIsInR5cGUiOiIqIn19fQ.lJqQJgK_dwrWgbI660OvyAuQ0LaV6IG2QS3mp4P1L5s", "signature": "B1STPd66IaBMCyvlat+dd/WF2mAXNf4ARubA4ht24k1ScAzJeTHfoU/72+SwXUKvePSiy1ziPjKR8U/6tsWGizBa50AyrLy5DQW4mG7rMAdpObewCTjr8g/azl6NsjjHpr30x9025r7DszrH5wBlXGS/AW0Sl4sSx2whBMRvdFvbiezqxu2xEMDw4riQhZiM2hTosbpWn/fFFyXK25u4NmYXqDsdw2Fpi+BdI9oNzEShf40/sF60XH5aGNPuvW2/L0FC1tEn7KbttYQoWez3fWTPvlx7A3GYca9mmuJyVLOve8YwKwrbPwOPjJwDu4QXkuHtKyjPoA73DPeArP8mVw=="}' -H "Content-Type: application/json" -X POST http://localhost:4999/revoke`

> brian attempts to use the revoked token delegated by alita to searchByLocType

`curl -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.**eyJpZCI6WyJhbGl0YSIsImJyaWFuIl0sInBlcm1pc3Npb24iOnsicmVzb3VyY2UiOiJzZWFyY2hCeUxvY1R5cGUiLCJwYXJhbXMiOnsibG9jIjoiKiIsInR5cGUiOiIqIn19fQ**.lJqQJgK_dwrWgbI660OvyAuQ0LaV6IG2QS3mp4P1L5s", "id": "brian", "signature": "'CAxcO0y615/dy2LDcmz4u17V/3LRi6XFSpVQnmWwWCIHsadsKM6+Txrfqpap400qgtA2G/lOHjnv8eEGlGe5vrx8ystBWGX1IE/oE6ECqw0j9P9L51R4dfTHYSr1acExuPfrkff7k+2UPkLLfpkS3ITDwz2oOii9udCTO2blQa6H5HHiNburz8InqAQ2qPlAwajEuCFcW+7yuEjoyMh0CYbmV3GGOcBFPL+SlTsuMTZDMeJTqnQXq9U0FPfp1BjaI2C/qSLioqUzeu2v6wu5qdnZooRW/1DtO8SRQ2V/h5u2rFI2gf03M1d9hdJBG9p8+I+Aib0n+IM4iIi5tQn2EA=='", "operation": {"resource": "searchByLocType", "method": "GET", "params": {"loc": "level5", "type": "pc"}}}' -H "Content-Type: application/json" -X POST http://localhost:4999/operate`
