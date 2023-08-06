

# Incantation 


See [codes in Here](https://github.com/thautwarm/Incantation/tree/master/incantation)

This library is written by `flowpython`(so it just support Python 3.6.x now...), which makes the codes much more readable.

## A Simple Guide

Firstly, import some modules, you can find out what they are at [Materialize-CSS](http://materializecss.com/)

```python
from incantation.Module.CSS.Grid import container, col, row, grid, section
from incantation.Module.CSS.Color import Indigo 
from incantation.Module.CSS.Helpers import align, left_align, right_align, center_align
from incantation.Module.CSS.Media import video_container
from incantation.Module import abst
from incantation.Module import blockquote
from incantation.Module.CSS.Table import table
from incantation.Module.abst import default_conf, gen_helper, Seq
from incantation.template import Page
from incantation.Module.Component.Badges import collections, dropdown, badge, collapsible
from incantation.Module.Component.Icons import icon
from incantation.Module.Component.Button import FAB, raised
from incantation.Module.Component.Form import form, input_field
from incantation.Module.Component.Navbar import navbar

```

Then create a HTML page(it wll be automatically rendered by materialize-css).

```python
# create a container
main  = container()

# create a navbar. See more at http://materializecss.com/navbar.html.
nav = navbar(
       [dict(href = 'https://baidu.com',  name = 'link1'),
        dict(href = 'https://google.com', name = 'link2')
       ],
       href = 'https://github.com/thautwarm', 
       name = 'Logo'
       )

# create collections. See more at http://materializecss.com/badges.html.
cs = collections([badge(new = False,href = '#!', num = 1, name = 'Alan'),
                  badge(new = True, href = '#!', num = 4, name = 'Alan'),
                  badge(href = '#!', name = 'Alan'),
                  badge(new = False,href = '#!', num = 14,name = 'Alan')
                                ],
                                )

# create a dropdown. See more at http://materializecss.com/badges.html.
dd = dropdown([badge(new = False,href = '#!', num = 1, name = 'Alan'),
               badge(new = True, href = '#!', num = 4, name = 'Alan'),
               badge(href = '#!', name = 'Alan'),
               badge(new = False,href = '#!', num = 14,name = 'Alan')
                                ],
               name = 'a dropdown list', id = 'someid')

# create a collapsible. See more at http://materializecss.com/badges.html.
collap = collapsible([(icon('filter_drama'),badge(href = '#!', name = "First") , "<p>Lorem ipsum dolor sit amet.</p>"),
                      (icon('place'),       badge(href = '#!', name = "Second"), "place")
                     ])

# create 2 rows. See more at See http://materializecss.com/grid.html.
a_col = col("contents", grid(s=6) )
a_row = row(Seq(a_col, a_col), name = "test_row")
b_row = row(Seq(col(cs, grid(s=6)), col(cs, grid(s=6).loffset(s=0, m =6, l=8))))
center_align(a_row)

# create a table. See more at http://materializecss.com/table.html
a_table = table(
        ["name", "email", "phone number"],
        [
         ["thautwarm", "twshere@outlook.com", None],
         ["person1"  , "email1"             ,"phone1"], 
         ["deep"     , "dark"               ,"fantasy"],
         ["Ass"      , "Tol"                ,"Fo"]
        ],
        action = "somescirpt"
        ) 

try_columns = blockquote("Columns")
try_table   = blockquote("Tables") 

# create a fixed action button. See more at http://materializecss.com/buttons.html.
fab = FAB([dict(color = 'red',  icon = icon("insert_chart"),  href = 'https://www.baidu.com'),
           dict(color = 'blue', icon = icon("publish"),       href = 'https://www.google.com'),
          ], loc = 'fixed', color = 'purple', icon = icon("publish"))

# create a form. See more at http://materializecss.com/forms.html.
a_form = form(
            Seq(
            input_field(grid(s=12), field_name = 'Username', type = 'text',     icon = icon('mode_edit'), id = 'for-username'),
            input_field(grid(s=12), field_name = 'Password', type = 'password', icon = icon('brightness_auto'),   id = 'for-password'),
            input_field(grid(s=12), field_name = 'School',   type = 'text',     icon = icon('brightness_3'),   id = 'for-school'),
            input_field(grid(s=12), field_name = 'submit',   type = 'submit',   icon = icon('publish'),   id = 'for-submit')->> right_align,
            ),
            action = 'script',
            method = 'POST')
            
# let container contain a sequence of Incantation objects.
main.contains(Seq(try_columns, 
                  a_row, 
                  col(dd, grid(l = 12)),
                  collap, 
                  b_row, 
                  try_table, 
                  a_table, 
                  cs, 
                  fab, 
                  raised(icon = icon('add_alarm'), name = "YHZ", href = 'https://www.baidu.com'),
                  a_form
                  ))
# set indent recursively
main.setIndent(1)

# create a page and write it to some path.
page = Page( Seq(nav,main) )
page.write(to = './test.html')

```

See `test.html`
![rendered-1](https://github.com/thautwarm/Incantation/raw/master/test/test-p1.png)
![rendered-2](https://github.com/thautwarm/Incantation/raw/master/test/test-p2.png)
![rendered-3](https://github.com/thautwarm/Incantation/raw/master/test/test-p3.png)