#ifndef CPYCPPYY_TEMPLATEPROXY_H
#define CPYCPPYY_TEMPLATEPROXY_H

// Bindings
#include "CPyCppyyType.h"

// Standard
#include <string>


namespace CPyCppyy {

    class PyCallable;
    class MethodProxy;

/** Template proxy object to return functions and methods
      @author  WLAV
      @date    01/15/2008
      @version 1.0
 */

    class TemplateProxy {
    private:
        friend TemplateProxy* TemplateProxy_New(
            const std::string& cppname, const std::string& pyname, PyObject* pyclass);
        void Set(const std::string& cppname, const std::string& pyname, PyObject* pyclass);

    public:              // public, as the python C-API works with C structs
        PyObject_HEAD
        PyObject* fSelf;           // must be first (same layout as MethodProxy)
        PyObject* fCppName;
        PyObject* fPyClass;
        PyObject* fPyName;
        MethodProxy* fNonTemplated;     // holder for non-template overloads
        MethodProxy* fTemplated;        // holder for templated overloads

    public:
        void AddOverload(MethodProxy* mp);
        void AddOverload(PyCallable* pc);
        void AddTemplate(PyCallable* pc);

    private:              // private, as the python C-API will handle creation
        TemplateProxy() {}
    };


//- template proxy type and type verification --------------------------------
    extern PyTypeObject TemplateProxy_Type;

    template<typename T>
    inline bool TemplateProxy_Check(T* object)
    {
        return object && PyObject_TypeCheck(object, &TemplateProxy_Type);
    }

    template<typename T>
    inline bool TemplateProxy_CheckExact(T* object)
    {
        return object && Py_TYPE(object) == &TemplateProxy_Type;
    }

//- creation -----------------------------------------------------------------
    inline TemplateProxy* TemplateProxy_New(
            const std::string& cppname, const std::string& pyname, PyObject* pyclass)
    {
    // Create and initialize a new template method proxy for the class.
        if (!CPyCppyyType_Check(pyclass)) return nullptr;

        TemplateProxy* pytmpl =
            (TemplateProxy*)TemplateProxy_Type.tp_new(&TemplateProxy_Type, nullptr, nullptr);
        pytmpl->Set(cppname, pyname, pyclass);
        return pytmpl;
    }

} // namespace CPyCppyy

#endif // !CPYCPPYY_TEMPLATEPROXY_H
