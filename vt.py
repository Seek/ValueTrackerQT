from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlComponent, QQmlEngine, QJSValue
from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl, pyqtSignal, QMetaObject, Q_ARG
import sys

class TrackedCard(QObject):

    nameChanged = pyqtSignal(str, arguments=['name'])
    costChanged = pyqtSignal(int, arguments=['cost'])
    cardsChanged = pyqtSignal('QVariantMap', arguments=['cards']) 
    
    def __init__(self, name='', cost=0, parent=None,):
        super().__init__(parent)

        # Initialise the value of the properties.
        self._name = name
        self._cost = cost

    # Define the getter of the 'name' property.  The C++ type of the
    # property is QString which Python will convert to and from a string.
    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    # Define the setter of the 'name' property.
    @name.setter
    def name(self, name):
        self._name = name
        self.nameChanged.emit(self._name)

    # Define the getter of the 'shoeSize' property.  The C++ type and
    # Python type of the property is int.
    @pyqtProperty(int, notify=costChanged)
    def cost(self):
        return self._cost

    # Define the setter of the 'shoeSize' property.
    @cost.setter
    def cost(self, cost):
        self._cost = cost
        self.costChanged.emit(self._cost)


if __name__ == "__main__":
    import pdb
    app = QApplication(sys.argv)
    # Register the Python type.  Its URI is 'People', it's v1.0 and the type
    # will be called 'Person' in QML.
    qmlRegisterType(TrackedCard, 'TrackedCards', 1, 0, 'TrackedCard')
    engine = QQmlApplicationEngine()
    engine.load(QUrl('vt.qml'))
    engine.quit.connect(app.quit)
    ctxt = engine.rootContext()
    objectName = engine.rootObjects()[0].findChild(QObject, 'card')
    objectName.cardsChanged.emit({'dd': 1})
    data = engine.rootObjects()[0].findChild(QObject, 'myList')
    QMetaObject.invokeMethod(data, "append", 
                Q_ARG('QVariant', {'name':'Josh', 'number': 90}))
    sys.exit(app.exec_())