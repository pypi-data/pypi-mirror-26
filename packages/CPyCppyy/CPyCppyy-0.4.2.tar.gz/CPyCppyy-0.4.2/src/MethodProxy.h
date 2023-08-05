#ifndef CPYCPPYY_METHODPROXY_H
#define CPYCPPYY_METHODPROXY_H

// Bindings
#include "PyCallable.h"

// Standard
#include <map>
#include <string>
#include <vector>


namespace CPyCppyy {

    class MethodProxy {
    public:
        typedef std::map<uint64_t, int>  DispatchMap_t;
        typedef std::vector<PyCallable*> Methods_t;

        struct MethodInfo_t {
            MethodInfo_t() : fFlags(TCallContext::kNone) { fRefCount = new int(1); }
            ~MethodInfo_t();

            std::string                 fName;
            MethodProxy::DispatchMap_t  fDispatchMap;
            MethodProxy::Methods_t      fMethods;
            uint64_t                    fFlags;

            int* fRefCount;

        private:
            MethodInfo_t(const MethodInfo_t&) = delete;
            MethodInfo_t& operator=(const MethodInfo_t&) = delete;
        };

    public:
        void Set(const std::string& name, std::vector<PyCallable*>& methods);

        const std::string& GetName() const { return fMethodInfo->fName; }
        void AddMethod(PyCallable* pc);
        void AddMethod(MethodProxy* meth);

    public:               // public, as the python C-API works with C structs
        PyObject_HEAD
        ObjectProxy*   fSelf;        // must be first (same layout as TemplateProxy)
        MethodInfo_t*  fMethodInfo;

    private:
        MethodProxy() = delete;
    };


//- method proxy type and type verification ----------------------------------
    extern PyTypeObject MethodProxy_Type;

    template<typename T>
    inline bool MethodProxy_Check(T* object)
    {
        return object && PyObject_TypeCheck(object, &MethodProxy_Type);
    }

    template<typename T>
    inline bool MethodProxy_CheckExact(T* object)
    {
        return object && Py_TYPE(object) == &MethodProxy_Type;
    }

//- creation -----------------------------------------------------------------
    inline MethodProxy* MethodProxy_New(
        const std::string& name, std::vector<PyCallable*>& methods)
    {
    // Create and initialize a new method proxy from the overloads.
        MethodProxy* pymeth = (MethodProxy*)MethodProxy_Type.tp_new(&MethodProxy_Type, nullptr, nullptr);
        pymeth->Set(name, methods);
        return pymeth;
    }

    inline MethodProxy* MethodProxy_New(const std::string& name, PyCallable* method)
    {
    // Create and initialize a new method proxy from the method.
        std::vector<PyCallable*> p;
        p.push_back(method);
        return MethodProxy_New(name, p);
    }

} // namespace CPyCppyy

#endif // !CPYCPPYY_METHODPROXY_H
