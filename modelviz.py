#!/usr/bin/env python
"""Django model to DOT (Graphviz) converter
by Antonio Cavedoni <antonio@cavedoni.org>

Make sure your DJANGO_SETTINGS_MODULE is set to your project and call 
the script like this:

$ python modelviz.py <app_label> > <filename>.dot
"""

__version__ = "0.6"
__svnid__ = "$Id$"
__license__ = "Python"
__author__ = "Antonio Cavedoni <http://cavedoni.com/>"
__contributors__ = [
   "Stefano J. Attardi <http://attardi.org/>",
   "limodou <http://www.donews.net/limodou/>",
   "Carlo C8E Miron"
   ]

from django.db import models
from django.db.models import get_models
from django.db.models.fields.related import \
    ForeignKey, OneToOneField, ManyToManyField
from django.db.models.fields.generic import GenericRelation
from django.template import Template, Context

dot_template = """
digraph {{ name }} {
  fontname = "Helvetica"
  fontsize = 8

  node [
    fontname = "Helvetica"
    fontsize = 8
    shape = "plaintext"
  ]
   edge [
    fontname = "Helvetica"
    fontsize = 8
  ]

  {% for model in models %}
  {{ model.name }} [label=<
    <TABLE BGCOLOR="palegoldenrod" BORDER="0" CELLBORDER="0" CELLSPACING="0">
     <TR><TD COLSPAN="2" CELLPADDING="4" ALIGN="CENTER" BGCOLOR="olivedrab4"
     ><FONT FACE="Helvetica Bold" COLOR="white"
     >{{ model.name }}</FONT></TD></TR>
     {% for field in model.fields %}
     <TR><TD ALIGN="LEFT" BORDER="0"
     ><FONT FACE="Helvetica Bold">{{ field.name }}</FONT
     ></TD>
     <TD ALIGN="LEFT">{{ field.type }}</TD></TR>
     {% endfor %}
    </TABLE>
    >]
   
  {% for relation in model.relations %}
  {{ model.name }} -> {{ relation.target }} 
    [label="{{ relation.type }}"] {{ relation.arrows }};
  {% endfor %}
  {% endfor %}
}
"""

def generate_dot(app_label):
   app = models.get_app(app_label)
   graph = Context({
      'name': '"%s"' % app.__name__, 
      'models': []
      })

   for appmodel in get_models(app):
      model = {
         'name': appmodel.__name__,
         'fields': [],
         'relations': []
         }

      # model attributes
      def add_attributes():
         model['fields'].append({
               'name': field.name,
               'type': type(field).__name__
               })

      for field in appmodel._meta.fields:
         add_attributes()
         
      if appmodel._meta.many_to_many:
         for field in appmodel._meta.many_to_many:
            add_attributes()

      # relations
      def add_relation(extras=""):
         _rel = {
            'target': field.rel.to.__name__,
            'type': type(field).__name__,
            'arrows': extras
            }
         if _rel not in model['relations']:
            model['relations'].append(_rel)

      for field in appmodel._meta.fields:
         if isinstance(field, ForeignKey):
            add_relation()
         elif isinstance(field, OneToOneField):
            add_relation("[arrowhead=none arrowtail=none]")

      if appmodel._meta.many_to_many:
         for field in appmodel._meta.many_to_many:
            if isinstance(field, ManyToManyField):
               add_relation("[arrowhead=normal arrowtail=normal]")
            elif isinstance(field, GenericRelation):
               add_relation(
                  '[style="dotted"] [arrowhead=normal arrowtail=normal]')
      graph['models'].append(model)
   
   t = Template(dot_template)
   return t.render(graph)

if __name__ == "__main__":
   import sys
   try:
      app_label = sys.argv[1]
      print generate_dot(app_label)
   except IndexError:
      print __doc__
