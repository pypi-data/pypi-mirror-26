######
pyphihue
######

************
description.
************

Pyphihue is an API-wrapper for the Philips Hue lighting system which enables you to control your lights in an nice and easy way. It started as a small project to get myself familiar with classes, objects, methods and such. Now it's a little bit out of control but I'm happy with what I created so far and I want to share it with the world. 

please note!
============

At this point in time pyphihue delivers a Bridge and Light class with a limited amount of methods. A Group class has the highest priority now. But if there are a lot of requests coming in I'm more than happy to shuffle priorities.

**************
prerequisites.
**************

* Python 3.6 (it will probably work with 3.x but I have only tested 3.6)
* Philips Hue bridge ver2 (I have not tested this with the first generation) connected to your local network and powered on.

****************
getting started.
****************

First thing you need to do is create an instance of your bridge
    >>> import pyphihue
    >>> b = pyphihue.Bridge('192.168.0.1', '32-characters-of-username-here..')

if you don't have or don't know your username you can create a bridge object with only an ip-address
    >>> b = pyphihue.Bridge('192.168.0.1')

first and only thing to do now is create a user. press the link button first!
    >>> b.createuser('some-descriptive-text')

Now you're read to define a light. A light is connected to a bridge and has an id.
    >>> l = pyphihue.Light(b, 1)

Let there be light ;)
    >>> l.turnon()

List the methods defined
    >>> help(pyphihue)


note:
=====

Philip's provides documenation on how to find your bridge on your network. Please consult `their documentation <https://developers.meethue.com/documentation/getting-started>`_.

********
feedback
********

I welcome any kind of feedback but please be nice. If you like it let me know, if you have requests please ask. That will help me managing my backlog ;)
