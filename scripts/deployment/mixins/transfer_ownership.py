#!/usr/bin/python3

class TransferOwnershipMixin:

    def transfer_contract_owner(self):
        print(f'==> Transferring Owner of {self.contract_name} '
              f'to {self.get_owner()}')
        self.contract_instance.transferOwnership(
            self.get_owner(),
            self.setting.TXN_SENDER
        )
