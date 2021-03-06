# -*- coding: utf-8 -*-
import unittest
from bottle import Jinja2Template


class TestJinja2Template(unittest.TestCase):

    def test_string(self):
        """ Templates: Jinja2 string"""
        t = Jinja2Template('start {{var}} end').render(var='var')
        self.assertEqual('start var end', ''.join(t))

    def test_file(self):
        """ Templates: Jinja2 file"""
        t = Jinja2Template(name='./views/jinja2_simple.tpl').render(var='var')
        self.assertEqual('start var end', ''.join(t))

    def test_name(self):
        """ Templates: Jinja2 lookup by name """
        t = Jinja2Template(name='jinja2_simple', lookup=['./views/']).render(var='var')
        self.assertEqual('start var end', ''.join(t))

    def test_notfound(self):
        """ Templates: Unavailable templates"""
        self.assertRaises(Exception, Jinja2Template, name="abcdef")

    def test_error(self):
        """ Templates: Exceptions"""
        self.assertRaises(Exception, Jinja2Template, '{% for badsyntax')

    def test_inherit(self):
        """ Templates: Jinja2 lookup and inherience """
        t = Jinja2Template(name='jinja2_inherit', lookup=['./views/']).render()
        self.assertEqual('begin abc end', ''.join(t))

    def test_custom_filters(self):
        """Templates: jinja2 custom filters """
        from bottle import jinja2_template as template
        settings = dict(filters = {"star": lambda var: u"".join((u'*', var, u'*'))})
        t = Jinja2Template("start {{var|star}} end", **settings)
        self.assertEqual("start *var* end", t.render(var="var"))

    def test_custom_tests(self):
        """Templates: jinja2 custom tests """
        from bottle import jinja2_template as template
        TEMPL = u"""{% if var is even %}gerade{% else %}ungerade{% endif %}"""
        settings = dict(tests={"even": lambda x: False if x % 2 else True})
        t = Jinja2Template(TEMPL, **settings)
        self.assertEqual("gerade", t.render(var=2))
        self.assertEqual("ungerade", t.render(var=1))


try:
  import jinja2
except ImportError:
  print "WARNING: No Jinja2 template support. Skipping tests."
  del TestJinja2Template

if __name__ == '__main__': #pragma: no cover
    unittest.main()

