The Things Network Python SDK
=============================

|Build Status|

.. figure:: https://thethings.blob.core.windows.net/ttn/logo.svg
   :alt: The Things Network

   The Things Network

Table of Contents
-----------------

-  `Description <#description>`__
-  `MQTTClient <#mqttclient>`__
-  `connect <#connect>`__
-  `disconnect <#disconnect>`__
-  `start <#start>`__
-  `startBackground <#startbackground>`__
-  `stopBackground <#stopbackground>`__
-  `setUplinkCallback <#setuplinkcallback>`__
-  `uplinkCallback <#uplinkcallback>`__
-  `setConnectBehavior <#setconnectbehavior>`__
-  `setPublishCallback <#setpublishcallback>`__
-  `publishCallback <#publishcallback>`__
-  `Publish <#publish>`__
-  `License <#license>`__

Description
-----------

This package provides you an easy way to connect to The Things Network
via MQTT. Take note that, you'll first need to create an application
with a device to run the constructor of the MQTT client because you need
to provide, an applicationID and a deviceID. First include the package
in your file like this:

.. code:: python

    from ttnmqtt import MQTTClient as mqtt

MQTTClient
~~~~~~~~~~

The class constructor can be called following this scheme:

.. code:: python

    mqtt(APPID, APPEUI, PSW)

-  ``APPID``: this the name you gave your application when you created
   it.
-  ``APPEUI``: this the unique identifier of your application on the TTN
   platform.
-  ``PSW``: it can be found at the bottom of your application page under
   **ACCESS KEYS**. All the above informations can be found in your The
   Things Network console. The constructor returns an MQTTClient object
   set up with your application informations, ready for connection.

connect
~~~~~~~

Connects the previously created client to the The Things Network MQTT
broker by default.

.. code:: python

    client.connect([address], [port])

-  ``address``: the address of the MQTT broker you wish to connect to.
   Default to ``eu.thethings.network``
-  ``port``: the port on which you wish to connect. Default to ``1883``

disconnect
~~~~~~~~~~

Disconnects the MQTT client from which we call the method. Also able to
stop a forever loop in case the client was running on a loop launched by
the ``start()`` method.

.. code:: python

    client.disconnect()

start
~~~~~

Start a loop as the main loop of your process. You wont be able to run
anything else at the same time on this script.

.. code:: python

    client.start()

Take note that a loop need to be started in order to receive uplink
messages.

startBackground
~~~~~~~~~~~~~~~

Starts a loop for the client in the background so that it's possible to
run another process (such as a web server) in the same script.

.. code:: python

    client.startBackground()

stopBackground
~~~~~~~~~~~~~~

Stops a loop which was started with the ``startBackground()`` method. It
also disconnect the client.

.. code:: python

    client.stopBackground()

setUplinkCallback
~~~~~~~~~~~~~~~~~

Set the callback function, to be called when an uplink message is
received.

.. code:: python

    client.setUplinkCallback(uplinkCallback)

uplinkCallback
^^^^^^^^^^^^^^

The callback function must be declared in your script following this
structure: \* ``uplinkCallback(msg, client)`` \* ``msg``: the message
received by the client \* ``client``: the client from which the callback
is executed are calling

On each message reception, you should see **MESSAGE RECEIVED** in the
console, and the callback will be executed.

setConnectBehavior
~~~~~~~~~~~~~~~~~~

Change the connect callback function, following the paho-mqtt standart.

.. code:: python

    client.setConnectBehavior(custom_function)

-  ``custom_function(client, userdata, flags, rc)``: the function which
   will be the new connection behavior for our MQTT client.
-  ``client``: the MQTT client from which we call the callback.
-  ``userdata``: the data of the user. Default to ``''``
-  ``flags``: connection flags
-  ``rc``: result from the connect method. ``0`` if the connection
   succeeded.

click `here <https://pypi.python.org/pypi/paho-mqtt/1.3.0>`__ for more
information on the paho-mqtt package.

setPublishCallback
~~~~~~~~~~~~~~~~~~

Set the publish callback function, following the paho-mqtt standart.

.. code:: python

    client.setPublishCallback(publishCallback)

publishCallback
^^^^^^^^^^^^^^^

-  ``publishCallback(mid, client)``: the function which will be the new
   publish behavior for our MQTT client.
-  ``mid``: it matches the mid variable returned from the publish call
   to allow sent messages to be tracked.
-  ``client``: the MQTT client from which we call the callback.

publish
~~~~~~~

Publishes a message to the MQTT broker.

.. code:: python

    client.publish(deviceID, message)

-  ``deviceID``: the ID of the device you wish to send the message to.
-  ``message``: the message to be published to the broker. The message
   that's sent to the TTN broker needs to be a string and can follow
   this example (it's not mandatory but they are mostly build on this
   format):
   ``json  {"port": 1, "confirmed": false, "payload_raw": "AA=="}`` This
   message will send the payload 00 to your device.

License
-------

Source code for The Things Network is released under the MIT License,
which can be found in the `LICENSE <LICENSE>`__ file. A list of authors
can be found in the `AUTHORS <AUTHORS>`__ file.

.. |Build Status| image:: https://travis-ci.org/TheThingsNetwork/python-app-sdk.svg?branch=master
   :target: https://travis-ci.org/TheThingsNetwork/python-app-sdk
