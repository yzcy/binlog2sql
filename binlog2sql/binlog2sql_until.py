import argparse,datetime,getpass,sys
def myparse():
    parser = argparse.ArgumentParser(description="this is binlog2sql,it only support mysql8.0",add_help=False)
    parser.add_argument('-h', dest='host', type=str,
                                 help='Host the MySQL database server located', default='127.0.0.1')
    parser.add_argument('-p', dest='password', type=str,help='the password for connect database')
    parser.add_argument('-u', dest='username', type=str,help='the username for connect database')
    parser.add_argument('-B', dest='database', type=str, help='Database name,If null, all dml statements in the binlog will be returned')
    parser.add_argument('-t', dest='table', type=str,help='If no table name is specified and the database name is specified, the dml statement for all tables in the database will be returned')
    parser.add_argument('--start_time', dest='start_datetime', type=str,help='start datetime')
    parser.add_argument('--stop_time', dest='stop_datetime', type=str,help='stop datetime')
    parser.add_argument('-f', dest='flashback', type=bool,help='print flashback result',default=False)
    parser.add_argument('-P', dest='port', type=int,help='port of mysql service',default=3306)
    parser.add_argument('-H', dest='help', type=str,help='print help information')
    parser.add_argument('--start_file', dest='start_file', type=str,help='start_file')
    parser.add_argument('--stop_file', dest='stop_file', type=str,help='stop_file')
    return parser
def is_valid_datetime(string):
    try:
        datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False
def command_line_args(args):
    need_print_help = False if args else True
    parser = myparse()
    args = parser.parse_args(args)
    if args.help or need_print_help:
        parser.print_help()
        sys.exit(1)
    if not args.start_file:
        raise ValueError('Lack of parameter: start_file')
    # if args.flashback and args.stop_never:
    #     raise ValueError('Only one of flashback or stop-never can be True')
    # if args.flashback and args.no_pk:
    #     raise ValueError('Only one of flashback or no_pk can be True')
    if (args.start_datetime and not is_valid_datetime(args.start_datetime)) or \
            (args.stop_datetime and not is_valid_datetime(args.stop_datetime)):
        raise ValueError('Incorrect datetime argument')
    if not args.password:
        args.password = getpass.getpass()
    return args



def myinsert(sqlevents,invalues,flashback=False):
    if flashback==False:
        myinsert = []
        myvaluesK=[]
        myvaluesV = []
        for i in sqlevents:
            myinsert.append(i)
        for k,v in invalues:
            myvaluesK.append(f"`{k}`")
            myvaluesV.append(f"'{v}'")
        sten1 = f"insert into {myinsert[0][1]}.{myinsert[1][1]}({myvaluesK}) values({myvaluesV})"
        sten2 = sten1.replace("[", "").replace("]", "").replace("'", "")
        print(sten2 + ";")
    else:
        mydelete(sqlevents,invalues,flashback=False)

def mydelete(sqlevents,delvalues,flashback=False):
    mydelete = [] #[('schema', 'kdb'), ('table', 'myt')]
    myvalues=[] #['`aa`="c"', '`bb`="3"', '`cc`="2020-02-02 20:20:20"']
    if flashback == False:
        for i in sqlevents:
            mydelete.append(i)
        for k,v in delvalues:
            tempv = f'`{k}`="{v}"'
            myvalues.append(tempv)
        myvalues = str(myvalues).replace(",", " and")
        sten1 = f"delete from {mydelete[0][1]}.{mydelete[1][1]} where {myvalues}"
        sten2 = sten1.replace("[", "").replace("]", "").replace("'", "")
        print(sten2 + ";")
    else:
        myinsert(sqlevents, delvalues, flashback=False)
def mkupdate(sqlevents,afvalues,bevalues,flashback=False):
    myupdate = []
    bedata=[]
    afdata=[]
    # print(sqlevents,afvalues,bevalues)
    for i in sqlevents:
        myupdate.append(i)
    for k,v in afvalues:
        tempv = f'`{k}`="{v}"'
        bedata.append(tempv)
    for k,v in bevalues:
        tempv = f'`{k}`="{v}"'
        afdata.append(tempv)
    if flashback == False:
        afdata=str(afdata).replace(","," and")
        # print('update %s.%s set %s' % (myupdate[0][1], myupdate[1][1],chagedata))
        sten1=f"update {myupdate[0][1]}.{myupdate[1][1]} set {bedata} where {afdata}"
        sten2=sten1.replace("[","" ).replace("]","").replace("'","")
        print(sten2+";")
    else:
        bedata=str(bedata).replace(","," and")
        # print('update %s.%s set %s' % (myupdate[0][1], myupdate[1][1],chagedata))
        sten1=f"update {myupdate[0][1]}.{myupdate[1][1]} set {afdata} where {bedata}"
        sten2=sten1.replace("[","" ).replace("]","").replace("'","")
        print(sten2+";")
if __name__ == "__main__":
    myargs=myparse()
    print(myargs.host)
