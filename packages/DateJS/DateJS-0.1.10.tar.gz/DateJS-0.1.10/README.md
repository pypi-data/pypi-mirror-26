# DateJS

## Convert Date from a JavaScript Date object to a Python DateTime object

## Usage

To use this library, you must first install the library (pip install DateJS)

In your code, you must import DateJS package by including `from DateJS import DateJS`.

To convert JavaScript Date, initialize a DateJS object by doing `DateJS.DateJS(JAVASCRIPT_DATE_STRING)`, where the `JAVASCRIPT_DATE_STRING` can be determined by running `new Date().toString()` in JavaScript.

## Get Values

You can access a wide array of values by calling one of the following methods:

#### Year -> `getYear()`
#### Month -> `getMonth()`
#### Date -> `getDate()`
#### Hours -> `getHours()`
#### Minutes -> `getMinutes()`
#### Seconds -> `getSeconds()`
#### Milliseconds -> `getMilliseconds()`
#### Common Timezone (From pytz.common_timezones) -> `getTimezone()`
#### Simple Timezone (From pre-determined list of all common timezones) -> `getSimpleTimezone()`

## Common Errors

If you get a JavaScript Runtime Error, you can fix this by running `sudo apt-get install nodejs`. This will configure the JavaScript Runtime Environment.

## Examples

```python
from DateJS import DateJS

dJS = DateJS.DateJS("Thu Oct 19 2017 21:50:06 GMT-0400 (Eastern Daylight Time)")

dJS.getTime() # Get datetime object of time with timezone data

dJS.getTimezone() # Returns a timezone object from pytz

dJS.getSimpleTime() # Returns most common timezone object from pytz

```

## Unnoticed Errors

If you would like to report any errors, please open an issue. If you know how to fix the issue, please submit appropiate changes.
