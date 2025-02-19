---
date: 2017-03-24T15:49:11Z
title: Analytics
description: Detail the analytics types that Tyk Pump generate and Dashboard presents via APIs or GUI.
tags:
  [
    "Tyk analytics",
    "Tyk pump analytics",
    "Tyk aggregated analytics",
    "Tyk detailed analytics",
  ]
weight: 3
menu:
  main:
    parent: "Tyk Dashboard"
aliases:
  - /analyse/
  - /tyk-stack/tyk-pump/tyk-dash-analytics/
---

The Tyk Dashboard has a full set of analytics functions and graphs that you can use to segment and view your API traffic and activity. The Dashboard offers a great way for you to debug your APIs and quickly pin down where errors might be cropping up and for what clients.

Tyk has two types of analytics:

1. Per request. Per request statistics contains information about each request, like path or status. It is also possible to enable "detailed request logging" where it will log base64 encoded data.
2. Aggregate. Aggregate statistics, aggregated by hour are available for the following keys: `APIID`, `ResponseCode`, `APIVersion`, `APIKey`, `OauthID`, `Geo`, `Tags` and `TrackPath`.

{{< note success >}}
**Note**

In Tyk v5.1 (and LTS patches v4.0.14 and v5.0.3) we introduced [User Owned Analytics]({{< ref "basic-config-and-security/security/dashboard/user-roles#user-owned-analytics" >}}) which can be used to limit the visibility of aggregate statistics to users when API Ownership is enabled. Due to the way that the analytics data are aggregated, not all statistics can be filtered by API and so may be inaccessible to users with the Owned Analytics permission.
{{< /note >}}

## How ?

When you make a request to the Tyk Gateway, it creates analytics records and stores them in a temporary Redis list, which is synced (and then flushed) every 10 seconds by the [Tyk Pump]({{< ref "tyk-pump" >}}). The Pump processes all synced analytic records, and forwards them to configured pumps. By default, to make the Tyk Dashboard work, there are 2 pumps depending on your database platform:

{{< tabs_start >}}
{{< tab_start "MongoDB" >}}

`mongo` (per request) and `mongo_aggregate` (for aggregate).
{{< tab_end >}}
{{< tab_start "SQL" >}}

`sql` (per request) and `sql_aggregate` (for aggregate)
{{< tab_end >}}
{{< tabs_end >}}
