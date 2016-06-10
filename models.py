from PyQt5 import QtCore

class TrackedDeckModel(QtCore.QAbstractListModel):
    """Provides data bout the deck to views in QML"""
    def __init__(self, base_deck):
        QtCore.QAbstractListModel.__init__()
        self._deck = base_deck.cards.copy()

    class Roles(IntEnum):
        """Internal enum to set roles for Qt"""
        CardIdRole = QtCore.Qt.UserRole + 1
        CardNameRole = QtCore.Qt.UserRole + 2
        CardCostRole = QtCore.Qt.UserRole + 3
        CardNumberRole = QtCore.Qt.UserRole + 4
        CardStateRole = QtCore.Qt.UserRole + 5

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
    