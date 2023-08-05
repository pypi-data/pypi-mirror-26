# flexible-data-parser

This module is designed to convert semi-structured text data into Python dicts (or lists) by interpreting an XML configuration file.

## Usage

    from fdp import FileParser

    p = FileParser("/path/to/config.xml")
    parsed_dict = p.parse("/path/to/target.txt")

## Theory

The parser walks through the target text file one line at a time, comparing the current line with the regexes defined in the config file. Matching capture groups are stored according to the specified keys in the config file.

The process supports loops (if there are multiple instances of a kind of data stored in a single file). For example, a text invoice might have several line items, each broken out into three lines; in the config file, you can define a Section for each line item, with a separate regex for each line of text.

## XML Configuration

A sample configuration file is included.

### Section

Defines how to populate a list or dict with data.

*Attributes:*

* `name` - Key to store the list or dict under in above section
* `key` - [Optional] If defined, this section will be a dict, and will use the value of the specified key from child dicts as the index

*Contains:*

* `<repeat-until>` - [Optional] Text node; regex that signals the end of any further repeats of this section
* `<section>` - [Optional] Defines how to populate a list or dict with data
* `<line>` - [Optional] Defines how to match and capture data from a line of text

### Line

Defines how to match and capture data from a line of text

*Attributes:*

* `ignore` - [Optional] Boolean; if true, wait for this line to appear in the file, but do not save any capture groups.
* `optional` - [Optional] Boolean; if true, this line can be skipped if a match is found for the next line. (By default, no line can be skipped, and the parser will continue reading the target file until the next matching line is found.)

*Contains:*

* `<regex>` - Specifies the regex the line must match. Any capture groups will be saved.
* `<fields>` - Contains `<field>` elements
  * `<field>` - Specifies the key in which to store the data from the capture group(s). Must be a number of `<field>` elements equal to the number of capture groups.


