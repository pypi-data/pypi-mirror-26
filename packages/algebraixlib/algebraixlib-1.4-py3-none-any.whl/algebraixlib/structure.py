r"""
The Structure of a `MathObject`
===============================

This module provides facilities to represent the structure of a `MathObject`. What we call
'structure' is a representation of the minimal :term:`power set` a given `MathObject` belongs to
(or should belong to) that can be expressed with the following elements.

The structural elements we use are:

-   `CartesianProduct`: The :term:`ground set` of a :class:`~.Couplet` is the :term:`Cartesian
    product` of the ground sets of the :term:`left` and :term:`right component`.
-   `PowerSet`: The ground set of a :term:`set` is the :term:`power set` of the ground set of its
    elements.
-   :class:`~Union`: The ground set of the elements of a :term:`set` is the :term:`union` of the
    ground sets of the individual elements.

Depending on the type of structure, we use one or two genesis sets:

-   `GenesisSetA`: The :term:`set A` (:math:`A`) is the :term:`set` of all :class:`~.Atom`\s.
-   `GenesisSetM`: The term:`set M` (:math:`M`) is the ground set of all `MathObject`\s that can be
    represented in a given system.

In addition to these, there is the structure of an empty set. It is represented by an instance of
`Structure` and is the only case that is represented by an instance of that class. It is a subset
of all other structures.

.. note:: The :term:`set M` (:math:`M`) is finite; essentially it is the set of all instances of
    `MathObject` that fit into a given system. This also implies that there is a power set
    :math:`P(M)` that is *not* an element of :math:`M`. (It follows that not *every* 'set of math
    objects' is an element of :math:`M`.) Since :math:`A \subset M`, :math:`A` is of course also
    finite.

Corresponding to the two genesis sets, we use two different forms to represent the structure of a
`MathObject`:

-   **Absolute structure**: An :term:`absolute` structure does not contain a reference to the set
    :math:`M`.
-   **Relative structure**: A relative structure contains a reference to the set :math:`M`. Such
    structures are typically used to compare absolute structures against them, to see whether a
    given absolute structure fulfills a minimal structural criterion.

Example Code
============

.. code::

    from algebraixlib.mathobjects import Set
    from algebraixlib.structure import PowerSet, GenesisSetM
    Set([1, 2]).get_ground_set()
    # Output: PowerSet(GenesisSetA())
    Set([1, 2]).get_ground_set().is_subset(PowerSet(GenesisSetM()))
    # Output: True

API
===

"""

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
import abc as _abc
import collections as _collections

import algebraixlib.util.miscellaneous as _misc


# --------------------------------------------------------------------------------------------------

class Structure(object):
    """Represent the :term:`ground set` of a `MathObject` in structural terms. An instance of this
    class is the empty :term:`set`.

    .. note:: This class serves a double purpose. On one hand it is the base class for all nodes in
        the structure tree, and on the other hand it is the representative of the whole tree (where
        the top level node of the tree of interest is typically a subclass of this class). This
        is common practice and should not pose a problem, but it is probably helpful to be aware of
        it.
    """
    @_abc.abstractmethod
    def is_subset(self, other) -> bool:
        """Return ``True`` if ``self`` is a subset of ``other``.

        :param other: Must be an instance of `Structure`.
        :return: Is always ``True`` for type `Structure`.
        """
        assert isinstance(other, Structure)
        return True

    @_abc.abstractmethod
    def get_powerset_level(self, other) -> int:
        """Return the number of power set levels between ``self`` and ``other``.

        :param other: Must be an instance of `Structure`.
        :return: An integer >= 0. Is always 0 for type `Structure`.
        """
        assert isinstance(other, Structure)
        return 0

    @_abc.abstractmethod
    def is_same(self, other) -> bool:
        """Return ``True`` if ``self`` is structurally equivalent to ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is structurally equivalent to ``other``.
        """
        assert isinstance(other, Structure)
        return type(other) == Structure

    # ----------------------------------------------------------------------------------------------

    def __eq__(self, other):
        """Map to `is_same`. Is called for the operator ``==``."""
        return self.is_same(other)

    def __ne__(self, other):
        """Map to the negation of `is_same`. Is called for the operator ``!=``."""
        return not self.is_same(other)

    def __le__(self, other):
        """Map to `is_subset`. Is called for the operator ``<=``."""
        return self.is_subset(other)

    @_abc.abstractmethod
    def __hash__(self):
        """Return a hash based on the member values. (It must match the implementation of `is_same`,
        to which `__eq__` redirects equality comparisons.)
        """
        return hash(_misc.get_full_class_name(self))

    @_abc.abstractmethod
    def __repr__(self):
        """Return the instance's code representation."""
        return 'Structure()'

    @_abc.abstractmethod
    def __str__(self):
        """Return the instance's string representation."""
        return '{}'


class GenesisSetA(Structure):
    r"""The set of all :term:`atom`\s. Is functionally a singleton."""

    def is_subset(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is a subset of ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is a subset of ``other``.
        """
        assert isinstance(other, Structure)
        return type(other) == GenesisSetA or type(other) == GenesisSetM

    def get_powerset_level(self, other: Structure) -> int:
        """Return the number of power set levels between ``self`` and ``other``.

        :param other: Must be an instance of `Structure`.
        :return: An integer >= 0. Is always 0 for type `GenesisSetA`.
        """
        assert isinstance(other, Structure)
        return 0

    def is_same(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is structurally equivalent to ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is structurally equivalent to ``other``.
        """
        assert isinstance(other, Structure)
        return type(other) == GenesisSetA

    # ----------------------------------------------------------------------------------------------

    def __hash__(self):
        """Return a hash based on the member values. (It must match the implementation of `is_same`,
        to which `Structure.__eq__` redirects equality comparisons.)
        """
        return hash(_misc.get_full_class_name(self))

    def __repr__(self):
        """Return the instance's code representation."""
        return 'GenesisSetA()'

    def __str__(self):
        """Return the instance's string representation."""
        return 'A'


class GenesisSetM(Structure):
    r"""The set of all instances of `MathObject`. Is functionally a singleton.

    .. note:: The set :math:`M` being a superset of :math:`A` means that subset checking (especially
        in :class:`~Union`) needs to 'know' about this relationship and take it into account.
        Representing :math:`M` as :math:`(A \cup A')` (where :math:`A' = M \setminus A`) would make
        this more straightforward, but would make the visible representation of :math:`M` (as union)
        non-intuitive.
    """

    def is_subset(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is a subset of ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is a subset of ``other``.
        """
        assert isinstance(other, Structure)
        return type(other) == GenesisSetM

    def get_powerset_level(self, other):
        """Return the number of power set levels between ``self`` and ``other``.

        :param other: Must be an instance of `Structure`.
        :return: An integer >= 0. Is always 0 for type `GenesisSetM`.
        """
        assert isinstance(other, Structure)
        return 0

    def is_same(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is structurally equivalent to ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is structurally equivalent to ``other``.
        """
        assert isinstance(other, Structure)
        return type(other) == GenesisSetM

    # ----------------------------------------------------------------------------------------------

    def __hash__(self):
        """Return a hash based on the member values. (It must match the implementation of `is_same`,
        to which `Structure.__eq__` redirects equality comparisons.)
        """
        return hash(_misc.get_full_class_name(self))

    def __repr__(self):
        """Return the instance's code representation."""
        return 'GenesisSetM()'

    def __str__(self):
        """Return the instance's string representation."""
        return 'M'


class GenesisSetN(Structure):
    r"""The set of all integers. Is functionally a singleton."""

    def is_subset(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is a subset of ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is a subset of ``other``.
        """
        assert isinstance(other, Structure)
        return type(other) == GenesisSetN

    def get_powerset_level(self, other):
        """Return the number of power set levels between ``self`` and ``other``.

        :param other: Must be an instance of `Structure`.
        :return: An integer >= 0. Is always 0 for type `GenesisSetN`.
        """
        assert isinstance(other, Structure)
        return 0

    def is_same(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is structurally equivalent to ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is structurally equivalent to ``other``.
        """
        assert isinstance(other, Structure)
        return type(other) == GenesisSetN

    # ----------------------------------------------------------------------------------------------

    def __hash__(self):
        """Return a hash based on the member values. (It must match the implementation of `is_same`,
        to which `Structure.__eq__` redirects equality comparisons.)
        """
        return hash(_misc.get_full_class_name(self))

    def __repr__(self):
        """Return the instance's code representation."""
        return 'GenesisSetN()'

    def __str__(self):
        """Return the instance's string representation."""
        return 'N'


class CartesianProduct(Structure):
    """Represent the :term:`Cartesian product` node of a structure."""

    def __init__(self, left, right):
        """
        :param left: The :term:`ground set` of the :term:`left component` of a :term:`couplet`. Must
            be an instance of `Structure`.
        :param right: The ground set of the :term:`right component` of a couplet. Must be an
            instance of `Structure`.
        """
        right_is_struct = isinstance(right, Structure)
        right_not_struct = type(right) != Structure
        assert right_is_struct and right_not_struct
        self._left = left
        self._right = right

    @property
    def left(self) -> Structure:
        """Read-only access to the :term:`left` structure."""
        return self._left

    @property
    def right(self) -> Structure:
        """Read-only access to the :term:`right` structure."""
        return self._right

    def is_subset(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is a subset of ``other``.

        In order for ``self`` to be a :term:`subset` of ``other``, ``other`` must be:

        -   A `CartesianProduct` and both left and right components must be subsets of left and
            right components of ``other``, or
        -   A :class:`~Union` that contains an instance of `CartesianProduct` where both left and
            right component are subsets of left and right components of ``other``, or
        -   `GenesisSetM` (everything in our system is a subset of :math:`M`).

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is a :term:`subset` of ``other``.
        """
        assert isinstance(other, Structure)

        def is_subset_of_cart_prod(cart_prod: CartesianProduct):
            return (self.left <= cart_prod.left) and (self.right <= cart_prod.right)

        if isinstance(other, GenesisSetM):
            return True
        elif isinstance(other, CartesianProduct):
            return is_subset_of_cart_prod(other)
        elif isinstance(other, Union):
            for union_elem in other.data:
                if isinstance(union_elem, CartesianProduct):
                    if is_subset_of_cart_prod(union_elem):
                        return True
        return False

    def get_powerset_level(self, other: Structure) -> int:
        """Return the number of power set levels between ``self`` and ``other``.

        :param other: Must be an instance of `Structure`.
        :return: An integer >= 0. Is always 0 for type `CartesianProduct`.
        """
        assert isinstance(other, Structure)
        return 0

    def is_same(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is structurally equivalent to ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is structurally equivalent to ``other``.
        """
        assert isinstance(other, Structure)
        if isinstance(other, CartesianProduct):
            return (self.left == other.left) and (self.right == other.right)
        return False

    # ----------------------------------------------------------------------------------------------

    def __hash__(self):
        """Return a hash based on the member values. (It must match the implementation of `is_same`,
        to which `Structure.__eq__` redirects equality comparisons.) Is always cached.
        """
        return _misc.get_hash(_misc.get_full_class_name(self), self.left, self.right)

    def __repr__(self):
        """Return the instance's code representation."""
        return 'CartesianProduct(left={left}, right={right})'.format(
            left=repr(self.left), right=repr(self.right))

    def __str__(self):
        """Return the instance's string representation."""
        return '({left} x {right})'.format(left=str(self.left), right=str(self.right))


class Union(Structure):
    """Represent the :term:`union` node of a structure.

    No member of this instance is a :term:`subset` of another member, and no member of this union
    is a union itself (union arguments get 'unioned into' this union).
    """

    def __init__(self, iterable):
        """
        :param iterable: An `Iterable
            <https://docs.python.org/3.4/library/collections.abc.html?highlight=iterable#collections.abc.Iterable>`_
            of one or more sets to be unioned. All elements must be an instance of `Structure`.
        """
        assert isinstance(iterable, _collections.Iterable)

        def _add_element(new_element):
            """Add an element (a Structure) to the union if it is not already in it."""
            assert isinstance(new_element, Structure)
            for existing_element in writeable_union:
                if new_element.is_subset(existing_element):
                    # To be added element is subset of existing element: nothing to add.
                    break
                elif existing_element.is_subset(new_element):
                    # To be added element is (real) superset of existing element: exchange them.
                    writeable_union.remove(existing_element)
                    writeable_union.add(new_element)
                    break
            else:
                # To be added element is neither subset nor superset of existing: add it.
                writeable_union.add(new_element)

        writeable_union = set()
        for new_structure in iterable:
            if isinstance(new_structure, Union):
                # If the structure to be added is a union, add it element by element.
                for element in new_structure.data:
                    _add_element(element)
            else:
                _add_element(new_structure)
        assert len(writeable_union) > 0
        self._data = frozenset(writeable_union)

    @property
    def data(self) -> frozenset:
        """Read-only access to the raw collection (`frozenset`) of the union members."""
        return self._data

    def is_subset(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is a :term:`subset` of ``other``.

        Is ``True`` if every element of this :term:`union` is a subset of ``other``:

        -   If ``other`` is a union, we compare against each element of it.
        -   If ``other`` is not a union, we compare directly against it.

        Is also ``True`` if ``other`` is `GenesisSetM` (everything in our system is an element of
        :math:`M`).

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is a subset of ``other``.
        """
        assert isinstance(other, Structure)

        def is_subset_of_union(elem, union):
            for union_elem in union:
                if elem.is_subset(union_elem):
                    return True  # If elem is a subset of any element of union, return True.
            return False  # Only return False if elem is not a subset of any element of union.

        if isinstance(other, GenesisSetM):
            return True
        elif isinstance(other, Union):
            for element in self.data:
                if not is_subset_of_union(element, other.data):
                    return False  # If any element is not a subset of other, return False.
        else:
            for element in self.data:
                if not element.is_subset(other):
                    return False  # If any element is not a subset of other, return False.
        return True  # Only return True if all elements are a subset of other.

    def get_powerset_level(self, other: Structure) -> int:
        """Return the number of power set levels between ``self`` and ``other``.

        :param other: Must be an instance of `Structure`.
        :return: An integer >= 0. Is always 0 for type `CartesianProduct`.
        """
        assert isinstance(other, Structure)
        return 0

    def is_same(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is structurally equivalent to ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is structurally equivalent to ``other``.
        """
        assert isinstance(other, Structure)
        if isinstance(other, Union):
            return self.data == other.data
        else:
            if len(self.data) == 1:
                # Compare the one element against 'other'.
                return _misc.get_single_iter_elem(self.data).is_same(other)
            else:
                # self is a 'real' union, so the 'other' must also be a union.
                return False

    # ----------------------------------------------------------------------------------------------

    def __hash__(self):
        """Return a hash based on the member values. (It must match the implementation of `is_same`,
        to which `Structure.__eq__` redirects equality comparisons.) Is always cached.
        """
        return _misc.get_hash(_misc.get_full_class_name(self), self.data)

    def __repr__(self):
        """Return the instance's code representation."""
        unsorted_strings = [repr(elem) for elem in self.data]
        return 'Union([{elems}])'.format(elems=', '.join(elem for elem in sorted(unsorted_strings)))

    def __str__(self):
        """Return the instance's string representation."""
        if len(self.data) == 1:
            return str(_misc.get_single_iter_elem(self.data))
        else:
            unsorted_strings = [str(elem) for elem in self.data]
            return '({elems})'.format(elems=' U '.join(elem for elem in sorted(unsorted_strings)))


class PowerSet(Structure):
    """Represent the :term:`power set` node of a structure."""

    def __init__(self, elements_struct):
        """
        :param elements_struct: The structure of the elements of the :term:`set` of which we are
            representing the power set. Must be an instance of `Structure`.
        """
        assert isinstance(elements_struct, Structure)
        self._base_set = elements_struct

    @property
    def base_set(self) -> Structure:
        """Read-only access to the base set of this powerset."""
        return self._base_set

    def is_subset(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is a :term:`subset` of ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is a subset of ``other``.
        """
        assert isinstance(other, Structure)
        if isinstance(other, GenesisSetM):
            return True
        elif isinstance(other, PowerSet):
            return self._base_set.is_subset(other._base_set)
        return False

    def get_powerset_level(self, other: Structure) -> int:
        """Return the number of :term:`power set` levels between ``self`` and ``other``.

        :param other: Must be an instance of `Structure`.
        :return: The number of power set levels (>= 0) that are between ``self`` and ``other``.
            A result of 0 may mean that the two ground sets are equal or that they are not related.
        """

        def recurse_through_powerset_levels(structure_under_test, powerset_level=0):
            if type(structure_under_test) != PowerSet:
                return 0
            powerset_level += 1
            if structure_under_test.base_set.is_subset(other):
                return powerset_level
            return recurse_through_powerset_levels(structure_under_test.base_set, powerset_level)

        return recurse_through_powerset_levels(self)

    def is_same(self, other: Structure) -> bool:
        """Return ``True`` if ``self`` is structurally equivalent to ``other``.

        :param other: Must be an instance of `Structure`.
        :return: ``True`` if ``self`` is structurally equivalent to ``other``.
        """
        assert isinstance(other, Structure)
        if isinstance(other, PowerSet):
            return self._base_set == other._base_set
        return False

    # ----------------------------------------------------------------------------------------------

    def __hash__(self):
        """Return a hash based on the member values. (It must match the implementation of `is_same`,
        to which `Structure.__eq__` redirects equality comparisons.) Is always cached.
        """
        return _misc.get_hash(_misc.get_full_class_name(self), self.base_set)

    def __repr__(self):
        """Return the instance's code representation."""
        return 'PowerSet({elems})'.format(elems=repr(self._base_set))

    def __str__(self):
        """Return the instance's string representation."""
        elem_str = str(self._base_set)
        # If the base set starts with a P (PowerSet) or a parenthesis, don't add parentheses.
        if elem_str[0] == 'P' or elem_str[0] == '(':
            return 'P{elem}'.format(elem=elem_str)
        else:
            return 'P({elem})'.format(elem=elem_str)
