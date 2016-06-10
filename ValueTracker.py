from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlComponent, QQmlEngine, QJSValue
from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl, pyqtSignal, QMetaObject, Q_ARG, QAbstractListModel
from PyQt5 import QtCore, QtQml
import sys
import pdb
from enum import IntEnum
from hearthstone.enums import CardType
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class MyList(QAbstractListModel):

    class Roles(IntEnum):
        CardIdRole = QtCore.Qt.UserRole + 1
        NameRole = QtCore.Qt.UserRole + 2

    def __init__(self,  parent=None):
        QAbstractListModel.__init__(self)
        self._list = []

    def append(self, item):
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(), self.rowCount())

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

    def headerData(self, section,  orientation, role=QtCore.Qt.DisplayRole):
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
from hearthstone.objects import Card


class CardModel(QAbstractListModel):

    class Roles(IntEnum):
        CardIdRole = QtCore.Qt.UserRole + 1
        CardNameRole = QtCore.Qt.UserRole + 2
        CardCostRole = QtCore.Qt.UserRole + 3

    def __init__(self, session):
        QAbstractListModel.__init__(self)
        self.session = session
        self._cards = []

    def add_cards(self, cards):
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(), len(cards)-1)
        self._cards.extend(cards)
        self.endInsertRows()

    def reset(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        self._cards.clear()
        self.endRemoveRows()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid() is True:        
            if role == QtCore.Qt.DisplayRole:
                print('display role', self._cards[index.row()])
                return QtCore.QVariant(self._cards[index.row()])
            elif role == QtCore.Qt.ItemDataRole:
                print('itemdata role', self._cards[index.row()])
                return QtCore.QVariant(self._cards[index.row()])
            elif role == self.Roles.CardIdRole:
                return self._cards[index.row()].id
            elif role == self.Roles.CardNameRole:
                return self._cards[index.row()].name
            elif role == self.Roles.CardCostRole:
                return self._cards[index.row()].cost
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._cards)

    def roleNames(self):
        return {self.Roles.CardIdRole: 'cardId'.encode(), 
                self.Roles.CardNameRole: "name".encode(),
                self.Roles.CardCostRole: 'cost'.encode()}
autoComplete = None
session = None
model = CardModel(session)
    
def onTextChanged(text):
    from sqlalchemy import and_, or_
    cards = session.query(Card).filter(
        and_(Card.name.like('%{0}%'.format(text)), Card.collectible == 1,
             or_(Card.type == CardType.SPELL.value, Card.type == CardType.WEAPON.value,
                 Card.type == CardType.MINION.value)))
    cards = cards.order_by(Card.cost).order_by(Card.type.asc()). \
                            order_by(Card.name.asc()).limit(8).all()
    model.reset()
    model.add_cards(cards)

if __name__ == "__main__":
    import pdb
    app = QApplication(sys.argv)
    # Register the Python type.  Its URI is 'People', it's v1.0 and the type
    # will be called 'Person' in QML.
    qmlRegisterType(TrackedCard, 'TrackedCards', 1, 0, 'TrackedCard')
    engine = QQmlApplicationEngine()
    ctxt = engine.rootContext()
    # Initialize the data base
    sqlengine = create_engine('sqlite:///stats.db', echo=False)
    Session = sessionmaker()
    Session.configure(bind=sqlengine)
    session = Session()


    ctxt.setContextProperty('pythonList', model)
    engine.load(QUrl('vt.qml'))
    engine.quit.connect(app.quit)
    autoComplete = engine.rootObjects()[0].findChild(QObject, 'autoComplete')
    autoComplete.textModified.connect(onTextChanged)
    # data = engine.rootObjects()[0].findChild(QObject, 'myList')
    # QMetaObject.invokeMethod(data, "append",
    #             Q_ARG('QVariant', {'name':'Josh', 'number': 90}))
    sys.exit(app.exec_())
