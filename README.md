# alx-backend-storage
The view definition is “frozen” at creation time and is not affected by subsequent changes to the definitions of the underlying tables. For example, if a view is defined as SELECT * on a table, new columns added to the table later do not become part of the view, and columns dropped from the table result in an error when selecting from the view.
