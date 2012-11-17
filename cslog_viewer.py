#!/usr/bin/python
# coding: utf-8


import datetime
import sys
import string
import time
import re
import calendar
import urllib
import shutil
import socket
import signal
import filetail
import email_sender
import string, threading, time
import select

reload(sys)
sys.setdefaultencoding('utf8')
import chain_controller

logpats_time = r'(\S+) (\S+) (\S+) \[(.*?)\] '\
               r'"(\S+) (\S+) (\S+)" (\S+) (\S+) '\
               r'"(\S+)" "(.*?)" "(\S+)" "(\S+)"  (\S+) (\S+) (\S+)'

logpats_time = r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+),(\d+) (\S+) \[(.*?)\] \((\S+)\) (.*)'

logpats_time = r'((\d+)-(\d+)-(\d+)) ((\d+):(\d+):(\d+),(\d+)) (\S+) \[(.*?)\] \((\S+)\) (.*)'

logpat_time = re.compile(logpats_time)


class eslog_viewer:
    def set_cache_flag( self, iscache ):
        self.is_cache = iscache

    def clear_cache(self):
        self.cache_log = None
        self.cache_log = []

    def add_cache_log(self, one_log ):
        one_log = one_log.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        self.cache_log.append(one_log + "<br />\r\n")
        pass

    def get_cache_log(self):
        all_line = ''
        for line in self.cache_log:
            all_line += line
        return all_line
        pass

    def begin(self):
        pass

    def process_line(self, s):
        if s.endswith("\r\n") or s.endswith("\n"):
            pass
        else:
            s += "\r\n"
        mr = self.is_start_with_time(s)
        if mr is None:
            pass
        else:
            if False:  # for debug log format
                print "0", mr.group(0)
                print "1", mr.group(1)
                #print "2", mr.group( 2 )
                #print "3", mr.group( 3 )
                #print "4", mr.group( 4 )
                print "5", mr.group(5)
                #print "6", mr.group( 6 )
                #print "7", mr.group( 7 )
                #print "8", mr.group( 8 )
                #print "9", mr.group( 9 )
                print "10", mr.group(10)
                print "11", mr.group(11)
                print "12", mr.group(12)
                print "13", mr.group(13)
            class_str = mr.group(11)
            tmps = class_str.split('.')
            lens = len(tmps)
            type_str = mr.group(12)
            content_str = mr.group(13)
            if lens > 1:
                class_str = tmps[lens - 1]
            #if self.curr_class == '':
            self.curr_class = class_str
            if self.curr_class != self.pre_class:
                #print class_str ,'\t', type_str ,'\t\t\t'
                if self.is_ommit_class( self.curr_class ):
                    pass
                else:
                    self.print_and_cache(class_str, False)
                    self.pre_class = self.curr_class
            if self.is_ommit_class( self.curr_class ):
                pass
            else:
                self.print_and_cache(content_str, True)
            pass
        s = self.remove_time_prefix(s)

    def is_ommit_class(self,cls_name):
        if cls_name in "Request ":
            return True
        return False
        pass


    def print_and_cache(self, content_str, intend=False):
        #omit content
        tmp_content = content_str
        tmp_content = tmp_content.strip()
        if tmp_content.startswith("Ping "):
            return
        if tmp_content.startswith("cleaning up "):
            return
        if tmp_content.startswith("VmStatsCollector "):
            return
        if tmp_content.startswith("HostStatsCollector "):
            return
        if intend:
            print '\t\t', content_str
        else:
            print content_str
        if self.is_cache:
            if intend:
                self.add_cache_log('\t\t' + content_str)
            else:
                self.add_cache_log(content_str)

    def is_start_with_time( self, s ):
        #2012-05-17 02:51:48,156 DEBUG [cloud.vm.VirtualMachineManagerImpl] (StatsCollector-3:null) Cleanup succeeded. Details null
        mr = logpat_time.match(s)
        return mr
        pass
        if mr is None:
            return False
        return True

    def remove_time_prefix( self, s  ):
        return s
        pass

    def end(self):
        pass

    def description(self):
        pass

    def result(self):
        pass

    def __init__( self ):
        self.pre_class = ''
        self.cache_log = []
        self.curr_class = ''
        self.is_cache = False
        self.allow_running = True
        pass


def thread_pring_log():
    threadname = threading.currentThread().getName()
    print threadname
    ac = chain_controller.controller(sys.stdin)
    ac.subscribe(eslog_viewer())
    ac.run()


def thread_keyboard_monitor( ev ):
    while ev.allow_running:
        heardEnter(ev)
    pass


def heardEnter( ev ):
    i, o, e = select.select([sys.stdin], [], [], 0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            input = input.replace("\r\n", "")
            input = input.replace("\n", "")
            if "exit" == input:
                ev.allow_running = False
                print "BYE BYE :-) "
                sys.exit(0)
            if "b" == input:
                ev.clear_cache()
                ev.set_cache_flag(True)
                print "-   -   -   -   -   -   -   -   -   -   -   -   begin,e for end\r\n"
            if "e" == input:
                ev.set_cache_flag(False)
                #print ev.get_cache_log()
                #ev.clear_cache()
                print "=   =   =  =   =   =  =   =   =  =   =   =  =   end\r\n"
            if "email" == input:
                content = ev.get_cache_log()
                es = email_sender.email_sender()
                now = datetime.datetime.now()
                today = datetime.date.today()
                module_name = "chain_mail_config"
                dyna_module = __import__(module_name)
                title = str(today) + " log email report"
                print "title:", title , " please wait for send over."
                html_content = """
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN"><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Content-Language" content="zh-CN"> 
</head>
<body>
				"""
                html_content += content
                html_content += "</body></html>"
                plain_content = ""
                es.send_html_email(dyna_module.config_mail_smtp, dyna_module.config_mail_from,
                    dyna_module.config_mail_from_password, dyna_module.config_mail_send_to, plain_content, html_content,
                    title)
                print "send over"
            #send it ...
            return True
    return False




def main(stdscr):
    while True:
        value = raw_input("Prompt:")
        if value != -1:
            print "-   -   -   -   -   -   -   -   -   -   -   -   \r\n"
            print value
        continue
        if True:
            break
        c = stdscr.getch()
        if c != -1:
            print "-   -   -   -   -   -   -   -   -   -   -   -   \r\n"
            print str(c)
            stdscr.refresh()
            pass


def handler(signum, frame):
    print 'BYE :--) '
    ev.allow_running = False
    sys.exit(0)




ev = eslog_viewer()
if __name__ == "__main__":
    log_file = "test:"
    print log_file
    print "sys.argv 0" , sys.argv[0]
    print "sys.argv 1" , sys.argv[1]
    if len(sys.argv) != 2:
        print " need cloudstack log file name!"
        exit(1)
    log_file = sys.argv[1]
    signal.signal(signal.SIGINT, handler)

    tlog = threading.Thread(target=thread_keyboard_monitor, args=(ev,))
    tlog.start()
    only_new = True
    tail = filetail.Tail(log_file, only_new)
    for line in tail:
        if ev.allow_running:
            ev.process_line(line)
        else:
            exit(0)
