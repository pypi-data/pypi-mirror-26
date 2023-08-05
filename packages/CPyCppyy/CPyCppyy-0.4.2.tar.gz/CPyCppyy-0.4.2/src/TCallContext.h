#ifndef CPYCPPYY_TCALLCONTEXT_H
#define CPYCPPYY_TCALLCONTEXT_H

// Standard
#include <vector>


namespace CPyCppyy {

// general place holder for function parameters
    struct TParameter {
        union Value {
            bool         fBool;
            Short_t      fShort;
            UShort_t     fUShort;
            Int_t        fInt;
            UInt_t       fUInt;
            Long_t       fLong;
            ULong_t      fULong;
            Long64_t     fLongLong;
            ULong64_t    fULongLong;
            Float_t      fFloat;
            Double_t     fDouble;
            LongDouble_t fLongDouble;
            void*        fVoidp;
        } fValue;
        void* fRef;
        char  fTypeCode;
    };

// extra call information
    struct TCallContext {
        TCallContext(std::vector<TParameter>::size_type sz = 0) : fArgs(sz), fFlags(0) {}

        enum ECallFlags {
            kNone           =    0,
            kIsSorted       =    1,   // if method overload priority determined
            kIsCreator      =    2,   // if method creates python-owned objects
            kIsConstructor  =    4,   // if method is a C++ constructor
            kUseHeuristics  =    8,   // if method applies heuristics memory policy
            kUseStrict      =   16,   // if method applies strict memory policy
            kManageSmartPtr =   32,   // if executor should manage smart pointers
            kReleaseGIL     =   64,   // if method should release the GIL
            kFast           =  128,   // if method should NOT handle signals
            kSafe           =  256    // if method should return on signals
        };

    // memory handling
        static ECallFlags sMemoryPolicy;
        static bool SetMemoryPolicy(ECallFlags e);

    // signal safety
        static ECallFlags sSignalPolicy;
        static bool SetSignalPolicy(ECallFlags e);

    // payload
        std::vector<TParameter> fArgs;
        uint64_t fFlags;
    };

    inline bool IsSorted(uint64_t flags) {
        return flags & TCallContext::kIsSorted;
    }

    inline bool IsCreator(uint64_t flags) {
        return flags & TCallContext::kIsCreator;
    }

    inline bool IsConstructor(uint64_t flags) {
        return flags & TCallContext::kIsConstructor;
    }

    inline bool ManagesSmartPtr(TCallContext* ctxt) {
        return ctxt->fFlags & TCallContext::kManageSmartPtr;
    }

    inline bool ReleasesGIL(uint64_t flags) {
        return flags & TCallContext::kReleaseGIL;
    }

    inline bool ReleasesGIL(TCallContext* ctxt) {
        return ctxt ? (ctxt->fFlags & TCallContext::kReleaseGIL) : false;
    }

    inline bool UseStrictOwnership(TCallContext* ctxt) {
        if (ctxt && (ctxt->fFlags & TCallContext::kUseStrict))
            return true;
        if (ctxt && (ctxt->fFlags & TCallContext::kUseHeuristics))
            return false;

        return TCallContext::sMemoryPolicy == TCallContext::kUseStrict;
    }

} // namespace CPyCppyy

#endif // !CPYCPPYY_TCALLCONTEXT_H
