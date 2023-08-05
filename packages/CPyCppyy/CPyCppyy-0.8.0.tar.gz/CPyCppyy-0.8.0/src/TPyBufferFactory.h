#ifndef CPYCPPYY_TPYBUFFERFACTORY_H
#define CPYCPPYY_TPYBUFFERFACTORY_H


namespace CPyCppyy {

/** Factory for python buffers of non-string type
      @author  WLAV
      @date    10/28/2004
      @version 1.5
*/

class TPyBufferFactory {
public:
    static TPyBufferFactory* Instance();

    PyObject* PyBuffer_FromMemory(bool* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(bool* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(short* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(short* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(unsigned short* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(unsigned short* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(Int_t* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(Int_t* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(UInt_t* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(UInt_t* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(Long_t* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(Long_t* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(ULong_t* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(ULong_t* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(float* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(float* buf, PyObject* sizeCallback);
    PyObject* PyBuffer_FromMemory(double* buf, Py_ssize_t size = -1);
    PyObject* PyBuffer_FromMemory(double* buf, PyObject* sizeCallback);

protected:
    TPyBufferFactory();
    ~TPyBufferFactory();
};

typedef TPyBufferFactory BufFac_t;

} // namespace CPyCppyy


#endif // !CPYCPPYY_TPYBUFFERFACTORY_H
