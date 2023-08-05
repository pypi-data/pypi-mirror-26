==================
python-varnishapi
==================


------------------------------------
Connect to libvarnish api by ctypes
------------------------------------

:Author: Shohei Tanaka(@xcir)
:Date: 2017-10-22
:Version: 52.22
:Support Varnish Version: 4.0.x, 4.1.x 5.0.x 5.1.x 5.2.x
:Check Varnish Version: 5.1.3 5.2.0
:Check Python Version: 2.7.x, 3.4.x
:Manual section: 3

For Varnish3.0.x
=================
See this link.
https://github.com/xcir/python-varnishapi/tree/varnish30


Installation
============
sudo python setup.py install

Versioning
============
[varnish-version].[library-version]

50.18 is v18 for Varnish5.0.x

DESCRIPTION
============
Connect to libvarnish api by ctypes


VSLUtil class
---------------------------------------

VSLUtil.tag2Var
-------------------

Prototype
        ::

                tag2Var(tag, data)

Parameter
        ::

                
                STRING tag
                STRING data

Return value
        ::

                DICT Var
                

Description
        ::

                Transcode spec and tagname to variable name and value
Example
        ::

                vut = VSLUtil()

                # output is {'val': ' example.net', 'key': 'resp.http.Host', 'vkey': 'resp'}
                print vut.tag2Var('RespHeader','Host: example.net')

VSLUtil.tag2VarName
-------------------

Prototype
        ::

                tag2VarName(tag, data)

Parameter
        ::

                
                STRING tag
                STRING data

Return value
        ::

                STRING Variable name
                

Description
        ::

                Transcode spec and tagname to variable name
Example
        ::

                vut = VSLUtil()

                # output is "resp.http.Host"
                print vut.tag2VarName('RespHeader','Host: example.net')


VarnishStat class
---------------------------------------

VarnishStat.__init__
-----------------------

Prototype
        ::

                VarnishStat(opt = '', sopath = 'libvarnishapi.so.1')

Parameter
        ::

                LIST   arg [OPTION]
                STRING libvarnishapi path [OPTION]

Return value
        ::

                class object
                

Description
        ::

                initialize
Example
        ::

                vsc = VarnishStat()
                
                #set arg
                vsc = VarnishStat(['-n', 'v2'])

VarnishStat.Fini
-----------------------

Prototype
        ::

                Fini()

Parameter
        ::

                VOID

Return value
        ::

                VOID
                

Description
        ::

                finish
Example
        ::

                vsc = VarnishStat()
                ...
                vsc.Fini()


VarnishStat.getStats
---------------------

Prototype
        ::

                getStats()

Parameter
        ::

                
                VOID

Return value
        ::

                DICT stats
                

Description
        ::

                Get statistics counter
Example
        ::

                vsc = varnishapi.VarnishStat()
                r= vsc.getStat();
                for k,v in r.iteritems():
                    #output
                    #                         MAIN.fetch_zero                    0 Fetch zero len body
                    #                              MAIN.vmods                    1 Loaded VMODs
                    #                       MAIN.sess_dropped                    0 Sessions dropped for thread
                    #                           LCK.ban.locks              1457831 Lock Operations
                    #...
                    print "%40s %20s %s" % (k,v['val'],v['desc'])


VarnishLog class
---------------------------------------

VarnishLog.__init__
-----------------------

Prototype
        ::

                VarnishLog(opt = '', sopath = 'libvarnishapi.so.1', dataDecode = 1)

Parameter
        ::

                LIST   arg [OPTION]
                STRING libvarnishapi path [OPTION]
                INT Using decode at the callback [OPTION]

Return value
        ::

                class object
                

Description
        ::

                initialize
Example
        ::

                vsl = VarnishLog()
                
                #set arg
                vsl = VarnishLog(['-n', 'v2'])


VarnishLog.Fini
-----------------------

Prototype
        ::

                Fini()

Parameter
        ::

                VOID

Return value
        ::

                VOID
                

Description
        ::

                finish
Example
        ::

                vsl = VarnishLog()
                ...
                vsl.Fini()

VarnishLog.Dispatch
-----------------------

Prototype
        ::

                Dispatch(cb, priv = None)

Parameter
        ::

                FUNC    cb   callback function
                OBJECT  priv 

Return value
        ::

                INT
                

Description
        ::

                Dispatch callback function

Example
        ::

                def cb(vap,cbd,priv):
                    #output
                    #...
                    #{'level': 0L, 'type': 'c', 'reason': 0, 'vxid_parent': 0, 'length': 22L, 'tag': 26L, 'vxid': 65709, 'data': 'Vary: Accept-Encoding\x00', 'isbin': 0L}
                    #{'level': 0L, 'type': 'c', 'reason': 0, 'vxid_parent': 0, 'length': 23L, 'tag': 26L, 'vxid': 65709, 'data': 'Content-Encoding: gzip\x00', 'isbin': 0L}
                    #...
                    print cbd

                vsl = varnishapi.VarnishLog(['-c'])
                while 1:
                    ret = vsl.Dispatch(cb)
                    if 0 == ret:
                        time.sleep(0.5)
                vsl.Fini()


VarnishLog.VSL_tags / VSL_tags_rev
-----------------------------------

Prototype
        ::

                #This is list variable
                VSL_tags[tag index]
                #This is dictionary variable
                VSL_tags_rev[tag name]

Return value
        ::

                STRING tagname (VSL_tags)
                INT tagindex (VSL_tags_rev)
                

Description
        ::

                Transcode tag index to tag text, or reverse

Example
        ::

                def cb(vap,cbd,priv):
                    #output
                    #...
                    #VCL_call
                    #VCL_return
                    #...
                    print vap.VSL_tags[cbd['tag']]

                vsl = varnishapi.VarnishLog(['-c'])
                while 1:
                    ret = vsl.Dispatch(cb)
                    if 0 == ret:
                        time.sleep(0.5)
                vsl.Fini()

VarnishLog.VSL_tagflags
--------------------------------

Prototype
        ::

                #This is list variable
                VSL_tagflags[tag index]

Return value
        ::

                INT tagflags

Description
        ::

                tag flags

VarnishLog.VSLQ_grouping
--------------------------------

Prototype
        ::

                #This is list variable
                VSLQ_grouping[tag index]

Return value
        ::

                STRING VSLQ_grouping_name

Description
        ::

                VSL Query grouping name


HISTORY
===========
Version 52.22: Fix VSC/varnishstat bug.(fix declare, add fini(I mis-deleted...) p-r #71,72 thanks ehocdet). Fix key varnishstat's decode for python3.

Version 52.21: Initial support Varnish5.2.x

Version 50.20: Improoved C binding.(p-r #67 thanks ema)

Version 50.19: Fix -c -b option issue.(issue #65 thanks ema)

Version 50.18: Support Varnish5.0 tags.

Version 40.17: Add VSL_TAG, VSL_DATA. Rename class from LIBVARNISHAPI13 to LIBVARNISHAPI.(p-r #56,57,58 thanks ehocdet)

Version 40.16: Change the decode error handler from "strict" to "replace".(p-r #51 thanks szymi-)

Version 40.15: Fix Crash.

Version 40.14: Fix decode issue.(via vsltrans p-r #25. thanks szymi-) Add dataDecode option in VarnishLog.__init__.

Version 40.13: No source change.

Version 40.12: Support pip.(p-r #39 thanks ziollek)

Version 0.11-varnish40: Initial support for Python3. Feedback is welcome.

Version 0.10-varnish40: Fix some error log did not output. (p-r #33 thanks ema)

Version 0.9-varnish40: Change VarnishLog.(VSL_tags|VSL_tagflags|VSLQ_grouping) from object to list. Add VarnishLog.VSL_tags_rev.

Version 0.8-varnish40: Fix Crash if log abandoned.

Version 0.7-varnish40: Support Varnish4.1 tags

Version 0.6-varnish40: Fix -n/-N option doesn't work in VarnishStat(issue #15 thanks athoune)

Version 0.5-varnish40: Add VSLUtil.tag2Var VarnishStat.Fini(p-r #10 thanks bryyyon)

Version 0.4-varnish40: Support change to Varnish4

Version 0.3-varnish30: Support VSM_ReOpen

Version 0.2-varnish30: Support VSL_Arg

Version 0.1-varnish30: First version


COPYRIGHT
===========

python-varnishapi

* Copyright (c) 2015 Shohei Tanaka(@xcir)

Varnish Cache

* Copyright (c) 2006-2015 Varnish Software AS
