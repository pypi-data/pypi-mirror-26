# Spitobj

Fake data object initialization


## Description

I was wondering if I could replace
[FactoryBoy](https://github.com/FactoryBoy/factory_boy) with something much
simpler and still fulfill my needs..

Ladies 'n' Gents, introducing: `spitobj`


## Warning:
It's a rough experiment and you should be **crazy** to using it.

Apparently, I'm crazy enough because I use `spitobj` in one of my
closed-source, simple project.


## FAQ

> This project looks like a shit, how do I install it?

`pip install git+https://github.com/xliiv/spitobj`

> This project is a shit, how do I use it?

Like all shit project, there is no doc.
You could see tests to get the sample code, like:

* https://github.com/xliiv/spitobj/blob/master/tests.py#L46
* https://github.com/xliiv/spitobj/blob/master/tests_sqlalchemy.py#L38

## TODO future:
* better DX, including doc
* `faker` provider? (https://faker.readthedocs.io/en/stable/index.html)?
* more generators:
    * GlobalCounterGenerator?
    * CycleGenerator?
    * ..
