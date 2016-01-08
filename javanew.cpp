/***********************************************************************
Copyright (C) 2009 OpenEye Scientific Software, Inc.
***********************************************************************/
#include "openeye.h"

#include <stdexcept>
#include <new>

namespace OEPlatform 
{
   OEPLATFORM_API void *Java_malloc(size_t bytes);
   OEPLATFORM_API void  Java_free(void *ptr);
}


#ifdef _MSC_VER
void* operator new(size_t size) 
{
  void* ptr = OEPlatform::Java_malloc(size); 
  if (ptr == NULL)
    throw std::bad_alloc();
  return ptr;
}

void* operator new[](size_t size) 
{
  void* ptr = OEPlatform::Java_malloc(size); 
  if (ptr == NULL)
    throw std::bad_alloc();
  return ptr;
}
#else
void* operator new(size_t size) throw (std::bad_alloc) 
{ 
  void* ptr = OEPlatform::Java_malloc(size); 
  if (ptr == NULL)
    throw std::bad_alloc();
  return ptr;
}

void* operator new[](size_t size) throw (std::bad_alloc) 
{ 
  void* ptr = OEPlatform::Java_malloc(size); 
  if (ptr == NULL)
    throw std::bad_alloc();
  return ptr;
}
#endif

void operator delete(void* p) throw() { OEPlatform::Java_free(p); }
void operator delete[](void* p) throw() { OEPlatform::Java_free(p); }

void* operator new(size_t size, const std::nothrow_t&) throw() 
  { return OEPlatform::Java_malloc(size); }
void operator delete(void* p, const std::nothrow_t&) throw() 
  { OEPlatform::Java_free(p);}
void* operator new[](size_t size, const std::nothrow_t&) throw() 
  { return OEPlatform::Java_malloc(size); }
void operator delete[](void* p, const std::nothrow_t&) throw() 
  { OEPlatform::Java_free(p); }


