/****************************************************************************
** Meta object code from reading C++ file 'cannonfield.h'
**
** Created: Fri Nov 26 15:04:51 2010
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "cannonfield.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'cannonfield.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_CannonField[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
       9,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: signature, parameters, type, tag, flags
      13,   12,   12,   12, 0x05,
      19,   12,   12,   12, 0x05,
      37,   28,   12,   12, 0x05,
      64,   55,   12,   12, 0x05,

 // slots: signature, parameters, type, tag, flags
      88,   82,   12,   12, 0x0a,
     108,  102,   12,   12, 0x0a,
     122,   12,   12,   12, 0x0a,
     130,   12,   12,   12, 0x0a,
     142,   12,   12,   12, 0x08,

       0        // eod
};

static const char qt_meta_stringdata_CannonField[] = {
    "CannonField\0\0hit()\0missed()\0newAngle\0"
    "angleChanged(int)\0newForce\0forceChanged(int)\0"
    "angle\0setAngle(int)\0force\0setForce(int)\0"
    "shoot()\0newTarget()\0moveShot()\0"
};

const QMetaObject CannonField::staticMetaObject = {
    { &QWidget::staticMetaObject, qt_meta_stringdata_CannonField,
      qt_meta_data_CannonField, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &CannonField::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *CannonField::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *CannonField::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_CannonField))
        return static_cast<void*>(const_cast< CannonField*>(this));
    return QWidget::qt_metacast(_clname);
}

int CannonField::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: hit(); break;
        case 1: missed(); break;
        case 2: angleChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: forceChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 4: setAngle((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: setForce((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 6: shoot(); break;
        case 7: newTarget(); break;
        case 8: moveShot(); break;
        default: ;
        }
        _id -= 9;
    }
    return _id;
}

// SIGNAL 0
void CannonField::hit()
{
    QMetaObject::activate(this, &staticMetaObject, 0, 0);
}

// SIGNAL 1
void CannonField::missed()
{
    QMetaObject::activate(this, &staticMetaObject, 1, 0);
}

// SIGNAL 2
void CannonField::angleChanged(int _t1)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void CannonField::forceChanged(int _t1)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}
QT_END_MOC_NAMESPACE
