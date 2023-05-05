# DragonFlyNetworkAnalysis

## Introduction
Project assumes creation of a large-scale dragonfly network model using NetBox simulation tool. On the network model with reasonable amount of nodes we will perform cost and scalability analysis. We will also consider physical parameters of the network and add an automation to the simulation.

## [Dragonfly topology](https://static.googleusercontent.com/media/research.google.com/pl//pubs/archive/34926.pdf)

Topology introduced in cooperation with Google to create a highly-scalable, low-latency and low-cost networks between data centers. It focuses on minimizing the number and length of interconenction cables, which can otherwise dominate the network costs. Nodes are connected to routers gathered into groups in which they are densely connected. Each group has a minimum of one connection to every other. As a result, a maximum of one inter-group connection has to be used to route a packet between any two nodes.

## [NetBox simulation tool](https://docs.netbox.dev/en/stable/introduction/)

NetBox is an open source tool for modeling and documenting modern networks. It provides a wide assortment of objects to allow creating infrastructure desing and document network starting from cabling, to IP address managements.

NetBox is highly customizable and extensible tool through plugins such as metrics or new functionalities.

The most important feature for us is [**scripting**](https://docs.netbox.dev/en/stable/getting-started/populating-data/), which allows us to start from a small network and easily scale it in to a bigger one.

NetBox also contains [**REST API**](https://docs.netbox.dev/en/stable/integrations/rest-api/) to facilitate the population of data. Also it supports the bulk creation of multiple objects using only a single request.
