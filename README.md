# Visma InSchool timetable to iCalendar

This is a python script that downloads a timetable from Visma InSchool and converts it to an iCalendar `.ics` file.

I have tested the iCalendar files generated in Thunderbird, Google calendar and Korganizer.

## iCalendar
iCalendar is a standardzed format for storing calendars. It is supported by almost all calendar programs. If you double click on an iCalendar file in your file explorer, it will most likley be opened in the default calendar program on your system.

It can also most likley be imported in the web interface for your online calendar provider.

## Setup
### Authorization
Obviously, Visma has authentication. When you log in the Visma website will handle out a cookie called `Authorization`. There exists different ways to get the values of cookies in your web browser. Since this depends upon you web browser and there are different ways to do it, I will not provide instructions on how to obtain cookies here. A simple web search for `How to view cookies in <web browser>` should suffice.

### VIS-ID
Your VIS-ID is also needed. In the sidebar, navigate to `Students > Personal` or `Elever > Personalia`. (Language dependent)

### FQDN
FQDN = Fully Qualified Domain Name

In the address bar of your web browser the FQDN will be the part after `HTTPS://` and before the first `/`

For example: here is my fqdn: `kvadraturen-vgs.inschool.visma.no`

### settings.json
Add `fqdn`, `Authorization` and `VIS-ID` to `settings.json`.

### Categories
You can replace the `null` in `"Categories"` with a comma seperated list of categories like:

`"School"` or `"School,Skole"`

This will set the iCalendar categories.

## Usage
Run `python timetable.py` in a terminal.

It will write out the raw iCalendar file with the timetable for the current week in the terminal and create a .ics file with the the current date in ISO 8601 format (yyyy-mm-dd) for example: `2022-02-16.ics`

You can also run `python timetable.py` with a date in dd/mm/yyyy format after it to get the timetable for the associated week.
For example: `python timetable.py 16/02/2022`

## Future
Make it possible to change how the description is created.

