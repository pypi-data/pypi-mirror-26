from __future__ import absolute_import, print_function, division
import six

import numpy as np
import unittest
from functools import update_wrapper

import theano
from theano import tensor
from theano.tests import unittest_tools as utt
from theano.misc.may_share_memory import may_share_memory
import theano.sparse

utt.seed_rng()


def makeSharedTester(shared_constructor_,
                     dtype_,
                     get_value_borrow_true_alias_,
                     shared_borrow_true_alias_,
                     set_value_borrow_true_alias_,
                     set_value_inplace_,
                     set_cast_value_inplace_,
                     shared_constructor_accept_ndarray_,
                     internal_type_,
                     test_internal_type_,
                     theano_fct_,
                     ref_fct_,
                     cast_value_=np.asarray,
                     expect_fail_fast_shape_inplace=True,
                     ):
    """
    This is a generic fct to allow reusing the same test function
    for many shared variable of many types.

    :param shared_constructor_: The shared variable constructor to use
    :param dtype_: The dtype of the data to test
    :param get_value_borrow_true_alias_: Should a get_value(borrow=True) return the internal object
    :param shared_borrow_true_alias_: Should shared(val,borrow=True) reuse the val memory space
    :param set_value_borrow_true_alias_: Should set_value(val,borrow=True) reuse the val memory space
    :param set_value_inplace_: Should this shared variable overwrite the current
                               memory when the new value is an ndarray
    :param set_cast_value_inplace_: Should this shared variable overwrite the
                               current memory when the new value is of the same
                               type as the internal type.
    :param shared_constructor_accept_ndarray_: Do the shared_constructor accept an ndarray as input?
    :param internal_type_: The internal type used.
    :param test_internal_type_: A function that tell if its input is of the same
                                type as this shared variable internal type.
    :param theano_fct_: A theano op that will be used to do some computation on the shared variable
    :param ref_fct_: A reference function that should return the same value as the theano_fct_
    :param cast_value_: A callable that cast an ndarray into the internal shared variable representation
    :param name: This string is used to set the returned class' __name__
                 attribute. This is needed for nosetests to properly tag the
                 test with its correct name, rather than use the generic
                 SharedTester name. This parameter is mandatory (keeping the
                 default None value will raise an error), and must be set to
                 the name of the variable that will hold the returned class.
    :note:
        We must use /= as sparse type don't support other inplace operation.
    """
    class m(type):
        pass

    class SharedTester(unittest.TestCase):
        # This is to allow setting __doc__ with python 2
        if not six.PY3:
            __metaclass__ = m
        shared_constructor = staticmethod(shared_constructor_)
        dtype = dtype_
        get_value_borrow_true_alias = get_value_borrow_true_alias_
        shared_borrow_true_alias = shared_borrow_true_alias_
        internal_type = internal_type_
        test_internal_type = staticmethod(test_internal_type_)
        theano_fct = staticmethod(theano_fct_)
        ref_fct = staticmethod(ref_fct_)
        set_value_borrow_true_alias = set_value_borrow_true_alias_
        set_value_inplace = set_value_inplace_
        set_cast_value_inplace = set_cast_value_inplace_
        shared_constructor_accept_ndarray = shared_constructor_accept_ndarray_
        cast_value = staticmethod(cast_value_)

        def test_shared_dont_alias(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x = np.asarray(rng.uniform(0, 1, [2, 4]), dtype=dtype)
            x = self.cast_value(x)

            x_ref = self.ref_fct(x)
            x_shared = self.shared_constructor(x, borrow=False)
            total = self.theano_fct(x_shared)

            total_func = theano.function([], total)

            total_val = total_func()

            assert np.allclose(self.ref_fct(x), total_val)

            x /= .5
            total_val_2 = total_func()

            # value used to construct should not alias with internal
            assert np.allclose(total_val, total_val_2)

            x = x_shared.get_value(borrow=False)

            x /= .5

            total_val_3 = total_func()

            # value returned by access should not alias with internal
            assert np.allclose(total_val, total_val_3)

            # in this case we can alias
            x = x_shared.get_value(borrow=True)
            x /= .5

            # this is not required by the contract but it is a feature we've
            # implemented for some type of SharedVariable.
            if self.get_value_borrow_true_alias:
                assert np.allclose(self.ref_fct(x), total_func())
            else:
                assert np.allclose(x_ref, total_func())

        def test_shape(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x = np.asarray(rng.uniform(0, 1, [2, 4]), dtype=dtype)
            x = self.cast_value(x)

            x_ref = self.ref_fct(x)
            x_shared = self.shared_constructor(x, borrow=False)
            total = self.theano_fct(x_shared)

            f = theano.function([], x_shared.shape)
            topo = f.maker.fgraph.toposort()

            assert np.all(f() == (2, 4))
            if theano.config.mode != 'FAST_COMPILE':
                assert len(topo) == 3
                assert isinstance(topo[0].op, tensor.opt.Shape_i)
                assert isinstance(topo[1].op, tensor.opt.Shape_i)
                assert isinstance(topo[2].op, tensor.opt.MakeVector)

        def test_shape_i(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x = np.asarray(rng.uniform(0, 1, [2, 4]), dtype=dtype)
            x = self.cast_value(x)

            x_ref = self.ref_fct(x)
            x_shared = self.shared_constructor(x, borrow=False)
            total = self.theano_fct(x_shared)

            f = theano.function([], x_shared.shape[1])
            topo = f.maker.fgraph.toposort()

            assert np.all(f() == (4))
            if theano.config.mode != 'FAST_COMPILE':
                assert len(topo) == 1
                assert isinstance(topo[0].op, tensor.opt.Shape_i)

        def test_return_internal_type(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x = np.asarray(rng.uniform(0, 1, [2, 4]), dtype=dtype)
            x = self.cast_value(x)

            x_ref = self.ref_fct(x)
            x_shared = self.shared_constructor(x, borrow=False)
            total = self.theano_fct(x_shared)

            total_func = theano.function([], total)

            # in this case we can alias with the internal value
            x = x_shared.get_value(borrow=True, return_internal_type=True)
            assert self.test_internal_type(x)

            x /= .5

            # this is not required by the contract but it is a feature we can
            # implement for some type of SharedVariable.
            assert np.allclose(self.ref_fct(x), total_func())

            x = x_shared.get_value(borrow=False, return_internal_type=True)
            assert self.test_internal_type(x)
            assert x is not x_shared.container.value
            x /= .5

            # this is required by the contract
            assert not np.allclose(self.ref_fct(x), total_func())

        def test_get_value(self):
            # Test that get_value returns a ndarray
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x_orig = np.asarray(rng.uniform(0, 1, [2, 4]), dtype=dtype)
            x_cast = self.cast_value(x_orig)
            if self.shared_constructor_accept_ndarray:
                x_shared = self.shared_constructor(x_orig, borrow=False)
                assert isinstance(x_shared.get_value(), x_orig.__class__)

            x_shared = self.shared_constructor(x_cast, borrow=False)
            assert isinstance(x_shared.get_value(), x_cast.__class__)

        def test_set_value(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x = np.asarray(rng.uniform(0, 1, [2, 4]), dtype=dtype)
            x = self.cast_value(x)

            x_orig = x
            x_orig_copy = x.copy()
            x_ref = self.ref_fct(x)
            x_shared = self.shared_constructor(x, borrow=False)
            total = self.theano_fct(x_shared)

            total_func = theano.function([], total)
            total_func()

            # test if that theano shared variable optimize set_value(borrow=True)
            get_x = x_shared.get_value(borrow=True)
            assert get_x is not x_orig  # borrow=False to shared_constructor
            get_x /= .5
            x_shared.set_value(get_x, borrow=True)
            x = x_shared.get_value(borrow=True)
            if self.set_value_borrow_true_alias:
                assert x is get_x
            else:
                assert x is not get_x
            assert np.allclose(self.ref_fct(np.asarray(x_orig)/.5), self.ref_fct(x))

            # test optimized get set value on the gpu(don't pass data to the cpu)
            get_x = x_shared.get_value(borrow=True, return_internal_type=True)
            assert get_x is not x_orig  # borrow=False to shared_constructor
            assert self.test_internal_type(get_x)

            get_x /= .5
            assert self.test_internal_type(get_x)
            x_shared.set_value(get_x, borrow=True)
            x = x_shared.get_value(borrow=True, return_internal_type=True)
            assert self.test_internal_type(x)
            assert x is get_x

            # TODO test Out.
        def test_shared_do_alias(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x = np.asarray(rng.uniform(1, 2, [4, 2]), dtype=dtype)
            x = self.cast_value(x)
            x_ref = self.ref_fct(x)

            x_shared = self.shared_constructor(x, borrow=True)

            total = self.theano_fct(x_shared)

            total_func = theano.function([], total)

            total_val = total_func()

            assert np.allclose(self.ref_fct(x), total_val)

            x /= .5

            # not required by the contract but it is a feature we've implemented
            if self.shared_borrow_true_alias:
                assert np.allclose(self.ref_fct(x), total_func())
            else:
                assert np.allclose(x_ref, total_func())

        def test_inplace_set_value(self):
            # We test that if the SharedVariable implement it we do inplace set_value
            # We also test this for partial inplace modification when accessing the internal of theano.

            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            shp = (100//4, 1024)  # 100KB

            x = np.zeros(shp, dtype=dtype)
            x = self.cast_value(x)
            x_shared = self.shared_constructor(x, borrow=True)

            old_data = x_shared.container.storage[0]
            nd = np.ones(shp, dtype=dtype)

            if x.__class__.__name__ != 'csr_matrix':
                # sparse matrix don't support inplace affectation
                x_shared.container.value[:] = nd
                assert (np.asarray(x_shared.get_value(borrow=True)) == nd).all()
                # This should always share value!
                assert may_share_memory(old_data, x_shared.container.storage[0])
                assert may_share_memory(old_data, x_shared.get_value(borrow=True, return_internal_type=True))

                nd[0] += 1
                x_shared.container.value[0] = nd[0]
                assert (np.asarray(x_shared.get_value(borrow=True)[0]) == nd[0]).all()
                assert (np.asarray(x_shared.get_value(borrow=True)[1:]) == nd[1:]).all()
                # This should always share value!
                assert may_share_memory(old_data, x_shared.container.storage[0])
                assert may_share_memory(old_data, x_shared.get_value(borrow=True, return_internal_type=True))

            if x.__class__.__name__ != 'csr_matrix':
                # sparse matrix don't support inplace affectation
                nd += 1
                # THIS DOENS'T DO WHAT WE EXPECT the content of a is
                # not updated for GpuArray, but it is for ndarray
                x_shared.get_value(borrow=True)[:] = nd
                assert may_share_memory(old_data, x_shared.container.storage[0])
                x_shared.get_value(borrow=True)

            # Test by set_value with borrow=False
            nd += 1
            old_data = x_shared.container.storage[0]
            x_shared.set_value(nd, borrow=False)
            assert np.allclose(self.ref_fct(x_shared.get_value(borrow=True)),
                    self.ref_fct(self.cast_value(nd)))
            assert may_share_memory(old_data, x_shared.container.storage[0]) == self.set_value_inplace

            # Test by set_value with borrow=False when new data cast.
            # specificaly useful for gpu data
            nd += 1
            old_data = x_shared.container.storage[0]
            x_shared.set_value(self.cast_value(nd), borrow=False)
            assert np.allclose(self.ref_fct(x_shared.get_value(borrow=True)),
                    self.ref_fct(self.cast_value(nd)))
            assert may_share_memory(old_data, x_shared.container.storage[0]) == self.set_cast_value_inplace

            # Test by set_value with borrow=True
            nd += 1
            old_data = x_shared.container.storage[0]
            x_shared.set_value(nd.copy(), borrow=True)
            assert np.allclose(self.ref_fct(x_shared.get_value(borrow=True)),
                    self.ref_fct(self.cast_value(nd)))
            assert may_share_memory(old_data, x_shared.container.storage[0]) == self.set_value_inplace

            # Test by set_value with borrow=True when new data cast.
            nd += 1
            old_data = x_shared.container.storage[0]
            x_shared.set_value(self.cast_value(nd.copy()), borrow=True)
            assert np.allclose(self.ref_fct(x_shared.get_value(borrow=True)), self.ref_fct(self.cast_value(nd)))
            assert may_share_memory(old_data, x_shared.container.storage[0]) == self.set_cast_value_inplace

        def test_specify_shape(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x1_1 = np.asarray(rng.uniform(1, 2, [4, 2]), dtype=dtype)
            x1_1 = self.cast_value(x1_1)
            x1_2 = np.asarray(rng.uniform(1, 2, [4, 2]), dtype=dtype)
            x1_2 = self.cast_value(x1_2)
            x2 = np.asarray(rng.uniform(1, 2, [4, 3]), dtype=dtype)
            x2 = self.cast_value(x2)

            # Test that we can replace with values of the same shape
            x1_shared = self.shared_constructor(x1_1)
            x1_specify_shape = tensor.specify_shape(x1_shared, x1_1.shape)
            x1_shared.set_value(x1_2)
            assert np.allclose(self.ref_fct(x1_shared.get_value(borrow=True)),
                    self.ref_fct( x1_2))
            shape_op_fct = theano.function([], x1_shared.shape)
            topo = shape_op_fct.maker.fgraph.toposort()
            if theano.config.mode != 'FAST_COMPILE':
                assert len(topo) == 3
                assert isinstance(topo[0].op, tensor.opt.Shape_i)
                assert isinstance(topo[1].op, tensor.opt.Shape_i)
                assert isinstance(topo[2].op, tensor.opt.MakeVector)

            # Test that we forward the input
            specify_shape_fct = theano.function([], x1_specify_shape)
            assert np.all(self.ref_fct(specify_shape_fct()) ==
                             self.ref_fct(x1_2))
            topo_specify = specify_shape_fct.maker.fgraph.toposort()
            assert len(topo_specify) == 2

            # Test that we put the shape info into the graph
            shape_constant_fct = theano.function([], x1_specify_shape.shape)
            assert np.all(shape_constant_fct() == shape_op_fct())
            topo_cst = shape_constant_fct.maker.fgraph.toposort()
            if theano.config.mode != 'FAST_COMPILE':
                assert len(topo_cst) == 1
                topo_cst[0].op == theano.compile.function_module.deep_copy_op

            # Test that we can take the grad.
            if (theano.sparse.enable_sparse and
                isinstance(x1_specify_shape.type, theano.sparse.SparseType)):
                # SparseVariable don't support sum for now.
                assert not hasattr(x1_specify_shape, 'sum')
            else:
                shape_grad = tensor.grad(x1_specify_shape.sum(), x1_shared)
                shape_constant_fct_grad = theano.function([], shape_grad)
                # theano.printing.debugprint(shape_constant_fct_grad)
                shape_constant_fct_grad()

            # Test that we can replace with values of the different shape
            # but that will raise an error in some case, but not all
            specify_shape_fct()
            x1_shared.set_value(x2)
            self.assertRaises(AssertionError, specify_shape_fct)

            # No assertion will be raised as the Op is removed from the graph
            # when their is optimization
            if theano.config.mode not in ['FAST_COMPILE', 'DebugMode', 'DEBUG_MODE']:
                shape_constant_fct()
            else:
                self.assertRaises(AssertionError, shape_constant_fct)

        def test_specify_shape_partial(self):
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            x1_1 = np.asarray(rng.uniform(1, 2, [4, 2]), dtype=dtype)
            x1_1 = self.cast_value(x1_1)
            x1_2 = np.asarray(rng.uniform(1, 2, [4, 2]), dtype=dtype)
            x1_2 = self.cast_value(x1_2)
            x2 = np.asarray(rng.uniform(1, 2, [5, 2]), dtype=dtype)
            x2 = self.cast_value(x2)

            # Test that we can replace with values of the same shape
            x1_shared = self.shared_constructor(x1_1)
            x1_specify_shape = tensor.specify_shape(x1_shared,
                                                    (tensor.as_tensor_variable(x1_1.shape[0]),
                                                     x1_shared.shape[1]))
            x1_shared.set_value(x1_2)
            assert np.allclose(
                    self.ref_fct(x1_shared.get_value(borrow=True)),
                    self.ref_fct( x1_2))
            shape_op_fct = theano.function([], x1_shared.shape)
            topo = shape_op_fct.maker.fgraph.toposort()
            shape_op_fct()
            if theano.config.mode != 'FAST_COMPILE':
                assert len(topo) == 3
                assert isinstance(topo[0].op, tensor.opt.Shape_i)
                assert isinstance(topo[1].op, tensor.opt.Shape_i)
                assert isinstance(topo[2].op, tensor.opt.MakeVector)

            # Test that we forward the input
            specify_shape_fct = theano.function([], x1_specify_shape)
            specify_shape_fct()
            # theano.printing.debugprint(specify_shape_fct)
            assert np.all(self.ref_fct(specify_shape_fct())
                             == self.ref_fct(x1_2))
            topo_specify = specify_shape_fct.maker.fgraph.toposort()
            if theano.config.mode != 'FAST_COMPILE':
                assert len(topo_specify) == 4

            # Test that we put the shape info into the graph
            shape_constant_fct = theano.function([], x1_specify_shape.shape)
            # theano.printing.debugprint(shape_constant_fct)
            assert np.all(shape_constant_fct() == shape_op_fct())
            topo_cst = shape_constant_fct.maker.fgraph.toposort()
            if theano.config.mode != 'FAST_COMPILE':
                assert len(topo_cst) == 2

            # Test that we can replace with values of the different shape
            # but that will raise an error in some case, but not all
            x1_shared.set_value(x2)
            self.assertRaises(AssertionError, specify_shape_fct)

            # No assertion will be raised as the Op is removed from the graph
            if theano.config.mode not in ['FAST_COMPILE', 'DebugMode', 'DEBUG_MODE']:
                shape_constant_fct()
            else:
                self.assertRaises(AssertionError, shape_constant_fct)

        def test_specify_shape_inplace(self):
            # test that specify_shape don't break inserting inplace op

            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            rng = np.random.RandomState(utt.fetch_seed())
            a = np.asarray(rng.uniform(1, 2, [40, 40]), dtype=dtype)
            a = self.cast_value(a)
            a_shared = self.shared_constructor(a)
            b = np.asarray(rng.uniform(1, 2, [40, 40]), dtype=dtype)
            b = self.cast_value(b)
            b_shared = self.shared_constructor(b)
            s = np.zeros((40, 40), dtype=dtype)
            s = self.cast_value(s)
            s_shared = self.shared_constructor(s)
            f = theano.function([],
                                updates=[(s_shared, theano.dot(a_shared, b_shared)
                                         + s_shared)])
            topo = f.maker.fgraph.toposort()
            f()
            # [Gemm{inplace}(<TensorType(float64, matrix)>, 0.01, <TensorType(float64, matrix)>, <TensorType(float64, matrix)>, 2e-06)]
            if theano.config.mode != 'FAST_COMPILE':
                assert sum([node.op.__class__.__name__ in ["Gemm", "GpuGemm", "StructuredDot"] for node in topo]) == 1
                assert all(node.op == tensor.blas.gemm_inplace for node in topo if isinstance(node.op, tensor.blas.Gemm))
                assert all(node.op.inplace for node in topo if node.op.__class__.__name__ == "GpuGemm")
            # Their is no inplace gemm for sparse
            # assert all(node.op.inplace for node in topo if node.op.__class__.__name__ == "StructuredDot")
            s_shared_specify = tensor.specify_shape(s_shared, s_shared.get_value(borrow=True).shape)

            # now test with the specify shape op in the output
            f = theano.function([], s_shared.shape,
                                updates=[(s_shared, theano.dot(a_shared, b_shared)
                                         + s_shared_specify)])
            topo = f.maker.fgraph.toposort()
            shp = f()
            assert np.all(shp == (40, 40))
            if theano.config.mode != 'FAST_COMPILE':
                assert sum([node.op.__class__.__name__ in ["Gemm", "GpuGemm", "StructuredDot"] for node in topo]) == 1
                assert all(node.op == tensor.blas.gemm_inplace for node in topo if isinstance(node.op, tensor.blas.Gemm))
                assert all(node.op.inplace for node in topo if node.op.__class__.__name__ == "GpuGemm")
            # now test with the specify shape op in the inputs and outputs
            a_shared = tensor.specify_shape(a_shared,
                    a_shared.get_value(borrow=True).shape)
            b_shared = tensor.specify_shape(b_shared,
                    b_shared.get_value(borrow=True).shape)

            f = theano.function([], s_shared.shape,
                                updates=[(s_shared, theano.dot(a_shared, b_shared)
                                         + s_shared_specify)])
            topo = f.maker.fgraph.toposort()
            shp = f()
            assert np.all(shp == (40, 40))
            if theano.config.mode != 'FAST_COMPILE':
                assert sum([node.op.__class__.__name__ in ["Gemm", "GpuGemm", "StructuredDot"] for node in topo]) == 1
                assert all(node.op == tensor.blas.gemm_inplace for node in topo if isinstance(node.op, tensor.blas.Gemm))
                assert all(node.op.inplace for node in topo if node.op.__class__.__name__ == "GpuGemm")

        if theano.config.cycle_detection == 'fast' and expect_fail_fast_shape_inplace and theano.config.mode != 'FAST_COMPILE':
            test_specify_shape_inplace = unittest.expectedFailure(test_specify_shape_inplace)

        def test_values_eq(self):
            # Test the type.values_eq[_approx] function
            dtype = self.dtype
            if dtype is None:
                dtype = theano.config.floatX

            # We need big shape as in the past there have been a bug in the
            # sparse values_eq_approx.
            shp = (1024, 1024)

            # Test the case with all zeros element
            rng = np.random.RandomState(utt.fetch_seed())
            for x in [np.asarray(rng.rand(*shp), dtype=dtype),
                      np.zeros(shp, dtype=dtype)]:
                zeros = (x == 0).all()
                x = self.cast_value(x)
                x_shared = self.shared_constructor(x, borrow=True)

                y = x.copy()
                y[0, 0], y[1, 0] = y[1, 0], y[0, 0]
                y = self.cast_value(y)

                assert x_shared.type.values_eq(x, x)
                assert x_shared.type.values_eq_approx(x, x)
                if not zeros:
                    assert not np.allclose(self.ref_fct(x), self.ref_fct(y))
                    assert not x_shared.type.values_eq(x, y)
                    assert not x_shared.type.values_eq_approx(x, y)

    def f(cls):
        return update_wrapper(SharedTester, cls, updated=())
    return f


@makeSharedTester(
    shared_constructor_=tensor._shared,
    dtype_=theano.config.floatX,
    get_value_borrow_true_alias_=True,
    shared_borrow_true_alias_=True,
    set_value_borrow_true_alias_=True,
    set_value_inplace_=False,
    set_cast_value_inplace_=False,
    shared_constructor_accept_ndarray_=True,
    internal_type_=np.ndarray,
    test_internal_type_=lambda a: isinstance(a, np.ndarray),
    theano_fct_=lambda a: a*2,
    ref_fct_=lambda a: np.asarray((a*2)),
    cast_value_=np.asarray)
class test_shared_options(object):
    pass


def test_scalar_shared_options():
    # Simple test to make sure we do not loose that fonctionality.
    theano.shared(value=0., name='lk', borrow=True)
    theano.shared(value=np.float32(0.), name='lk', borrow=True)
