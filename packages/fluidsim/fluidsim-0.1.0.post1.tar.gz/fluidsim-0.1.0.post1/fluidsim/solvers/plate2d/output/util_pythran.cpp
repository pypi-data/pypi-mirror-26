#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/int32.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/int32.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/include/__builtin__/str.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/numpy/complex128.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/len.hpp>
#include <pythonic/include/numpy/conj.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/__builtin__/str.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/numpy/complex128.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/len.hpp>
#include <pythonic/numpy/conj.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/zeros.hpp>
namespace __pythran_util_pythran
{
  struct compute_correl2_seq
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type0>(), std::declval<__type0>())) __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type2;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type>()(std::declval<__type1>(), std::declval<__type2>()))>::type __type3;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type0>())) __type4;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type4>::type::iterator>::value_type>::type __type5;
      typedef long __type6;
      typedef decltype((std::declval<__type5>() + std::declval<__type6>())) __type7;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type __type9;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type9>())) __type10;
      typedef indexable<__type10> __type11;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type5>())) __type12;
      typedef indexable<__type12> __type13;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type16;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type17;
      typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type17>::type>::type>::type __type18;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type18>())) __type19;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type20>(), std::declval<__type5>())) __type21;
      typedef decltype(std::declval<__type16>()[std::declval<__type21>()]) __type22;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type>()(std::declval<__type16>()))>::type __type23;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type20>(), std::declval<__type9>())) __type24;
      typedef decltype(std::declval<__type23>()[std::declval<__type24>()]) __type25;
      typedef decltype((std::declval<__type22>() * std::declval<__type25>())) __type26;
      typedef container<typename std::remove_reference<__type26>::type> __type27;
      typedef typename __combined<__type3,__type11,__type27>::type __type29;
      typedef decltype(std::declval<__type29>()[std::declval<__type10>()]) __type31;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type>()(std::declval<__type31>())) __type32;
      typedef container<typename std::remove_reference<__type32>::type> __type33;
      typedef typename pythonic::returnable<typename __combined<__type3,__type11,__type13,__type27,__type33>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0 const & q_fftt, argument_type1 const & iomegas1, argument_type2 const & nb_omegas, argument_type3 const & nb_xs_seq) const
    ;
  }  ;
  struct compute_correl4_seq
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>())) __type1;
      typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type1>::type>::type>::type __type2;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type3>::type::iterator>::value_type>::type __type4;
      typedef decltype(std::declval<__type0>()[std::declval<__type4>()]) __type5;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::len{})>::type>::type>()(std::declval<__type0>())) __type6;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type7;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type7>(), std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type9;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type>()(std::declval<__type8>(), std::declval<__type9>()))>::type __type10;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type7>())) __type11;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
      typedef long __type13;
      typedef decltype((std::declval<__type12>() + std::declval<__type13>())) __type14;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type14>())) __type15;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type12>(), std::declval<__type16>())) __type17;
      typedef indexable<__type17> __type18;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type16>(), std::declval<__type12>())) __type26;
      typedef indexable<__type26> __type27;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type29;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type30;
      typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type30>::type>::type>::type __type31;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type31>())) __type32;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type __type33;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()[std::declval<__type4>()])>::type __type34;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type34>())) __type35;
      typedef decltype(std::declval<__type29>()[std::declval<__type35>()]) __type36;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type>()(std::declval<__type29>()))>::type __type37;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type12>())) __type38;
      typedef decltype(std::declval<__type37>()[std::declval<__type38>()]) __type39;
      typedef decltype((std::declval<__type36>() * std::declval<__type39>())) __type40;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type16>())) __type41;
      typedef decltype(std::declval<__type37>()[std::declval<__type41>()]) __type42;
      typedef decltype((std::declval<__type40>() * std::declval<__type42>())) __type43;
      typedef decltype((std::declval<__type12>() + std::declval<__type16>())) __type44;
      typedef typename pythonic::assignable<decltype((std::declval<__type44>() - std::declval<__type34>()))>::type __type45;
      typedef typename pythonic::assignable<decltype((-std::declval<__type45>()))>::type __type46;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type46>())) __type47;
      typedef decltype(std::declval<__type37>()[std::declval<__type47>()]) __type48;
      typedef decltype((std::declval<__type43>() * std::declval<__type48>())) __type49;
      typedef container<typename std::remove_reference<__type49>::type> __type50;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type45>())) __type61;
      typedef decltype(std::declval<__type29>()[std::declval<__type61>()]) __type62;
      typedef decltype((std::declval<__type43>() * std::declval<__type62>())) __type63;
      typedef container<typename std::remove_reference<__type63>::type> __type64;
      typedef decltype((std::declval<__type13>() * std::declval<__type7>())) __type78;
      typedef decltype((std::declval<__type78>() - std::declval<__type13>())) __type80;
      typedef typename pythonic::assignable<decltype((std::declval<__type80>() - std::declval<__type45>()))>::type __type81;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type81>())) __type82;
      typedef decltype(std::declval<__type37>()[std::declval<__type82>()]) __type83;
      typedef decltype((std::declval<__type43>() * std::declval<__type83>())) __type84;
      typedef container<typename std::remove_reference<__type84>::type> __type85;
      typedef typename __combined<__type10,__type18,__type64,__type85>::type __type87;
      typedef decltype(std::declval<__type87>()[std::declval<__type17>()]) __type89;
      typedef container<typename std::remove_reference<__type89>::type> __type90;
      typedef __type5 __ptype0;
      typedef typename pythonic::returnable<typename __combined<__type10,__type18,__type27,__type85,__type90>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0 const & q_fftt, argument_type1 const & iomegas1, argument_type2 const & nb_omegas, argument_type3 const & nb_xs_seq) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename compute_correl2_seq::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type compute_correl2_seq::operator()(argument_type0 const & q_fftt, argument_type1 const & iomegas1, argument_type2 const & nb_omegas, argument_type3 const & nb_xs_seq) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type0>(), std::declval<__type0>())) __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type2;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type>()(std::declval<__type1>(), std::declval<__type2>()))>::type __type3;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type0>())) __type4;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type4>::type::iterator>::value_type>::type __type5;
    typedef long __type6;
    typedef decltype((std::declval<__type5>() + std::declval<__type6>())) __type7;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type7>())) __type8;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type __type9;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type9>())) __type10;
    typedef indexable<__type10> __type11;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type5>())) __type12;
    typedef indexable<__type12> __type13;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type16;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type17;
    typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type17>::type>::type>::type __type18;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type18>())) __type19;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type20>(), std::declval<__type5>())) __type21;
    typedef decltype(std::declval<__type16>()[std::declval<__type21>()]) __type22;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type>()(std::declval<__type16>()))>::type __type23;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type20>(), std::declval<__type9>())) __type24;
    typedef decltype(std::declval<__type23>()[std::declval<__type24>()]) __type25;
    typedef decltype((std::declval<__type22>() * std::declval<__type25>())) __type26;
    typedef container<typename std::remove_reference<__type26>::type> __type27;
    typedef typename __combined<__type3,__type11,__type27>::type __type29;
    typedef decltype(std::declval<__type29>()[std::declval<__type10>()]) __type31;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type>()(std::declval<__type31>())) __type32;
    typedef container<typename std::remove_reference<__type32>::type> __type33;
    typename pythonic::assignable<decltype(pythonic::numpy::functor::conj{}(q_fftt))>::type q_fftt_conj = pythonic::numpy::functor::conj{}(q_fftt);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt)))>::type nx = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt));
    typename pythonic::assignable<typename __combined<__type3,__type11,__type13,__type27,__type33>::type>::type corr2 = pythonic::numpy::functor::zeros{}(pythonic::types::make_tuple(nb_omegas, nb_omegas), pythonic::numpy::functor::complex128{});
    {
      long  __target1 = nb_omegas;
      for (long  io3=0L; io3 < __target1; io3 += 1L)
      {
        {
          long  __target2 = (io3 + 1L);
          for (long  io4=0L; io4 < __target2; io4 += 1L)
          {
            {
              long  __target3 = nx;
              for (long  ix=0L; ix < __target3; ix += 1L)
              {
                corr2[pythonic::types::make_tuple(io3, io4)] += (q_fftt[pythonic::types::make_tuple(ix, io3)] * q_fftt_conj[pythonic::types::make_tuple(ix, io4)]);
              }
            }
            corr2[pythonic::types::make_tuple(io4, io3)] = pythonic::numpy::functor::conj{}(corr2[pythonic::types::make_tuple(io3, io4)]);
          }
        }
      }
    }
    return corr2;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename compute_correl4_seq::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type compute_correl4_seq::operator()(argument_type0 const & q_fftt, argument_type1 const & iomegas1, argument_type2 const & nb_omegas, argument_type3 const & nb_xs_seq) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::len{})>::type>::type>()(std::declval<__type0>())) __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type2;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type1>(), std::declval<__type2>(), std::declval<__type2>())) __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type4;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type>()(std::declval<__type3>(), std::declval<__type4>()))>::type __type5;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>())) __type6;
    typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type>::type __type7;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type7>())) __type8;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type __type9;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type2>())) __type10;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
    typedef long __type12;
    typedef decltype((std::declval<__type11>() + std::declval<__type12>())) __type13;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type13>())) __type14;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type11>(), std::declval<__type15>())) __type16;
    typedef indexable<__type16> __type17;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type15>(), std::declval<__type11>())) __type25;
    typedef indexable<__type25> __type26;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type28;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>())) __type29;
    typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type29>::type>::type>::type __type30;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type30>())) __type31;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type31>::type::iterator>::value_type>::type __type32;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()[std::declval<__type9>()])>::type __type33;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type33>())) __type34;
    typedef decltype(std::declval<__type28>()[std::declval<__type34>()]) __type35;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type>()(std::declval<__type28>()))>::type __type36;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type11>())) __type37;
    typedef decltype(std::declval<__type36>()[std::declval<__type37>()]) __type38;
    typedef decltype((std::declval<__type35>() * std::declval<__type38>())) __type39;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type15>())) __type40;
    typedef decltype(std::declval<__type36>()[std::declval<__type40>()]) __type41;
    typedef decltype((std::declval<__type39>() * std::declval<__type41>())) __type42;
    typedef decltype((std::declval<__type11>() + std::declval<__type15>())) __type43;
    typedef typename pythonic::assignable<decltype((std::declval<__type43>() - std::declval<__type33>()))>::type __type44;
    typedef typename pythonic::assignable<decltype((-std::declval<__type44>()))>::type __type45;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type45>())) __type46;
    typedef decltype(std::declval<__type36>()[std::declval<__type46>()]) __type47;
    typedef decltype((std::declval<__type42>() * std::declval<__type47>())) __type48;
    typedef container<typename std::remove_reference<__type48>::type> __type49;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type44>())) __type60;
    typedef decltype(std::declval<__type28>()[std::declval<__type60>()]) __type61;
    typedef decltype((std::declval<__type42>() * std::declval<__type61>())) __type62;
    typedef container<typename std::remove_reference<__type62>::type> __type63;
    typedef decltype((std::declval<__type12>() * std::declval<__type2>())) __type77;
    typedef decltype((std::declval<__type77>() - std::declval<__type12>())) __type79;
    typedef typename pythonic::assignable<decltype((std::declval<__type79>() - std::declval<__type44>()))>::type __type80;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type80>())) __type81;
    typedef decltype(std::declval<__type36>()[std::declval<__type81>()]) __type82;
    typedef decltype((std::declval<__type42>() * std::declval<__type82>())) __type83;
    typedef container<typename std::remove_reference<__type83>::type> __type84;
    typedef typename __combined<__type5,__type17,__type63,__type84>::type __type86;
    typedef decltype(std::declval<__type86>()[std::declval<__type16>()]) __type88;
    typedef container<typename std::remove_reference<__type88>::type> __type89;
    typename pythonic::assignable<decltype(pythonic::numpy::functor::conj{}(q_fftt))>::type q_fftt_conj = pythonic::numpy::functor::conj{}(q_fftt);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt)))>::type nx = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt));
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(iomegas1)))>::type n0 = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(iomegas1));
    typename pythonic::assignable<typename __combined<__type5,__type17,__type26,__type84,__type89>::type>::type corr4 = pythonic::numpy::functor::zeros{}(pythonic::types::make_tuple(pythonic::__builtin__::functor::len{}(iomegas1), nb_omegas, nb_omegas), pythonic::numpy::functor::complex128{});
    {
      long  __target1 = n0;
      for (long  i1=0L; i1 < __target1; i1 += 1L)
      {
        typename pythonic::assignable<decltype(iomegas1.fast(i1))>::type io1 = iomegas1.fast(i1);
        {
          long  __target2 = nb_omegas;
          for (long  io3=0L; io3 < __target2; io3 += 1L)
          {
            {
              long  __target3 = (io3 + 1L);
              for (long  io4=0L; io4 < __target3; io4 += 1L)
              {
                typename pythonic::assignable<decltype(((io3 + io4) - io1))>::type io2 = ((io3 + io4) - io1);
                if ((io2 < 0L))
                {
                  typename pythonic::assignable<decltype((-io2))>::type io2_ = (-io2);
                  {
                    long  __target4 = nx;
                    for (long  ix=0L; ix < __target4; ix += 1L)
                    {
                      corr4[pythonic::types::make_tuple(i1, io3, io4)] += (((q_fftt[pythonic::types::make_tuple(ix, io1)] * q_fftt_conj[pythonic::types::make_tuple(ix, io3)]) * q_fftt_conj[pythonic::types::make_tuple(ix, io4)]) * q_fftt_conj[pythonic::types::make_tuple(ix, io2_)]);
                    }
                  }
                }
                else
                {
                  if ((io2 >= nb_omegas))
                  {
                    typename pythonic::assignable<decltype((((2L * nb_omegas) - 1L) - io2))>::type io2__ = (((2L * nb_omegas) - 1L) - io2);
                    {
                      long  __target4 = nx;
                      for (long  ix_=0L; ix_ < __target4; ix_ += 1L)
                      {
                        corr4[pythonic::types::make_tuple(i1, io3, io4)] += (((q_fftt[pythonic::types::make_tuple(ix_, io1)] * q_fftt_conj[pythonic::types::make_tuple(ix_, io3)]) * q_fftt_conj[pythonic::types::make_tuple(ix_, io4)]) * q_fftt_conj[pythonic::types::make_tuple(ix_, io2__)]);
                      }
                    }
                  }
                  else
                  {
                    {
                      long  __target4 = nx;
                      for (long  ix__=0L; ix__ < __target4; ix__ += 1L)
                      {
                        corr4[pythonic::types::make_tuple(i1, io3, io4)] += (((q_fftt[pythonic::types::make_tuple(ix__, io1)] * q_fftt_conj[pythonic::types::make_tuple(ix__, io3)]) * q_fftt_conj[pythonic::types::make_tuple(ix__, io4)]) * q_fftt[pythonic::types::make_tuple(ix__, io2)]);
                      }
                    }
                  }
                }
                corr4[pythonic::types::make_tuple(i1, io4, io3)] = corr4[pythonic::types::make_tuple(i1, io3, io4)];
              }
            }
          }
        }
      }
    }
    return corr4;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util_pythran::compute_correl4_seq::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl4_seq0(pythonic::types::ndarray<std::complex<double>,2> q_fftt, pythonic::types::ndarray<int32_t,1> iomegas1, long nb_omegas, long nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl4_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_correl4_seq::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl4_seq1(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>> q_fftt, pythonic::types::ndarray<int32_t,1> iomegas1, long nb_omegas, long nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl4_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_correl2_seq::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl2_seq0(pythonic::types::ndarray<std::complex<double>,2> q_fftt, pythonic::types::ndarray<int32_t,1> iomegas1, long nb_omegas, long nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl2_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_correl2_seq::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl2_seq1(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>> q_fftt, pythonic::types::ndarray<int32_t,1> iomegas1, long nb_omegas, long nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl2_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
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
__pythran_wrap_compute_correl4_seq0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) and is_convertible<long>(args_obj[2]) and is_convertible<long>(args_obj[3]))
        return to_python(compute_correl4_seq0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_correl4_seq1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) and is_convertible<long>(args_obj[2]) and is_convertible<long>(args_obj[3]))
        return to_python(compute_correl4_seq1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_correl2_seq0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) and is_convertible<long>(args_obj[2]) and is_convertible<long>(args_obj[3]))
        return to_python(compute_correl2_seq0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_correl2_seq1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) and is_convertible<long>(args_obj[2]) and is_convertible<long>(args_obj[3]))
        return to_python(compute_correl2_seq1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_correl4_seq(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_correl4_seq0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_correl4_seq1(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `compute_correl4_seq'.\n"
                "Candidates are:\n   compute_correl4_seq(ndarray<std.complex<double>,2>,ndarray<int32_t,1>,long,long)\n   compute_correl4_seq(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<int32_t,1>,long,long)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_compute_correl2_seq(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_correl2_seq0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_correl2_seq1(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `compute_correl2_seq'.\n"
                "Candidates are:\n   compute_correl2_seq(ndarray<std.complex<double>,2>,ndarray<int32_t,1>,long,long)\n   compute_correl2_seq(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<int32_t,1>,long,long)\n"
                );
                return nullptr;
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_correl4_seq",
    (PyCFunction)__pythran_wrapall_compute_correl4_seq,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - compute_correl4_seq(complex128[][], int32[], int, int)\n    - compute_correl4_seq(complex128[][].T, int32[], int, int)\nCompute the correlations 4.\n\n    .. math::\n       C_4(\omega_1, \omega_2, \omega_3, \omega_4) =\n       \langle\n       \tilde w(\omega_1, \mathbf{x})\n       \tilde w(\omega_2, \mathbf{x})\n       \tilde w(\omega_3, \mathbf{x})^*\n       \tilde w(\omega_4, \mathbf{x})^*\n       \rangle_\mathbf{x},\n\n    where\n\n    .. math::\n       \omega_2 = \omega_3 + \omega_4 - \omega_1\n\n    and :math:`\omega_1 > 0`, :math:`\omega_3 > 0` and\n    :math:`\omega_4 > 0`. Thus, this function produces an array\n    :math:`C_4(\omega_1, \omega_3, \omega_4)`.\n\n"},{
    "compute_correl2_seq",
    (PyCFunction)__pythran_wrapall_compute_correl2_seq,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - compute_correl2_seq(complex128[][], int32[], int, int)\n    - compute_correl2_seq(complex128[][].T, int32[], int, int)\nCompute the correlations 2.\n\n    .. math::\n       C_2(\omega_1, \omega_2) =\n       \langle\n       \tilde w(\omega_1, \mathbf{x})\n       \tilde w(\omega_2, \mathbf{x})^*\n       \rangle_\mathbf{x},\n\n    where :math:`\omega_1 = \omega_2`. Thus, this function\n    produces an array :math:`C_2(\omega)`.\n\n"},
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
                                      "2017-11-04 00:30:51.760300",
                                      "0457aa8a7fb0558353c85f19d1ef2d300c5e96fccfab6a5a6d8f186bafb57af1");
    if(not theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PYTHRAN_RETURN;
}

#endif