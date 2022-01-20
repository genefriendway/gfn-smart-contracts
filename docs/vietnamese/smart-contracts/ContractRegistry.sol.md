## Description
GFN sẽ có rất nhiều các smart contracts khác nhau, các smart contracts đó sẽ 
cần biết địa chỉ của nhau để tương tác.

ContractRegistry sẽ là nơi mà những smart contracts trong GFN được đăng ký, 
khi muốn tìm địa chỉ smart contract nào thì sẽ tìm trong ContractRegistry
## API
- `function registerContract(string memory name, address _address)`
  - đăng ký 1 địa chỉ contract và cùng với tên của nó vào registry
  - chỉ có gfnOwner mới có thể thực hiện đăng ký
- `function removeContract(string memory name, address _address)`
  - xóa bỏ 1 địa chỉ contract và tên của nó khởi registry
  - chỉ có gfnOwner mới có thể thực hiện xóa bỏ.
- `function getContractAddress(string memory name)`
  - lấy ra địa chỉ của 1 smart contract bởi tên đăng ký trong registry
  - ai cũng có thể gọi được hàm này
- `function getContractName(address _address)`
  - lấy ra tên của 1 smart contract bởi tên đợi chỉ đăng đăng ký của nó
  - ai cũng có thể gọi được hàm này