# DragonFlyNetworkAnalysis

## Introduction
Project assumes creation of a large-scale dragonfly network model using NetBox simulation tool. On that model we will perform const and scalability analysis for that network. We will also consider physical placement of that network and add automation to it.

## Dragonfly topology

## [NetBox simulation tool](https://docs.netbox.dev/en/stable/introduction/)

NetBox is an open source tool for modeling and documenting modern networks. It provides a wide assortment of objects to allow creating infrastructure desing and document network starting from cabling, to IP address managements.

NetBox is highly customizable and extensible tool through plugins.

The most important feature for us is [**scripting**](https://docs.netbox.dev/en/stable/getting-started/populating-data/), which allows us to start from a small network and easily scale it in to a bigger one.

NetBox also contains [**REST API**](https://docs.netbox.dev/en/stable/integrations/rest-api/) to facilitate the population of data. Also it supports the bulk creation of multiple objects using only a single request.