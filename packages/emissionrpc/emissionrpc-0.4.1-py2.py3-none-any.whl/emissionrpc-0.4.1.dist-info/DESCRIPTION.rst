EmissionRPC
===========

.. image:: https://badge.fury.io/py/emissionrpc.svg
    :target: https://badge.fury.io/py/emissionrpc

.. image:: https://img.shields.io/pypi/pyversions/emissionrpc.svg
    :target: emissionrpc

EmissionRPC, a (Yet Another) Python wrapper JSON-RPC to `Transmission <http://transmissionbt.com/>`_ BitTorrent client.

See the `RPC interface <https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt>`_ .

Prerequisites
-------------

python 2.7 and 3.6


How to install
--------------

.. code-block:: bash

    $ pip install emissionrpc

Usage
-----

.. code-block:: python3

    import emissionrpc

    emitter = emissionrpc.Client()

    # Get the torrent's list
    emitter.list_torrent()

    # Adding a torrent (the torrent is not started)
    emitter.add_torrent('http://urltorrent.torrent')

    # To start all the torrents
    emitter.start()

    # To start a specific torrent (pass the id to the client)
    emitter.start(1)

    # To delete a torrent (pass the id to the client)
    emitter.delete(3)



