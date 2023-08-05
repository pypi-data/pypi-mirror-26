#ifndef CPYCPPYY_PYCALLABLE_H
#define CPYCPPYY_PYCALLABLE_H

// Bindings
#include "TCallContext.h"


namespace CPyCppyy {

    class ObjectProxy;

    class PyCallable {
    public:
        virtual ~PyCallable() {}

    public:
        virtual PyObject* GetSignature(bool show_formalargs = true) = 0;
        virtual PyObject* GetPrototype(bool show_formalargs = true) = 0;
        virtual PyObject* GetDocString() { return GetPrototype(); }

        virtual Int_t GetPriority() = 0;

        virtual Int_t GetMaxArgs() = 0;
        virtual PyObject* GetCoVarNames() = 0;
        virtual PyObject* GetArgDefault(Int_t /* iarg */)  = 0;

        virtual PyObject* GetScopeProxy()  = 0;

        virtual PyCallable* Clone() = 0;

    public:
        virtual PyObject* Call(
            ObjectProxy*& self, PyObject* args, PyObject* kwds, TCallContext* ctxt = nullptr) = 0;
    };

} // namespace CPyCppyy

#endif // !CPYCPPYY_PYCALLABLE_H
