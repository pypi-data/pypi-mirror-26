..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Vitrage API
-----------
|

.. contents:: Contents:
   :local:

Overview
********
**This document describes the Vitrage API v1.**

**The Vitrage API provides a RESTful JSON interface for interacting with Vitrage Service.**

List Versions
^^^^^^^^^^^^^

Lists the supported versions of the Vitrage API.

GET /
~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

None.

Request Body
============

None.

Request Examples
================

::

    GET / HTTP/1.1
    Host: 135.248.19.18:8999
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json



ResponseStatus code
===================

-  200 - OK

Response Body
=============

Returns a JSON object with a 'links' array of links of supported versions.

Response Examples
=================

::

    {
        "versions": [
            {
               "id": "v1.0",
              "links": [
                    {
                     "href": "http://135.248.19.18:8999/v1/",
                    "rel": "self"
                   }
              ],
              "status": "CURRENT",
              "updated": "2015-11-29"
            }
        ]

    }



Get  topology
^^^^^^^^^^^^^

Get the topology for the cluster.
Its possible to filter the edges vertices and depth of the
graph


POST /v1/topology/
~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

None

Request Body
============

Consists of a topology request definition which has the following properties:

* root - (string, optional) the root node to start. defaults to the openstack node
* depth - (int, optional) the depth of the topology graph. defaults to max depth
* graph_type-(string, optional) can be either tree or graph. defaults to graph
* query - (string, optional) a json query filter to filter the graph components. defaults to return all the graph
* all_tenants - (boolean, optional) shows the entities of all the tenants in the graph (in case the user has the permissions).

query expression
================
::

 query := expression
 expression := simple_expression|complex_expression
 simple_expression := {simple_operator: {field_name: value}}
 simple_operator := = | != | < | <= | > | >=
 complex_expression := {complex_operator: [expression, expression, ...]} | not_expression
 not_expression := {not: expression}
 complex_operator := and | or


Query example
=============

::

    POST /v1/topology/
    Host: 135.248.19.18:8999
    Content-Type: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

    {
      "query" :
       {
          "or":
          [
              "=":
                  {
                    "vitrage_type":"host"
                  },
              "=":
                  {
                    "vitrage_type":"instance"
                  },
              "=":
                  {
                    "vitrage_type":"zone"
                  },
              "=":
                  {
                    "vitrage_type":"node"
                  }
          ]
       }
       "graph_type" : "tree"
       limit : 4
    }



Response Status Code
====================

-  200 - OK
-  400 - Bad request

Response Body
=============

Returns a JSON object that describes a graph with nodes
and links. If a tree representation is asked then returns
a Json tree with nodes and children.

An error of cannot represent as a tree will be return if the
graph is not a tree. (400 - Bad request)

Response Examples
=================

::

 {
  "directed": true,
  "graph": {},
  "nodes": [
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-8",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "20d12a8a-ea9a-89c6-5947-83bea959362e",
      "vitrage_id": "RESOURCE:nova.instance:20d12a8a-ea9a-89c6-5947-83bea959362e"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-2",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "dc35fa2f-4515-1653-ef6b-03b471bb395b",
      "vitrage_id": "RESOURCE:nova.instance:dc35fa2f-4515-1653-ef6b-03b471bb395b"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-13",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "9879cf5a-bdcf-3651-3017-961ed887ec86",
      "vitrage_id": "RESOURCE:nova.instance:9879cf5a-bdcf-3651-3017-961ed887ec86"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-10",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "fe124f4b-9ed7-4591-fcd1-803cf5c33cb1",
      "vitrage_id": "RESOURCE:nova.instance:fe124f4b-9ed7-4591-fcd1-803cf5c33cb1"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-11",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "f2e48a97-7350-061e-12d3-84c6dc3e67c0",
      "vitrage_id": "RESOURCE:nova.instance:f2e48a97-7350-061e-12d3-84c6dc3e67c0"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "host-2",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "available",
      "vitrage_type": "nova.host",
      "id": "host-2",
      "vitrage_id": "RESOURCE:nova.host:host-2"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "host-3",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "available",
      "vitrage_type": "nova.host",
      "id": "host-3",
      "vitrage_id": "RESOURCE:nova.host:host-3"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "host-0",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "available",
      "vitrage_type": "nova.host",
      "id": "host-0",
      "vitrage_id": "RESOURCE:nova.host:host-0"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "host-1",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "available",
      "vitrage_type": "nova.host",
      "id": "host-1",
      "vitrage_id": "RESOURCE:nova.host:host-1"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-9",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "275097cf-954e-8e24-b185-9514e24b8591",
      "vitrage_id": "RESOURCE:nova.instance:275097cf-954e-8e24-b185-9514e24b8591"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-1",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "a0f0805f-c804-cffe-c25a-1b38f555ed68",
      "vitrage_id": "RESOURCE:nova.instance:a0f0805f-c804-cffe-c25a-1b38f555ed68"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-14",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "56af57d2-34a4-19b1-5106-b613637a11a7",
      "vitrage_id": "RESOURCE:nova.instance:56af57d2-34a4-19b1-5106-b613637a11a7"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "zone-1",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "available",
      "vitrage_type": "nova.zone",
      "id": "zone-1",
      "vitrage_id": "RESOURCE:nova.zone:zone-1"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-3",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "16e14c58-d254-2bec-53e4-c766e48810aa",
      "vitrage_id": "RESOURCE:nova.instance:16e14c58-d254-2bec-53e4-c766e48810aa"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-7",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "f35a1e10-74ff-7332-8edf-83cd6ffcb2de",
      "vitrage_id": "RESOURCE:nova.instance:f35a1e10-74ff-7332-8edf-83cd6ffcb2de"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-4",
      "update_timestamp": "2015-12-01T12:46:41Z?vitrage_id=all",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "ea8a450e-cab1-2272-f431-494b40c5c378",
      "vitrage_id": "RESOURCE:nova.instance:ea8a450e-cab1-2272-f431-494b40c5c378"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-6",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "6e42bdc3-b776-1b2c-2c7d-b7a8bb98f721",
      "vitrage_id": "RESOURCE:nova.instance:6e42bdc3-b776-1b2c-2c7d-b7a8bb98f721"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-5",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "8c951613-c660-87c0-c18b-0fa3293ce8d8",
      "vitrage_id": "RESOURCE:nova.instance:8c951613-c660-87c0-c18b-0fa3293ce8d8"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "zone-0",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "available",
      "vitrage_type": "nova.zone",
      "id": "zone-0",
      "vitrage_id": "RESOURCE:nova.zone:zone-0"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-0",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "78353ce4-2710-49b5-1341-b8cbb6000ebc",
      "vitrage_id": "RESOURCE:nova.instance:78353ce4-2710-49b5-1341-b8cbb6000ebc"
    },TODO
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-12",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "35bf479a-75d9-80a9-874e-d3b50fb2dd2e",
      "vitrage_id": "RESOURCE:nova.instance:35bf479a-75d9-80a9-874e-d3b50fb2dd2e"
    },
    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "openstack.cluster",
      "vitrage_type": "openstack.cluster",
      "id": "openstack.cluster",
      "vitrage_id": "RESOURCE:openstack.cluster"
    }
  ],
  "links": [
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 3,
      "key": "contains",
      "source": 5
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 1,
      "key": "contains",
      "source": 5
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 16,
      "key": "contains",
      "source": 5
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 11,
      "key": "contains",
      "source": 5
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 13,
      "key": "contains",
      "source": 6
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 4,
      "key": "contains",
      "source": 6
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 14,
      "key": "contains",
      "source": 6
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 20,
      "key": "contains",
      "source": 7
    },?vitrage_id=all
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 0,
      "key": "contains",
      "source": 7
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 19,
      "key": "contains",
      "source": 7
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 15,
      "key": "contains",
      "source": 7
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 9,
      "key": "contains",
      "source": 8
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 10,
      "key": "contains",
      "source": 8
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 2,
      "key": "contains",
      "source": 8
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 17,
      "key": "contains",
      "source": 8
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 6,
      "key": "contains",
      "source": 12
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 8,
      "key": "contains",
      "source": 12
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 5,
      "key": "contains",
      "source": 18
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 7,
      "key": "contains",
      "source": 18
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 18,
      "key": "contains",
      "source": 21
    },
    {
      "relationship_name": "contains",
      "vitrage_is_deleted": false,
      "target": 12,
      "key": "contains",
      "source": 21
    }
  ],
  "multigraph": true
 }

Show RCA
^^^^^^^^

Shows the root cause analysis on an alarm.

GET /v1/rca/
~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

alarm id - (string(255)) get rca on this alarm.

Request Body
============

* all_tenants - (boolean, optional) shows the rca of all tenants (in case the user has the permissions).

Request Examples
================

::

    GET /v1/rca/alarm_id=ALARM%3Anagios%3Ahost0%3ACPU%20load HTTP/1.1
    Host: 135.248.19.18:8999
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json



Response Status code
====================

-  200 - OK

Response Body
=============

Returns a JSON object represented as a graph with all the alarms that either causing the alarm or caused by the requested alarm.

Response Examples
=================

::

 {
  "directed": true,
  "graph": {

  },
  "nodes": [
    {
      "vitrage_category": "ALARM",
      "vitrage_type": "nagios",
      "name": "CPU load",
      "state": "Active",
      "severity": "WARNING",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "info": "WARNING - 15min load 1.66 at 32 CPUs",
      "resource_type": "nova.host",
      "resource_name": "host-0",
      "resource_id": "host-0",
      "id": 0,
      "vitrage_id": "ALARM:nagios:host0:CPU load"
    },
    {
      "vitrage_category": "ALARM",
      "vitrage_type": "vitrage",
      "name": "Machine Suboptimal",
      "state": "Active",
      "severity": "WARNING",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "resource_type": "nova.instance",
      "resource_name": "vm0",
      "resource_id": "20d12a8a-ea9a-89c6-5947-83bea959362e",
      "id": 1,
      "vitrage_id": "ALARM:vitrage:vm0:Machine Suboptimal"
    },
    {
      "vitrage_category": "ALARM",
      "vitrage_type": "vitrage",
      "name": "Machine Suboptimal",
      "state": "Active",
      "severity": "WARNING",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "resource_type": "nova.instance",
      "resource_name": "vm1",
      "resource_id": "275097cf-954e-8e24-b185-9514e24b8591",
      "id": 2,
      "vitrage_id": "ALARM:vitrage:vm1:Machine Suboptimal"
    }
  ],
  "links": [
    {
      "source": 0,
      "target": 1,
      "relationship": "causes"
    },
    {
      "source": 0,
      "target": 2,
      "relationship": "causes"
    }
  ],
  "multigraph": false,
  "inspected_index": 0
 }


List Alarms
^^^^^^^^^^^

Shows the alarms on a resource or all alarms

GET /v1/alarm/
~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

vitrage_id - (string(255)) get alarm on this resource can be 'all' for all alarms.

Request Body
============

* all_tenants - (boolean, optional) shows the alarms of all tenants (in case the user has the permissions).

Request Examples
================

::

    GET /v1/alarms/?vitrage_id=all HTTP/1.1
    Host: 135.248.19.18:8999
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json

Response Status code
====================

-  200 - OK

Response Body
=============

Returns a JSON object with all the alarms requested.

Response Examples
=================

::


  [
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "nagios",
       "name": "CPU load",
       "state": "Active",
       "severity": "WARNING",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "info": "WARNING - 15min load 1.66 at 32 CPUs",
       "resource_type": "nova.host",
       "resource_name": "host-0",
       "resource_id": "host-0",
       "id": 0,
       "vitrage_id": "ALARM:nagios:host0:CPU load",
       "normalized_severity": "WARNING"
     },
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "vitrage",
       "name": "Machine Suboptimal",
       "state": "Active",
       "severity": "CRITICAL",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "resource_type": "nova.instance",
       "resource_name": "vm0",
       "resource_id": "20d12a8a-ea9a-89c6-5947-83bea959362e",
       "id": 1,
       "vitrage_id": "ALARM:vitrage:vm0:Machine Suboptimal",
       "normalized_severity": "CRITICAL"
     },
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "vitrage",
       "name": "Machine Suboptimal",
       "state": "Active",
       "severity": "CRITICAL",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "resource_type": "nova.instance",
       "resource_name": "vm1",
       "resource_id": "275097cf-954e-8e24-b185-9514e24b8591",
       "id": 2,
       "vitrage_id": "ALARM:vitrage:vm1:Machine Suboptimal",
       "normalized_severity": "CRITICAL"
     },
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "aodh",
       "name": "Memory overload",
       "state": "Active",
       "severity": "WARNING",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "info": "WARNING - 15min load 1.66 at 32 CPUs",
       "resource_type": "nova.host",
       "resource_name": "host-0",
       "resource_id": "host-0",
       "id": 3,
       "vitrage_id": "ALARM:aodh:host0:Memory overload",
       "normalized_severity": "WARNING"
     }
 ]

Template Validate
^^^^^^^^^^^^^^^^^

An API for validating templates

POST /v1/template/
~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

None.

Query Parameters
================

-  path (string(255), required) - the path to template file or directory

Request Body
============

None

Request Examples
================

::

    POST /v1/template/?path=[file/dir path]
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Content-Type: application/json
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

Response Status code
====================

None

Response Body
=============

Returns a JSON object that is a list of results.
Each result describes a full validation (syntax and content) of one template file.

Response Examples
=================

::

    {
      "results": [
        {
          "status": "validation failed",
          "file path": "/tmp/templates/basic_no_meta.yaml",
          "description": "Template syntax validation",
          "message": "metadata is a mandatory section.",
          "status code": 62
        },
        {
          "status": "validation OK",
          "file path": "/tmp/templates/basic.yaml",
          "description": "Template validation",
          "message": "Template validation is OK",
          "status code": 4
        }
      ]
    }

Template List
=============

List all templates loaded from /etc/vitrage/templates, both those that passed validation and those that did not.

GET /v1/template/
~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)

Path Parameters
===============

None

Query Parameters
================

None

Request Body
============

None

Request Examples
================

::

    GET /v1/template/
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

Response Status code
====================

None

Response Body
=============

Returns list of all templates loaded from /etc/vitrage/templates, both those that passed validation and those that did not.

Response Examples
=================

::

    +--------------------------------------+---------------------------------------+--------+--------------------------------------------------+----------------------+
    | uuid                                 | name                                  | status | status details                                   | date                 |
    +--------------------------------------+---------------------------------------+--------+--------------------------------------------------+----------------------+
    | 67bebcb4-53b1-4240-ad05-451f34db2438 | vm_down_causes_suboptimal_application | failed | Entity definition must contain template_id field | 2016-06-29T12:24:16Z |
    | 4cc899e6-f6cb-43d8-94a0-6fa937e41ae2 | host_cpu_load_causes_vm_problem       | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    | 0548367e-711a-4c08-9bdb-cb61f96fed04 | switch_connectivity_issues            | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    | 33cb4400-f846-4c64-b168-530824d38f3e | host_nic_down                         | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    | a04cd155-0fcf-4409-a27c-c83ba8b20a3c | disconnected_storage_problems         | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    +--------------------------------------+---------------------------------------+--------+--------------------------------------------------+----------------------+


Template Show
^^^^^^^^^^^^^

Shows the template body for given template ID

GET /v1/template/[template_uuid]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Headers
=======

-  User-Agent (string)
-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

- template uuid

Query Parameters
================

None

Request Body
============

None

Request Examples
================

::

    GET /v1/template/a0bdb89a-fe4c-4b27-adc2-507b7ec44c24
    Host: 135.248.19.18:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json



Response Status code
====================

-  200 - OK
-  404 - failed to show template with uuid: [template_uuid]

Response Body
=============

Returns a JSON object which represents the template body

Response Examples
=================

::

    {
      "scenarios": [
        {
          "scenario": {
            "actions": [
              {
                "action": {
                  "action_target": {
                    "target": "instance"
                  },
                  "properties": {
                    "alarm_name": "exploding_world",
                    "severity": "CRITICAL"
                  },
                  "action_type": "raise_alarm"
                }
              }
            ],
            "condition": "alarm_1_on_host and host_contains_instance"
          }
        },
        {
          "scenario": {
            "actions": [
              {
                "action": {
                  "action_target": {
                    "source": "alarm_1",
                    "target": "alarm_2"
                  },
                  "action_type": "add_causal_relationship"
                }
              }
            ],
            "condition": "alarm_1_on_host and alarm_2_on_instance and host_contains_instance"
          }
        }
      ],
      "definitions": {
        "relationships": [
          {
            "relationship": {
              "relationship_type": "on",
              "source": "alarm_1",
              "target": "host",
              "template_id": "alarm_1_on_host"
            }
          },
          {
            "relationship": {
              "relationship_type": "on",
              "source": "alarm_2",
              "target": "instance",
              "template_id": "alarm_2_on_instance"
            }
          },
          {
            "relationship": {
              "relationship_type": "contains",
              "source": "host",
              "target": "instance",
              "template_id": "host_contains_instance"
            }
          }
        ],
        "entities": [
          {
            "entity": {
              "vitrage_category": "ALARM",
              "vitrage_type": "nagios",
              "name": "check_libvirtd",
              "template_id": "alarm_1"
            }
          },
          {
            "entity": {
              "vitrage_category": "RESOURCE",
              "vitrage_type": "nova.host",
              "template_id": "host"
            }
          },
          {
            "entity": {
              "vitrage_category": "RESOURCE",
              "vitrage_type": "nova.instance",
              "template_id": "instance"
            }
          },
          {
            "entity": {
              "vitrage_category": "ALARM",
              "vitrage_type": "vitrage",
              "name": "exploding_world",
              "template_id": "alarm_2"
            }
          }
        ]
      },
      "metadata": {
        "name": "first_deduced_alarm_ever"
    }

Event Post
^^^^^^^^^^
Post an event to Vitrage message queue, to be consumed by a datasource driver.

POST /v1/event/
~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

None.

Query Parameters
================

None.

Request Body
============

An event to be posted. Will contain the following fields:

- time: a timestamp of the event. In case of a monitor event, should specify when the fault has occurred.
- type: the type of the event.
- details: a key-value map of metadata.

A dict of some potential details, copied from the Doctor SB API reference:

- hostname: the hostname on which the event occurred.
- source: the display name of reporter of this event. This is not limited to monitor, other entity can be specified such as ‘KVM’.
- cause: description of the cause of this event which could be different from the type of this event.
- severity: the severity of this event set by the monitor.
- status: the status of target object in which error occurred.
- monitorID: the ID of the monitor sending this event.
- monitorEventID: the ID of the event in the monitor. This can be used by operator while tracking the monitor log.
- relatedTo: the array of IDs which related to this event.

Request Examples
================

::

    POST /v1/event/
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Content-Type: application/json
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7


::

    {
        'event': {
            'time': '2016-04-12T08:00:00',
            'type': 'compute.host.down',
            'details': {
                'hostname': 'compute-1',
                'source': 'sample_monitor',
                'cause': 'link-down',
                'severity': 'critical',
                'status': 'down',
                'monitor_id': 'monitor-1',
                'monitor_event_id': '123',
            }
        }
    }



Response Status code
====================

-  200 - OK
-  400 - Bad request

Response Body
=============

Returns an empty response body if the request was OK.
Otherwise returns a detailed error message (e.g. 'missing time parameter').

Resource list
^^^^^^^^^^^^^
List the resources with specified type or all the resources.

GET /v1/resources/
~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

None.

Query Parameters
================

* resource_type - (string, optional) the type of resource, defaults to return all resources.
* all_tenants - (boolean, optional) shows the resources of all tenants (in case the user has the permissions).

Request Body
============

None.

Request Examples
================

::

    GET /v1/resources/?all_tenants=False&resource_type=nova.host
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Content-Type: application/json
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7


Response Status code
====================

-  200 - OK
-  404 - Bad request

Response Body
=============

Returns a list with all the resources requested.

Response Examples
=================

::

  [
    {
      "vitrage_id": "RESOURCE:nova.host:cloud",
      "vitrage_aggregated_state": "AVAILABLE",
      "state": "available",
      "vitrage_type": "nova.host",
      "id": "cloud",
      "metadata": {
        "name": "cloud",
        "update_timestamp": "2017-04-24 04:27:47.501777+00:00"
      }
    }
  ]


Resource show
^^^^^^^^^^^^^
Show the details of specified resource.

GET /v1/resources/[vitrage_id]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

- vitrage_id.

Query Parameters
================

None.

Request Body
============

None.

Request Examples
================

::

    GET /v1/resources/`<vitrage_id>`
    Host: 127.0.0.1:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

Response Status code
====================

-  200 - OK
-  404 - Bad request

Response Body
=============

Returns details of the requested resource.

Response Examples
=================

::

    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-1",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "dc35fa2f-4515-1653-ef6b-03b471bb395b",
      "vitrage_id": "RESOURCE:nova.instance:dc35fa2f-4515-1653-ef6b-03b471bb395b"
    }
