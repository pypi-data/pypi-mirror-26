#ifndef CPYCPPYY_CPPYY_H
#define CPYCPPYY_CPPYY_H

// Standard
#include <string>
#include <vector>
#include <stddef.h>


namespace Cppyy {

    typedef ptrdiff_t   TCppScope_t;
    typedef TCppScope_t TCppType_t;
    typedef void*       TCppObject_t;
    typedef ptrdiff_t   TCppMethod_t;

    typedef Long_t      TCppIndex_t;
    typedef void*       TCppFuncAddr_t;

// name to opaque C++ scope representation -----------------------------------
    TCppIndex_t GetNumScopes(TCppScope_t parent);
    std::string GetScopeName(TCppScope_t parent, TCppIndex_t iscope);
    std::string ResolveName(const std::string& cppitem_name);
    TCppScope_t GetScope(const std::string& scope_name);
    TCppType_t  GetActualClass(TCppType_t klass, TCppObject_t obj);
    size_t      SizeOf(TCppType_t klass);

    bool      IsBuiltin(const std::string& type_name);
    bool      IsComplete(const std::string& type_name);

    extern TCppScope_t gGlobalScope;      // for fast access

// memory management ---------------------------------------------------------
    TCppObject_t Allocate(TCppType_t type);
    void         Deallocate(TCppType_t type, TCppObject_t instance);
    TCppObject_t Construct(TCppType_t type);
    void         Destruct(TCppType_t type, TCppObject_t instance);

// method/function dispatching -----------------------------------------------
    void         CallV(TCppMethod_t method, TCppObject_t self, void* args);
    UChar_t      CallB(TCppMethod_t method, TCppObject_t self, void* args);
    Char_t       CallC(TCppMethod_t method, TCppObject_t self, void* args);
    Short_t      CallH(TCppMethod_t method, TCppObject_t self, void* args);
    Int_t        CallI(TCppMethod_t method, TCppObject_t self, void* args);
    Long_t       CallL(TCppMethod_t method, TCppObject_t self, void* args);
    Long64_t     CallLL(TCppMethod_t method, TCppObject_t self, void* args);
    Float_t      CallF(TCppMethod_t method, TCppObject_t self, void* args);
    Double_t     CallD(TCppMethod_t method, TCppObject_t self, void* args);
    LongDouble_t CallLD(TCppMethod_t method, TCppObject_t self, void* args);
    void*        CallR(TCppMethod_t method, TCppObject_t self, void* args);
    Char_t*      CallS(TCppMethod_t method, TCppObject_t self, void* args, size_t* length);
    TCppObject_t CallConstructor(TCppMethod_t method, TCppType_t type, void* args);
    void         CallDestructor(TCppType_t type, TCppObject_t self);
    TCppObject_t CallO(TCppMethod_t method, TCppObject_t self, void* args, TCppType_t result_type);

    TCppFuncAddr_t GetFunctionAddress(TCppScope_t scope, TCppIndex_t imeth);

// handling of function argument buffer --------------------------------------
    void*  AllocateFunctionArgs(size_t nargs);
    void   DeallocateFunctionArgs(void* args);
    size_t GetFunctionArgSizeof();
    size_t GetFunctionArgTypeoffset();

// scope reflection information ----------------------------------------------
    bool IsNamespace(TCppScope_t scope);
    bool IsTemplate(const std::string& template_name);
    bool IsAbstract(TCppType_t type);
    bool IsEnum(const std::string& type_name);

// class reflection information ----------------------------------------------
    std::string GetFinalName(TCppType_t type);
    std::string GetScopedFinalName(TCppType_t type);
    bool        HasComplexHierarchy(TCppType_t type);
    TCppIndex_t GetNumBases(TCppType_t type);
    std::string GetBaseName(TCppType_t type, TCppIndex_t ibase);
    bool        IsSubtype(TCppType_t derived, TCppType_t base);
    void        AddSmartPtrType(const std::string&);
    bool        IsSmartPtr(const std::string&);

// calculate offsets between declared and actual type, up-cast: direction > 0; down-cast: direction < 0
    ptrdiff_t GetBaseOffset(
        TCppType_t derived, TCppType_t base, TCppObject_t address, int direction, bool rerror = false);

// method/function reflection information ------------------------------------
    TCppIndex_t GetNumMethods(TCppScope_t scope);
    TCppIndex_t GetMethodIndexAt(TCppScope_t scope, TCppIndex_t imeth);
    std::vector<Cppyy::TCppIndex_t> GetMethodIndicesFromName(
        TCppScope_t scope, const std::string& name);

    TCppMethod_t GetMethod(TCppScope_t scope, TCppIndex_t imeth);

    std::string GetMethodName(TCppMethod_t);
    std::string GetMethodResultType(TCppMethod_t);
    TCppIndex_t GetMethodNumArgs(TCppMethod_t);
    TCppIndex_t GetMethodReqArgs(TCppMethod_t);
    std::string GetMethodArgName(TCppMethod_t, int iarg);
    std::string GetMethodArgType(TCppMethod_t, int iarg);
    std::string GetMethodArgDefault(TCppMethod_t, int iarg);
    std::string GetMethodSignature(TCppScope_t scope, TCppIndex_t imeth);
    bool        IsConstMethod(TCppMethod_t);

    bool        ExistsMethodTemplate(TCppScope_t scope, const std::string& name);
    bool        IsMethodTemplate(TCppScope_t scope, TCppIndex_t imeth);
    TCppIndex_t GetMethodNumTemplateArgs(TCppScope_t scope, TCppIndex_t imeth);
    std::string GetMethodTemplateArgName(TCppScope_t scope, TCppIndex_t imeth, TCppIndex_t iarg);

    TCppMethod_t GetMethodTemplate(
        TCppScope_t scope, const std::string& name, const std::string& proto);
    TCppIndex_t  GetGlobalOperator(
        TCppType_t scope, TCppType_t lc, TCppScope_t rc, const std::string& op);

// method properties ---------------------------------------------------------
    bool IsConstructor(TCppMethod_t method);
    bool IsPublicMethod(TCppMethod_t method);
    bool IsStaticMethod(TCppMethod_t method);

// data member reflection information ----------------------------------------
    TCppIndex_t GetNumDatamembers(TCppScope_t scope);
    std::string GetDatamemberName(TCppScope_t scope, TCppIndex_t idata);
    std::string GetDatamemberType(TCppScope_t scope, TCppIndex_t idata);
    ptrdiff_t   GetDatamemberOffset(TCppScope_t scope, TCppIndex_t idata);
    TCppIndex_t GetDatamemberIndex(TCppScope_t scope, const std::string& name);

// data member properties ----------------------------------------------------
    bool  IsPublicData(TCppScope_t scope, TCppIndex_t idata);
    bool  IsStaticData(TCppScope_t scope, TCppIndex_t idata);
    bool  IsConstData(TCppScope_t scope, TCppIndex_t idata);
    bool  IsEnumData(TCppScope_t scope, TCppIndex_t idata);
    Int_t GetDimensionSize(TCppScope_t scope, TCppIndex_t idata, int dimension);

} // namespace Cppyy

#endif // !CPYCPPYY_CPPYY_H
