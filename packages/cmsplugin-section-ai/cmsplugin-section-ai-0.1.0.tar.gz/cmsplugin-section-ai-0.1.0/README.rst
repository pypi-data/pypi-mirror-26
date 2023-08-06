Django CMS Section Plugin
=========================

A Django CMS container plugin for creating content sections.

This layout system relies on Bootstrap 4 and includes example SCSS styles that you can use with the plugin. To be able to use the SCSS files without modifications, you need to have the Bootstrap 4 variables included in your project.

It should be possible to just tweak the variables.less file to get the look and feel of your project.

Available with pip https://pypi.python.org/pypi/cmsplugin-section-ai

Features
--------

- Select the background image or background color for the section:

  - TRANSPARENT, CSS classname ``bg-color-transparent``
  - LIGHT_GRAY, CSS classname ``bg-color-light-gray``
  - PRIMARY, CSS classname ``bg-color-primary``
  - SECONDARY, CSS classname ``bg-color-secondary``

- Define the number of columns:

  - Single column
  - Two columns
  - Three columns
  - Four columns

- An optional title for each section

  - Justify title to left / center / right

- Adjust section vertical padding

  - Large / Medium / Small padding options for both top and bottom

- Select the container size

  - Options full-width / container / small container

- Add extra margin for the inner columns
- Align columns vertically to top / center / bottom
- Select if the content text should be centered
- Possibility to add an html ``id`` value for each section to enable anchor linking
- Possibility to add buttons with custom URLs and define the button sizes and styles:

  - PRIMARY, CSS classname ``btn-primary``
  - SECONDARY, CSS classname ``btn-secondary``
  - LIGHT, CSS classname ``btn-light``
  - DARK, CSS classname ``btn-dark``

- Justify buttons to left / center / right
