from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlComponent, QQmlEngine, QJSValue
from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl, pyqtSignal, QMetaObject, Q_ARG, QAbstractListModel
from PyQt5 import QtCore, QtQml
import sys
import pdb
from enum import IntEnum
class MyList(QAbstractListModel):

    class Roles(IntEnum):
        CardIdRole = QtCore.Qt.UserRole + 1
        NameRole = QtCore.Qt.UserRole + 2

    def __init__(self,  parent=None):
        QAbstractListModel.__init__(self)
        self._list = []

    def append(self, item):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        
        self._list.append(item)
        self.endInsertRows()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        print(role)
        if index.isValid() is True:
            if role == QtCore.Qt.DisplayRole:
                print('display role', self._list[index.row()])
                return QtCore.QVariant(self._list[index.row()])
            elif role == QtCore.Qt.ItemDataRole:
                print('itemdata role', self._list[index.row()])
                return QtCore.QVariant(self._list[index.row()])
            elif role == self.Roles.CardIdRole:
                return self._list[index.row()]['name']
            elif role == self.Roles.NameRole:
                return self._list[index.row()]['number']
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        print('RowCount', len(self._list))
        return len(self._list)

    def headerData(self, section,  orientation, role = QtCore.Qt.DisplayRole):
        pass

    def test_func(self):
        print('working')
        self.append({'name': 'josh', 'number': 9090909})

    def roleNames(self):
        return {self.Roles.CardIdRole: 'cardId'.encode(), self.Roles.NameRole: "name".encode()}


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

autoComplete = None
def onTextChanged(text):
    print("Text changed to: ", text)

if __name__ == "__main__":
    import pdb
    app = QApplication(sys.argv)
    # Register the Python type.  Its URI is 'People', it's v1.0 and the type
    # will be called 'Person' in QML.
    qmlRegisterType(TrackedCard, 'TrackedCards', 1, 0, 'TrackedCard')
    engine = QQmlApplicationEngine()
    ctxt = engine.rootContext()
    myList = MyList()
    myList.append({'name': 'josh', 'number': 9090909})
    ctxt.setContextProperty('pythonList', myList)
    engine.load(QUrl('vt.qml'))
    engine.quit.connect(app.quit)
    timer = QtCore.QTimer()
    timer.timeout.connect(myList.test_func)
    #timer.start(1000)
    autoComplete = engine.rootObjects()[0].findChild(QObject, 'autoComplete')
    autoComplete.textModified.connect(onTextChanged)
    # data = engine.rootObjects()[0].findChild(QObject, 'myList')
    # QMetaObject.invokeMethod(data, "append", 
    #             Q_ARG('QVariant', {'name':'Josh', 'number': 90}))
    sys.exit(app.exec_())