"""Testing the mathobjects.atom module."""

# Copyright Algebraix Data Corporation 2015 - 2017
#
# This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.
#
# algebraixlib is free software: you can redistribute it and/or modify it under the terms of version
# 3 of the GNU Lesser General Public License as published by the Free Software Foundation.
#
# algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
# If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------
import inspect
import os
import unittest

from algebraixlib.algebras.properties import is_functional, is_right_functional, is_bijective, \
    is_reflexive, is_symmetric, is_transitive, is_equivalence_relation
from algebraixlib.mathobjects import Atom, Couplet, MathObject, Multiset, Set
from algebraixlib.cache_status import CacheStatus
from algebraixlib.structure import GenesisSetA
from algebraixlib.undef import Undef

# noinspection PyUnresolvedReferences
from data_mathobjects import basic_atoms as ba


class AtomTest(unittest.TestCase):
    """Test the Atom class."""

    print_examples = False

    def test_atom(self):
        """Create various forms of Atoms."""
        if self.print_examples:
            print('(printing examples)')  # Make 'nosetests -s' more readable.
        for test_key in ba.keys():
            self._atom_assert(test_key)

    def _atom_assert(self, test_key):
        """Assert that 'test_atom' is a proper Atom (with test additions) with the value 'value'."""
        atom = ba[test_key]
        value = atom._test_val
        value_val = value
        while type(value_val) == Atom:
            value_val = value_val.value
        msg = atom._test_msg
        # Test the type structure.
        self.assertTrue(isinstance(atom, MathObject))
        self.assertTrue(isinstance(atom, Atom))
        self.assertFalse(isinstance(atom, Couplet))
        self.assertFalse(isinstance(atom, Set))
        # Compare the value and make sure it is not a MathObject.
        atom_value = atom.value
        self.assertFalse(isinstance(atom_value, MathObject))
        self.assertEqual(atom_value, value_val)
        # Make sure that the representations and string conversion of the atom and the value match.
        self.assertEqual(repr(atom), 'Atom({value})'.format(value=repr(value_val)))
        self.assertEqual(str(atom), repr(value_val))
        # Make sure that the representation evaluates to an atom that compares equal.
        repr_exec = 'self.assertEqual(atom, {0})'.format(repr(atom))
        exec(repr_exec)
        # Check the ground set.
        self.assertEqual(atom.get_ground_set(), GenesisSetA())
        # Test left set and functionality.
        self.assertIs(atom.get_left_set(), Undef())
        self.assertIs(is_functional(atom), Undef())
        self.assertIs(atom('callable'), Undef())
        # Print the representation and the string conversion.
        if self.print_examples:
            print('repr(Atom({msg})) = {repr}'.format(msg=msg, repr=repr(atom)))
            print('str(Atom({msg})) = {str}'.format(msg=msg, str=str(atom)))

    def test_equality(self):
        """Test equality concept of Atoms."""
        for value_key1, atom1 in ba.items():
            self._equality_assert(atom1, atom1)
            for value_key2, atom2 in ba.items():
                if value_key1 == value_key2:
                    self._equality_assert(atom1, atom2)
                else:
                    self._inequality_assert(atom1, atom2)
        self.assertNotEqual(Atom(True), Atom(1))
        self.assertNotEqual(Atom(True), 1)
        self.assertFalse(Atom(True) == 1)

    def test_less_than(self):
        for value_key1, atom1 in ba.items():
            for value_key2, atom2 in ba.items():
                self.assertNotEqual(atom1 < atom2, NotImplemented)
                self.assertNotEqual(atom2 < atom1, NotImplemented)
                if atom1 == atom2:
                    self.assertFalse(atom1 < atom2)
                    self.assertFalse(atom2 < atom1)
            for mo in [Couplet(1, 2), Multiset(1, 2, 3), Set(1, 2, 3)]:
                self.assertTrue(atom1 < mo)

    def test_invalid_constructs(self):
        """Test invalid Atoms."""
        self.assertRaises(TypeError, lambda: Atom(MathObject()))
        self.assertRaises(TypeError, lambda: Atom(Couplet(1, 2)))
        self.assertRaises(TypeError, lambda: Atom(Set()))
        self.assertRaises(TypeError, lambda: Atom(Undef()))
        self.assertRaises(TypeError, lambda: Atom([]))
        self.assertRaises(TypeError, lambda: Atom([7, '8']))
        self.assertRaises(TypeError, lambda: Atom({}))
        self.assertRaises(TypeError, lambda: Atom({'one': 9, 2: 'ten'}))

    def test_properties(self):
        a = ba['2']
        self.assertIs(a.get_left_set(), Undef())
        self.assertIs(is_functional(a), Undef())
        self.assertIs(a.get_right_set(), Undef())
        self.assertIs(is_right_functional(a), Undef())
        self.assertIs(is_bijective(a), Undef())
        self.assertIs(is_reflexive(a), Undef())
        self.assertIs(is_symmetric(a), Undef())
        self.assertIs(is_transitive(a), Undef())
        self.assertIs(is_equivalence_relation(a), Undef())

    def test_flags_cache(self):
        a = Atom(1)
        self.assertEqual(a.cached_relation, CacheStatus.IS_NOT)
        self.assertEqual(a.cached_clan, CacheStatus.IS_NOT)
        self.assertEqual(a.cached_multiclan, CacheStatus.IS_NOT)
        self.assertEqual(a.cached_functional, CacheStatus.N_A)
        self.assertEqual(a.cached_right_functional, CacheStatus.N_A)
        self.assertEqual(a.cached_regular, CacheStatus.N_A)
        self.assertEqual(a.cached_reflexive, CacheStatus.N_A)
        self.assertEqual(a.cached_symmetric, CacheStatus.N_A)
        self.assertEqual(a.cached_transitive, CacheStatus.N_A)

        self.assertRaises(AssertionError, lambda: a.cache_relation(CacheStatus.IS))
        self.assertRaises(AssertionError, lambda: a.cache_clan(CacheStatus.IS))
        self.assertRaises(AssertionError, lambda: a.cache_multiclan(CacheStatus.IS))

        self.assertRaises(Exception, lambda: a.cache_transitive(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: a.cache_functional(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: a.cache_right_functional(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: a.cache_regular(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: a.cache_reflexive(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: a.cache_symmetric(CacheStatus.IS_NOT))
        self.assertRaises(Exception, lambda: a.cache_transitive(CacheStatus.IS_NOT))

    def _equality_assert(self, at1, at2):
        """Check that at1 and at2 are properly equal."""
        self.assertEqual(at1, at2)
        self.assertTrue(at1 == at2)
        self.assertFalse(at1 != at2)

    def _inequality_assert(self, at1, at2):
        """Check that at1 and at2 are properly not equal."""
        self.assertNotEqual(at1, at2)
        self.assertTrue(at1 != at2)
        self.assertFalse(at1 == at2)

    def test_permutations(self):
        self.assertNotEqual(Atom(2), Atom(2.0))
        self.assertTrue(Atom(2) != Atom(2.0))
        self.assertFalse(Atom(2) == Atom(2.0))

        values = [None, bool(2), int(2), float(2), complex('1+2j'), str(2), bytes(2), range(-1, 5),
                  frozenset([None, None]), tuple((34, 35)), Atom(int(2)), Couplet(-1, -2),
                  Set('x', 'y', 'z')]
        test = Atom(frozenset(values))
        import itertools

        def top_n(n, generator):
            for _ in range(n):
                yield next(generator)
        # Test the first 100 permutations of values..frozenset sometimes orders differently
        # ..need to make sure that doesn't affect our equality check.
        for p in top_n(100, itertools.permutations(values)):
            act = Atom(frozenset(p))
            if act != test:
                print("exp", test)
                print("act", act)
            self.assertEqual(test, act)

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
