# encoding=utf8

import time
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)
import pymysql
from pymysql.cursors import DictCursor
from binlog2sql_until import *


class GetData:
    def __init__(self, conndict, bdatetime, edatetime, flashback, start_file, stop_file, database, table):
        self.bdatetime = int(time.mktime(time.strptime(bdatetime, '%Y-%m-%d %H:%M:%S')))
        self.edatetime = int(time.mktime(time.strptime(edatetime, '%Y-%m-%d %H:%M:%S')))
        self.binlogList = []
        self.flashback = flashback
        self.stop_file = stop_file
        self.start_file = start_file
        self.schema = database
        self.table = table

    def get_data(self):
        # for binlog in self.binlogList:
        stream = BinLogStreamReader(connection_settings=conndict, server_id=1, log_file=self.start_file,
                                    log_pos=4, resume_stream=True,
                                    only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent])
        for binlogevent in stream:
            for row in binlogevent.rows:
                event = {"schema": binlogevent.schema, "table": binlogevent.table}
                # print(datetime.datetime.fromtimestamp(binlogevent.timestamp))
                if binlogevent.timestamp >= self.bdatetime and binlogevent.timestamp <= self.edatetime:
                    # 判断时间范围
                    db_t_name=[i for i in event.items()]
                    if self.schema == db_t_name[0][1] and self.table == db_t_name[1][1]:
                        # 限制某个库某个表
                        if isinstance(binlogevent, DeleteRowsEvent):
                            mydelete(event.items(), row["values"].items(), self.flashback)
                        elif isinstance(binlogevent, UpdateRowsEvent):
                            # event["action"] = "update"
                            mkupdate(event.items(), row["after_values"].items(), row["before_values"].items(),
                                     self.flashback)
                        elif isinstance(binlogevent, WriteRowsEvent):
                            # event["action"] = "insert"
                            myinsert(event.items(), row["values"].items(), self.flashback)
                    if self.schema == db_t_name[0][1] and self.table == None:
                        if isinstance(binlogevent, DeleteRowsEvent):
                            mydelete(event.items(), row["values"].items(), self.flashback)
                        elif isinstance(binlogevent, UpdateRowsEvent):
                            # event["action"] = "update"
                            mkupdate(event.items(), row["after_values"].items(), row["before_values"].items(),
                                     self.flashback)
                        elif isinstance(binlogevent, WriteRowsEvent):
                            # event["action"] = "insert"
                            myinsert(event.items(), row["values"].items(), self.flashback)
                    if self.schema == None and self.table == None:
                        if isinstance(binlogevent, DeleteRowsEvent):
                            mydelete(event.items(), row["values"].items(), self.flashback)
                        elif isinstance(binlogevent, UpdateRowsEvent):
                            # event["action"] = "update"
                            mkupdate(event.items(), row["after_values"].items(), row["before_values"].items(),
                                     self.flashback)
                        elif isinstance(binlogevent, WriteRowsEvent):
                            # event["action"] = "insert"
                            myinsert(event.items(), row["values"].items(), self.flashback)
                    # sys.stdout.flush()
        stream.close()


if __name__ == '__main__':
    myargs = command_line_args(sys.argv[1:])
    conndict = {"host": myargs.host, "port": myargs.port, "user": myargs.username, "password": myargs.password}
    # , "database": myargs.database, "table": myargs.table
    # print(conndict,myargs.start_datetime,myargs.stop_datetime,myargs.flashback,myargs.start_file)
    getdata = GetData(conndict, myargs.start_datetime, myargs.stop_datetime, myargs.flashback, myargs.start_file,
                      myargs.stop_file, myargs.database, myargs.table)
    getdata.get_data()
