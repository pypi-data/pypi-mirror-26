#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/bool.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/include/__builtin__/str.hpp>
#include <pythonic/include/__builtin__/pow.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/abs.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/__builtin__/False.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/__builtin__/str.hpp>
#include <pythonic/__builtin__/pow.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/abs.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/__builtin__/False.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/__builtin__/tuple.hpp>
namespace __pythran_util_pythran
{
  struct strfunc_from_pdf
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = bool>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type1;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type>()(std::declval<__type1>()))>::type __type2;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type3;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type3>())) __type4;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type4>::type::iterator>::value_type>::type __type5;
      typedef indexable<__type5> __type6;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type>::type __type8;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::abs{})>::type>::type>()(std::declval<__type8>()))>::type __type9;
      typedef typename __combined<__type8,__type9>::type __type10;
      typedef long __type11;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type11>())) __type12;
      typedef decltype(std::declval<__type10>()[std::declval<__type12>()]) __type13;
      typedef decltype((std::declval<__type13>() - std::declval<__type13>())) __type18;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::abs{})>::type>::type>()(std::declval<__type18>())) __type19;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type20;
      typedef decltype(std::declval<__type20>()[std::declval<__type5>()]) __type21;
      typedef decltype(std::declval<__type10>()[std::declval<__type5>()]) __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type24;
      typedef decltype((pythonic::__builtin__::pow(std::declval<__type23>(), std::declval<__type24>()))) __type25;
      typedef decltype((std::declval<__type21>() * std::declval<__type25>())) __type26;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type>()(std::declval<__type26>())) __type27;
      typedef decltype((std::declval<__type19>() * std::declval<__type27>())) __type28;
      typedef container<typename std::remove_reference<__type28>::type> __type29;
      typedef __type0 __ptype8;
      typedef typename pythonic::returnable<typename __combined<__type2,__type6,__type29>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = bool>
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0 const & rxs, argument_type1 const & pdf, argument_type2 const & values, argument_type3 const & order, argument_type4 const & absolute= pythonic::__builtin__::False) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
  typename strfunc_from_pdf::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type strfunc_from_pdf::operator()(argument_type0 const & rxs, argument_type1 const & pdf, argument_type2 const & values, argument_type3 const & order, argument_type4 const & absolute) const
  {
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type>::type __type0;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::abs{})>::type>::type>()(std::declval<__type0>()))>::type __type1;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type2;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type>()(std::declval<__type2>()))>::type __type3;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type4;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type4>())) __type5;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type __type6;
    typedef indexable<__type6> __type7;
    typedef typename __combined<__type0,__type1>::type __type9;
    typedef long __type10;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type10>())) __type11;
    typedef decltype(std::declval<__type9>()[std::declval<__type11>()]) __type12;
    typedef decltype((std::declval<__type12>() - std::declval<__type12>())) __type17;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::abs{})>::type>::type>()(std::declval<__type17>())) __type18;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type19;
    typedef decltype(std::declval<__type19>()[std::declval<__type6>()]) __type20;
    typedef decltype(std::declval<__type9>()[std::declval<__type6>()]) __type22;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type23;
    typedef decltype((pythonic::__builtin__::pow(std::declval<__type22>(), std::declval<__type23>()))) __type24;
    typedef decltype((std::declval<__type20>() * std::declval<__type24>())) __type25;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type>()(std::declval<__type25>())) __type26;
    typedef decltype((std::declval<__type18>() * std::declval<__type26>())) __type27;
    typedef container<typename std::remove_reference<__type27>::type> __type28;
    typename pythonic::assignable<typename __combined<__type0,__type1>::type>::type values_ = values;
    typename pythonic::assignable<typename __combined<__type3,__type7,__type28>::type>::type S_order = pythonic::numpy::functor::empty{}(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(rxs));
    if (absolute)
    {
      values_ = pythonic::__builtin__::functor::abs{}(values_);
    }
    {
      long  __target1 = pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(rxs);
      for (long  irx=0L; irx < __target1; irx += 1L)
      {
        ;
        S_order.fast(irx) = (pythonic::__builtin__::functor::abs{}((values_[pythonic::types::make_tuple(irx, 1L)] - values_[pythonic::types::make_tuple(irx, 0L)])) * pythonic::numpy::functor::sum{}((pdf.fast(irx) * (pythonic::__builtin__::pow(values_.fast(irx), order)))));
      }
    }
    return S_order;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf0(pythonic::types::ndarray<double,2> rxs, pythonic::types::ndarray<double,2> pdf, pythonic::types::ndarray<double,2> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf1(pythonic::types::ndarray<double,2> rxs, pythonic::types::ndarray<double,2> pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf2(pythonic::types::ndarray<double,2> rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> pdf, pythonic::types::ndarray<double,2> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf3(pythonic::types::ndarray<double,2> rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf4(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> rxs, pythonic::types::ndarray<double,2> pdf, pythonic::types::ndarray<double,2> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf5(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> rxs, pythonic::types::ndarray<double,2> pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf6(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> pdf, pythonic::types::ndarray<double,2> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf7(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> values, double order, bool absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_strfunc_from_pdf0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf0(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf1(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf2(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf3(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf4(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf5(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf6(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) and is_convertible<double>(args_obj[3]) and is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf7(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_strfunc_from_pdf(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_strfunc_from_pdf0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf7(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `strfunc_from_pdf'.\n"
                "Candidates are:\n   strfunc_from_pdf(ndarray<double,2>,ndarray<double,2>,ndarray<double,2>,double,bool)\n   strfunc_from_pdf(ndarray<double,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>,double,bool)\n   strfunc_from_pdf(ndarray<double,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>,double,bool)\n   strfunc_from_pdf(ndarray<double,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>,double,bool)\n   strfunc_from_pdf(numpy_texpr<ndarray<double,2>>,ndarray<double,2>,ndarray<double,2>,double,bool)\n   strfunc_from_pdf(numpy_texpr<ndarray<double,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>,double,bool)\n   strfunc_from_pdf(numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>,double,bool)\n   strfunc_from_pdf(numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>,double,bool)\n"
                );
                return nullptr;
                });
            }


static PyMethodDef Methods[] = {
    {
    "strfunc_from_pdf",
    (PyCFunction)__pythran_wrapall_strfunc_from_pdf,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - strfunc_from_pdf(float64[][], float64[][], float64[][], float, bool)\n    - strfunc_from_pdf(float64[][], float64[][], float64[][].T, float, bool)\n    - strfunc_from_pdf(float64[][], float64[][].T, float64[][], float, bool)\n    - strfunc_from_pdf(float64[][], float64[][].T, float64[][].T, float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][], float64[][], float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][], float64[][].T, float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][].T, float64[][], float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][].T, float64[][].T, float, bool)\nCompute structure function of specified order from pdf for increments\n    module.\n\n"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "util_pythran",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(util_pythran)(void)
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible));
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(util_pythran)(void) {
    #ifdef PYTHONIC_TYPES_NDARRAY_HPP
        import_array()
    #endif
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("util_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(not theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.8.3",
                                      "2017-11-04 00:30:53.948165",
                                      "4906555a6987a1be9faa4d8956b291395a644065db9cdc1c45bbe5bc60ce2b0d");
    if(not theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PYTHRAN_RETURN;
}

#endif