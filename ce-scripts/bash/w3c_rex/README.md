# Instructions document for using test_rex_books.sh script

## Purpose

This script was created when working on a self-closing tag issue within the 
cnxmlutils repository. There is a related python script that helps search for
self-closing tags via cnx-archive. This is primarily an issue of rendering xhtml
when rex-web renders html. Self-closing tags are not invalid in xhtml. 
Therefore, in https://cnx.org self-closing tags should not cause any visible 
changes, however, in rex-web there is increased risk for changes because it renders html.

### TL;DR

The team worked on self-closing tag issue in cnxmlutils. This issue affected all
the books and had to be tested thoroughly. Additionally, since rex-web uses 
content from archive and renders it in html there is increased risk for content to look funky.

## Prerequisites

> Note: These instructions assume OSX is the OS. Adapt the steps accordingly to your OS if it differs.

* Homebrew
* node
* Java
* rex-web (install instructions [here][rex-web])

## Install necessary application and packages

Install vnu using brew:

	$ brew install vnu

Install the html-validator-cli using yarn:

	$ yarn global add html-validator-cli

### Prepare rex-web

> Note: All the following actions are taken within the rex-web source code located locally.

Change directories to where you have cloned rex-web.

Comment out the following line in the rex-web source code:

[https://github.com/openstax/rex-web/blob/master/src/app/content/components/Page.tsx#L57][line-comment]

Adjust what books you want to prerender in `src/config.js`. If all the books are used the process can be lengthy.

Build the project:

	$ REACT_APP_ENV=development yarn build

Pre-render the pages to the books selected in `src/config.js`:

	REACT_APP_ENV=development yarn prerender

Start the server:

	yarn start

## Run the script

> Note: Ensure you have rex-web running locally first!

Run the vnu server:

	$ java -cp /usr/local/Cellar/vnu/18.11.5/libexec/vnu.jar nu.validator.servlet.Main 8888

Change directories into the w3c_rex directory

Run the script:

	$ BOOKS_PATH=/path/to/rex/rex-web/build/books ./w3c_rex.sh

Examine the results in `results.txt`

[rex-web]: https://github.com/openstax/rex-web
[line-comment]: https://github.com/openstax/rex-web/blob/master/src/app/content/components/Page.tsx#L57
