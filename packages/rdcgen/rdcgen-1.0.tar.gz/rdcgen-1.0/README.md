Installation (for development/testing):

pip install --editable .

## Debugging notes:
## 
## Install requirements
##
##   pip install -r requirements.txt
##
## View results with colorizing
##
##   echo username | python rdcgen.py | ccze -A
##
## Count results
##
##   echo username | python rdcgen.py | ccze -A | wc -l
##
## Save results to file
##
##    echo jnorris | python rdcgen.py > ~/results.txt
##
## Create environment variable PSS and store password or an LM:NTLM hash of password there
## To generate the LM:NTLM password, run the following commands, then join the results with a ':'
## character and store that in the PSS variable.
##
##    apt-get install freeradius-utils
##    smbencrypt Myp\@\$\$word
##    export PSS=123123123123123123123123123:123123123123123123123123123
