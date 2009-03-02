import clusto
from clusto.test import testbase 
import itertools

from clusto.drivers import *

from clusto.drivers.resources.simplenamemanager import SimpleNameManagerException



class SimpleEntityNameManagerTests(testbase.ClustoTestBase):

    def data(self):

        n1 = SimpleEntityNameManager('foonamegen',
                                     basename='foo',
                                     digits=4,
                                     startingnum=1,
                                     )


        n2 = SimpleEntityNameManager('barnamegen',
                                     basename='bar',
                                     digits=2,
                                     startingnum=95,
                                     )
        
        clusto.flush()

    def testNamedDriverCreation(self):
        ngen = clusto.getByName('foonamegen')
        
        s1 = ngen.allocate(Driver)

        clusto.flush()

        d1 = clusto.getByName('foo0001')

        self.assertEquals(s1.name, d1.name)
        
    def testAllocateName(self):

        ngen = clusto.getByName('foonamegen')
        
        s1 = ngen.allocate(Driver)
        s2 = ngen.allocate(Driver)
        s3 = ngen.allocate(Driver)
        s4 = ngen.allocate(Driver)

        clusto.flush()

        self.assertEqual(s1.name, 'foo0001')
        self.assertEqual(s2.name, 'foo0002')
        self.assertEqual(s3.name, 'foo0003')
        self.assertEqual(s4.name, 'foo0004')

    def testNoLeadingZeros(self):

        ngen = clusto.getByName('barnamegen')

        s1 = ngen.allocate(Driver)
        s2 = ngen.allocate(Driver)
        s3 = ngen.allocate(Driver)
        s4 = ngen.allocate(Driver)

        clusto.flush()

        self.assertEqual(s1.name, 'bar95')
        self.assertEqual(s2.name, 'bar96')
        self.assertEqual(s3.name, 'bar97')
        self.assertEqual(s4.name, 'bar98')

    def testTooManyDigits(self):
        
        ngen = clusto.getByName('barnamegen')

        s1 = ngen.allocate(Driver)
        s2 = ngen.allocate(Driver)
        s3 = ngen.allocate(Driver)
        s4 = ngen.allocate(Driver)

        s5 = ngen.allocate(Driver)
        self.assertRaises(SimpleNameManagerException,
                          ngen.allocate, Driver)


    def testAllocateManyNames(self):
        
        ngen = clusto.getByName('foonamegen')

        for i in xrange(50):
            ngen.allocate(Driver)

        self.assertRaises(LookupError, clusto.getByName, 'foo0051')
        self.assertEqual(clusto.getByName('foo0050').name, 'foo0050')


class SimpleNameManagerTests(testbase.ClustoTestBase):

    def data(self):
        n1 = SimpleNameManager('foonamegen',
                               basename='foo',
                               digits=4,
                               startingnum=1,
                               )

        clusto.flush()

    def testAllocateManyNames(self):
        
        ngen = clusto.getByName('foonamegen')

        d = Driver('foo')

        for i in xrange(50):
            ngen.allocate(d)
            
        
        self.assertEqual(ngen.attrQuery('resource', count=True), 50)