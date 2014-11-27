import MySQLdb

try:
    conn=MySQLdb.connect(host='192.168.9.36',user='tuna',passwd='tuna',db='userdb')
    cur=conn.cursor()
    cur.execute("LOAD DATA LOCAL INFILE '/home/roo/git/team_py/data/user_sim.dat'             REPLACE INTO TABLE sim_user             FIELDS TERMINATED BY '|'             LINES TERMINATED BY '\n'")
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print 'Mysql Error %d: %s' % (e.args[0], e.args[1])