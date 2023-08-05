#!/usr/bin/env python3

import datetime
import pytz
import execjs

class DateJS():
    def __init__(self, JS_STRING):
        self.YEAR = 0
        self.MONTH = 0
        self.DATE = 0
        self.HOUR = 0
        self.MINUTE = 0
        self.SECOND = 0
        self.MILLISECONDS = 0
        self.TZ = None
        self.TZ_SIMPLE = None
        self.TZ_CUSTOM = None
        self.JS_TIME = JS_STRING
        self.PYTIME = datetime.datetime.now()
        self.PYTIME_SIMPLE = datetime.datetime.now()
        self.PYTIME_CUSTOM = datetime.datetime.now()
        self.CUSTOM_TIMEZONES = []
        self.ctx = None
        self.setCTX()
        self.setAllValues()

    def setCTX(self):
        self.ctx = execjs.compile("""
                function y(x){
                    return new Date(x).getFullYear();
                }
                function m(x){
                    return new Date(x).getMonth();
                }
                function d(x){
                    return new Date(x).getDate();
                }
                function h(x){
                    return new Date(x).getHours();
                }
                function i(x){
                    return new Date(x).getMinutes();
                }
                function s(x){
                    return new Date(x).getSeconds();
                }
                function l(x){
                    return new Date(x).getMilliseconds();
                }
                function t(x){
                    return new Date(x).getTimezoneOffset();
                }
            """)

    def setAllValues(self):
        self.setYear()
        self.setMonth()
        self.setDate()
        self.setHour()
        self.setMinute()
        self.setSecond()
        self.setMillisecond()
        self.setTZ()

    def getTime(self):
        self.PYTIME = self.PYTIME.replace(year=self.YEAR, month=self.MONTH, day=self.DATE, hour=self.HOUR, minute=self.MINUTE, second=self.SECOND, microsecond=self.MILLISECONDS, tzinfo=self.TZ)
        return self.PYTIME

    def getSimpleTime(self):
        self.PYTIME_SIMPLE = self.PYTIME_SIMPLE.replace(year=self.YEAR, month=self.MONTH, day=self.DATE, hour=self.HOUR, minute=self.MINUTE, second=self.SECOND, microsecond=self.MILLISECONDS, tzinfo=self.TZ_SIMPLE)
        return self.PYTIME_SIMPLE

    def getCustomTime(self):
        self.PYTIME_CUSTOM = self.PYTIME_CUSTOM.replace(year=self.YEAR, month=self.MONTH, day=self.DATE, hour=self.HOUR, minute=self.MINUTE, second=self.SECOND, microsecond=self.MILLISECONDS, tzinfo=self.TZ_CUSTOM)
        return self.PYTIME_CUSTOM

    def getYear(self):
        return self.YEAR

    def setYear(self):
        self.YEAR = self.ctx.call("y", self.JS_TIME)
        return

    def getMonth(self):
        return self.MONTH

    def setMonth(self):
        self.MONTH = self.ctx.call("m", self.JS_TIME) + 1 # This +1 moves month numbers from 0-11 to 1-12
        return

    def getDate(self):
        return self.DATE

    def setDate(self):
        self.DATE = self.ctx.call("d", self.JS_TIME)
        return

    def getHours(self):
        return self.HOUR

    def setHour(self):
        self.HOUR = self.ctx.call("h", self.JS_TIME)
        return

    def getMinutes(self):
        return self.MINUTE

    def setMinute(self):
        self.MINUTE = self.ctx.call("i", self.JS_TIME)
        return

    def getSeconds(self):
        return self.SECOND

    def setSecond(self):
        self.SECOND = self.ctx.call("s", self.JS_TIME)
        return

    def getMilliseconds(self):
        return self.MILLISECONDS

    def setMillisecond(self):
        self.MILLISECONDS = self.ctx.call("l", self.JS_TIME)
        return

    def getTimezone(self):
        return self.TZ

    def getSimpleTimezone(self):
        return self.TZ_SIMPLE

    def getCustomTimezone(self):
        return self.TZ_CUSTOM

    def setTZ(self):
        offset = self.ctx.call("t", self.JS_TIME)
        offset = self.offsetFormat(offset)
        sorted_tzs = self.allTimezones()
        for zone in sorted_tzs:
            if offset in zone[1]:
                self.TZ = pytz.timezone(zone[0])
                break
        simple_tzs = self.basicTimezones()
        for z in simple_tzs:
            if offset in z[1]:
                self.TZ_SIMPLE = pytz.timezone(z[0])
                break
        custom_tzs = self.CUSTOM_TIMEZONES
        if custom_tzs == []:
            return
        for w in custom_tzs:
            if offset in w[1]:
                self.TZ_CUSTOM = pytz.timezone(w[0])
                return
        raise Exception("No Timezone Found!")

    def offsetFormat(self, offset):
        west = True
        if offset == "-":
            west = False
        hours_offset = int(offset/60)
        if abs(hours_offset) < 10:
            hours_offset = "0" + str(hours_offset)
        minutes_offset = int(offset%60)
        if minutes_offset < 10:
            minutes_offset = "0" + str(minutes_offset)
        if west:
            return "-" + str(hours_offset) + str(minutes_offset)
        return str(hours_offset) + str(minutes_offset)

    def allTimezones(self):
        tz = [(item, datetime.datetime.now(pytz.timezone(item)).strftime('%z') + " " + item) for item in pytz.common_timezones]
        sorted_tzs = sorted(tz, key=lambda x: int(x[1].split()[0]))
        return sorted_tzs

    def basicTimezones(self):
        SHORT_LIST_TIMEZONES = [('Pacific/Midway', '-1100 Pacific/Midway'), ('US/Hawaii', '-1000 US/Hawaii'), ('Pacific/Marquesas', '-0930 Pacific/Marquesas'), ('Pacific/Gambier', '-0900 Pacific/Gambier'), ('US/Alaska', '-0800 US/Alaska'), ('US/Pacific', '-0700 US/Pacific'), ('US/Mountain', '-0600 US/Mountain'), ('US/Central', '-0500 US/Central'), ('US/Eastern', '-0400 US/Eastern'), ('America/Argentina/Buenos_Aires', '-0300 America/Argentina/Buenos_Aires'),   ('Canada/Newfoundland', '-0230 Canada/Newfoundland'), ('America/Sao_Paulo', '-0200 America/Sao_Paulo'), ('Atlantic/Cape_Verde', '-0100 Atlantic/Cape_Verde'), ('UTC', '+0000 UTC'), ('Europe/London', '+0100 Europe/London'),  ('Europe/Paris', '+0200 Europe/Paris'), ('Europe/Moscow', '+0300 Europe/Moscow'), ('Asia/Tehran', '+0330 Asia/Tehran'), ('Asia/Dubai', '+0400 Asia/Dubai'), ('Asia/Kabul', '+0430 Asia/Kabul'), ('Asia/Karachi', '+0500 Asia/Karachi'), ('Asia/Kolkata', '+0530 Asia/Kolkata'), ('Asia/Kathmandu', '+0545 Asia/Kathmandu'), ('Asia/Dhaka', '+0600 Asia/Dhaka'), ('Indian/Cocos', '+0630 Indian/Cocos'), ('Asia/Bangkok', '+0700 Asia/Bangkok'), ('Asia/Hong_Kong', '+0800 Asia/Hong_Kong'), ('Asia/Pyongyang', '+0830 Asia/Pyongyang'), ('Australia/Eucla', '+0845 Australia/Eucla'), ('Asia/Tokyo', '+0900 Asia/Tokyo'),  ('Australia/Darwin', '+0930 Australia/Darwin'), ('Australia/Brisbane', '+1000 Australia/Brisbane'),  ('Australia/Adelaide', '+1030 Australia/Adelaide'), ('Australia/Sydney', '+1100 Australia/Sydney'), ('Pacific/Fiji', '+1200 Pacific/Fiji'), ('Pacific/Auckland', '+1300 Pacific/Auckland'), ('Pacific/Chatham', '+1345 Pacific/Chatham'), ('Pacific/Kiritimati', '+1400 Pacific/Kiritimati')]
        return SHORT_LIST_TIMEZONES

    def setcustomTimezones(self, CUSTOM_LIST):
        self.TZ_CUSTOM = CUSTOM_LIST
        return
