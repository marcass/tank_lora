def readlineCR(port):
    try:
        rv = ''
        while True:
            ch = port.read()
            rv += ch
            if ch=='\n':# or ch=='':
                if 'PY' in rv:              #arduino formats message as PY;<nodeID>;<waterlevle;batteryvoltage;>\r\n
                    #print 'Printing status flags stuff on receive'
                    #for x in tanks.tank_list:
                        #print x.name +' is ' +x.statusFlag
                    print rv
                    rec_split = rv.split(';')   #make array like [PYTHON, nodeID, payloadance]
                    print rec_split
                    sort_data(rec_split[1:4])
                    #q.put(rec_split[1:4])           #put data in queue for processing at rate
                    rv = ''
    except (KeyboardInterrupt, SystemExit):
        print "Interrupted"
        sys.exit()
    except:
        print 'failed on port read'
        port_start()
