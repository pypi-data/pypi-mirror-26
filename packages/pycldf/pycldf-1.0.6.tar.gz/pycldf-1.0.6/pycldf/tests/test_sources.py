# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir
from clldutils.path import Path


FIXTURES = Path(__file__).parent.joinpath('fixtures')
BIB = """@BOOK{Obrazy,
    author = {Borovský, Karel Havlíček},
    title = {Obrazy z Rus}
}

@BOOK{Elegie,
    author = {Borovský, Karel Havlíček},
    title = {Tirolské elegie}
}
"""


class Tests(WithTempDir):
    def test_Sources(self):
        from pycldf.sources import Sources, Source

        src = Sources()
        src.add(BIB, Source(
            'book', 'huber2005', author='Herrmann Huber', year='2005', title='y'))
        self.assertEqual(len(list(src.items())), 3)
        self.assertEqual(len(list(src.keys())), 3)
        refs = ['huber2005[1-6]', 'Obrazy', 'Elegie[34]']
        self.assertEqual(src.format_refs(*list(src.expand_refs(refs))), refs)
        self.assertEqual('%s' % src['huber2005'], 'Huber, Herrmann. 2005. y.')
        with self.assertRaises(ValueError):
            src.add(5)
        with self.assertRaises(ValueError):
            src.add('@misc{a.b,\n  author="a.b"\n}')
        with self.assertRaises(ValueError):
            _ = src['unknown']
            assert _  # pragma: no cover
        with self.assertRaises(ValueError):
            src.parse('a[x')
        with self.assertRaises(ValueError):
            src.parse('[x]')
        with self.assertRaises(ValueError):
            src.validate(['x'])

        bib = self.tmp_path('test.bib')
        src.write(bib)

        src2 = Sources()
        src2.read(bib)

        bib = self.tmp_path('test.bib')
        src2.write(bib, ids=['huber2005'])
        src = Sources.from_file(bib)
        self.assertEqual(len(src), 1)

    def test_Source_from_bibtex(self):
        from pycldf.sources import Source

        bibtex = '@' + BIB.split('@')[1]
        self.assertEqual(Source.from_bibtex(bibtex).entry.fields['title'], 'Obrazy z Rus')

    def test_Sources_with_None_values(self):
        from pycldf.sources import Sources, Source

        src = Sources()
        src.add(Source('book', 'huber2005', title=None))
        src.write(self.tmp_path('test.bib'))

    def test_Source_expand_refs(self):
        from pycldf.sources import Sources, Source

        sources = Sources()
        src = Source(
            'book', 'Meier2005', author='Hans Meier', year='2005', title='The Book')
        self.assertIn('Meier2005', repr(src))
        sources.add(src)
        bib = sources._bibdata.to_string(bib_format='bibtex')
        self.assertEqual(len(bib.split('author')), 2)
        self.assertEqual(len(list(sources.expand_refs('Meier2005'))), 1)
        bib = sources._bibdata.to_string(bib_format='bibtex')
        self.assertEqual(len(bib.split('author')), 2)
        self.assertEqual(len(list(sources.expand_refs('12345'))), 1)

    def test_Reference(self):
        from pycldf.sources import Reference, Source

        ref = Reference(Source('book', 'huber2005', author='Herrmann Huber'), '2-5')
        self.assertIn('2-5', repr(ref))
        self.assertEqual('%s' % ref, 'huber2005[2-5]')
        with self.assertRaises(ValueError):
            Reference(Source('book', 'huber2005', author='Herrmann Huber'), '[2-5]')

    def test_Source_persons(self):
        from pycldf.sources import Source

        self.assertEqual(len(list(Source.persons('A. Meier'))), 1)
        self.assertEqual(len(list(Source.persons('Meier, A.B.'))), 1)
        self.assertEqual(len(list(Source.persons('A. Meier, B. Meier, C.Meier'))), 3)
