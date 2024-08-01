# Static Site Generator

# High-Level Overview

1. Markdown files are in the **/content** directory. A temporary **template.html**
   is in the root of the project.
2. The python code in **src/** (static site generator) reads the Markdown files and the template file.
3. The generator converts the Markdown files into a final HTML file for each page and writes them to the
   **/public** directory.
4. The built-in Python HTTP server (separate program) is started to serve the contents of the **/public**
   directory on **https://localhost:8888** (i.e., local machine).
5. Open a browser and navigate to **https://localhost:8888** to view the rendered site.

## How the SSG works

Vast majority of code is written in the **src/** directory because almost all work is done in steps 2 and 3 above.
Here is a rough outline of what the program will do when it runs:

1. Delete everything in the **/public** directory.
2. Copy any static assets (i.e., HTML template, CSS, images, etc.) to the **/public** directory.
3. Generate an HTML file for each Markdown file in the **/content** directory.

For each Markdown file:

1. Open the file and read its contents.
2. Split the markdown file into "blocks" (i.e., paragraphs, headings, lists, etc.).
3. Convert each block into a tree of **HTMLNode** objects. For inline elements (e.g., bold text, links, etc.)
   they are converted:
   - Raw markdown -> **TextNode** -> **HTMLNode**
4. Join all the **HTMLNode** "blocks" under one large parent **HTMLNode** for the pages.
5. Use a recursive **to_html()** method to convert the **HTMLNode** and all its nested nodes to a giant
   HTML string and inject it in the HTML template.
6. Write the full HTML string to a file for that page in the **/public** directory.

