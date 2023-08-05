# DateJS

## Convert Date from a JavaScript Date object to a Python DateTime object

## Usage

To use this library, you must first install the library (pip install datejs)

In your code, import DateJS

To convert JavaScript Date, initialize a DateJS object by doing `DateJS(JAVASCRIPT_DATE_STRING)`. The `JAVASCRIPT_DATE_STRING` can be determined by running `new Date().toString()` in JavaScript.

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
