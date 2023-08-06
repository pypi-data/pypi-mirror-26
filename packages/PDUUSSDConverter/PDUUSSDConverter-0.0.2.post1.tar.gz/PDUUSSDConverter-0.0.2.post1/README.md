# PDU-USSDConverter
A Simple Utility to Convert Between PDU encoded text, USSD/GSM and String and
Vice-Versa.
This is works well with python3


## Installation
`pip install PDUUSSDConverter`


## Example

```
from PDUUSSDConverter import converter


ussd_code = converter.text_to_pdu(''*124#'')  # 'AA988C3602' (length=10)

pdu_to_text = converter.pdu_to_text('54747A0E6A97E7F3F0B90CBA87E7A0F1DB6D2FCBE9657208'))  # 'This message was converted!' (length=27)


```

Other Operations Available:

```
gsm_code_to_text(param: gsm_code) // Convert a gsm code into a unicode sequence
text_to_gsm_code(param: String)   // Converts text into gsm code sequence
```


## Credits

[Junior Polegato](https://github.com/JuniorPolegato/pdu_gsm_ussd)


