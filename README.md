# MessagePack
This is an implementation of MessagePack in Python.

## Usage
To use this module, simply import it and call the relevant functions. For example:
```python
from pack import pack
packed = pack(data)
```
You can see the demo code in `demo.py`.

Please note that by default, float data type is double-precision in Python. If you need to use single-precision when converting, please add the argument using_single_float=True to the pack function as shown below:
```python
from pack import pack
packed = pack(data, using_single_float=True)
```

## Testing
To test the module, please create a virtual environment and install the required packages using the following commands:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
Then, run the tests using the following command:
```bash
pytest test_pack.py
```
